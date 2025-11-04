from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from datetime import date
from rest_framework.views import APIViewf

# --- UPDATED IMPORTS ---
from .models import (
    Exercise,
    WorkoutSet,
    DietLog,
    FoodItem
)
from .serializers import (
    UserSerializer,
    ExerciseSerializer,
    WorkoutSetSerializer,
    DietLogSerializer,
    FoodItemSerializer
)


class CreateUserViewSet(viewsets.ModelViewSet):
    """Create a new user in the system"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    pass

# --- NEW WORKOUT 2.0 VIEWSETS ---


class ExerciseViewSet(viewsets.ModelViewSet):
    """Manage exercises in the database (e.g., Bench Press, Squat)"""
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve the exercises for the authenticated user only"""
        # We also allow searching by name, e.g., /api/exercises/?name=bench
        queryset = self.queryset.filter(user=self.request.user)
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def perform_create(self, serializer):
        """Save the new exercise and assign it to the logged-in user"""
        serializer.save(user=self.request.user)


class WorkoutSetViewSet(viewsets.ModelViewSet):
    """Manage workout sets (reps, weight) in the database"""
    serializer_class = WorkoutSetSerializer
    queryset = WorkoutSet.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve the sets for the authenticated user only"""
        # We also allow filtering by date, e.g., /api/sets/?date=2025-11-05
        queryset = self.queryset.filter(user=self.request.user)
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def perform_create(self, serializer):
        """Save the new set and assign it to the logged-in user"""
        serializer.save(user=self.request.user)

# --- UNCHANGED DIET VIEWSETS ---


class DietLogViewSet(viewsets.ModelViewSet):
    """Manage daily diet logs in the database"""
    serializer_class = DietLogSerializer
    queryset = DietLog.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve the diet logs for the authenticated user only"""
        queryset = self.queryset.filter(user=self.request.user)
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def perform_create(self, serializer):
        """Save the new diet log and assign it to the logged-in user"""
        serializer.save(user=self.request.user)


class FoodItemViewSet(viewsets.ModelViewSet):
    """Manage food items for diet logs"""
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only return food items for the logged-in user."""
        return self.queryset.filter(diet_log__user=self.request.user)

    def perform_create(self, serializer):
        """
        --- THIS IS THE FIX ---
        Link the new food item to a diet log.
        The frontend must provide 'diet_log_id' in the request body.
        """
        diet_log_id = self.request.data.get('diet_log_id')

        # Check that the diet log exists and belongs to the user
        try:
            diet_log = DietLog.objects.get(id=diet_log_id, user=self.request.user)
        except DietLog.DoesNotExist:
            # If it doesn't exist or doesn't belong to user, deny permission
            raise permissions.PermissionDenied("Invalid diet log ID or not authorized.")

        # Save the food item, linked to the correct diet log
        serializer.save(diet_log=diet_log)


class DashboardView(APIView):
    """
    Provides a summary of workout and diet data for the current day.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today_date = date.today()

        # 1. Get Workout Summary for Today
        workout_sets = WorkoutSet.objects.filter(user=request.user, date=today_date)
        workout_serializer = WorkoutSetSerializer(workout_sets, many=True)

        # 2. Get Diet Summary for Today
        total_calories = 0
        try:
            diet_log = DietLog.objects.get(user=request.user, date=today_date)
            food_items = FoodItem.objects.filter(diet_log=diet_log)
            total_calories = sum(item.calories for item in food_items)
        except DietLog.DoesNotExist:
            pass  # total_calories remains 0

        # 3. Combine into one response
        data = {
            'workout_summary': workout_serializer.data,
            'diet_summary': {
                'total_calories': total_calories,
            }
        }
        return Response(data)
