# core/views.py
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import DailyWorkout, DietLog, FoodItem
from .serializers import (
    UserSerializer,
    DailyWorkoutSerializer,
    DietLogSerializer,
    FoodItemSerializer
)

class CreateUserViewSet(viewsets.ModelViewSet):
    """Create a new user in the system"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # No authentication needed to create a user
    permission_classes = [permissions.AllowAny]

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    # This view is provided by DRF, we just need to hook it into our URLs.
    # It takes 'username' and 'password' and returns a 'token'.
    pass

class DailyWorkoutViewSet(viewsets.ModelViewSet):
    """Manage daily workouts in the database"""
    serializer_class = DailyWorkoutSerializer
    queryset = DailyWorkout.objects.all()
    # Only allow authenticated users
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve the workouts for the authenticated user only"""
        # This ensures users can ONLY see their own data
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Save the new workout and assign it to the logged-in user"""
        serializer.save(user=self.request.user)

class DietLogViewSet(viewsets.ModelViewSet):
    """Manage daily diet logs in the database"""
    serializer_class = DietLogSerializer
    queryset = DietLog.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve the diet logs for the authenticated user only"""
        # This filters by user. We also filter by date if a 'date'
        # query param is provided, e.g., /api/dietlogs/?date=2025-10-31
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
        """
        Only return food items for the logged-in user.
        This works by finding the user's diet logs first.
        """
        return self.queryset.filter(diet_log__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new food item.
        We expect the 'diet_log_id' to be in the request data.
        """
        # We must check that the diet_log being added to
        # actually belongs to the user making the request.
        diet_log_id = self.request.data.get('diet_log_id')
        diet_log = DietLog.objects.get(id=diet_log_id, user=self.request.user)
        serializer.save(diet_log=diet_log)