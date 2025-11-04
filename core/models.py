from django.db import models
from django.contrib.auth.models import User

# --- NEW WORKOUT PLANNER 2.0 MODELS ---
# We are replacing the old 'DailyWorkout' model with these.

class Exercise(models.Model):
    """
    Represents a single exercise.
    e.g., "Bench Press", "Squat", "Treadmill Run"
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises',
                             help_text="The user who created this exercise.")
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=50, blank=True, null=True,
                                    help_text="e.g., 'Chest', 'Legs', 'Cardio'")

    class Meta:
        # A user cannot have two exercises with the same name
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class WorkoutSet(models.Model):
    """
    Represents a single set of an exercise performed by a user.
    e.g., User 1 did 'Bench Press' on '2025-11-05' for '10 reps' at '135.5 lbs'
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='sets')
    date = models.DateField(help_text="The date the workout was performed.")
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2,
                                 help_text="Weight in lbs or kgs.")

    class Meta:
        # Order by date when querying
        ordering = ['date']

    def __str__(self):
        return f"{self.user.username} - {self.exercise.name} ({self.reps} reps @ {self.weight} lbs)"


# --- DIET PLANNER MODELS (Unchanged) ---
# These models are not affected.

class DietLog(models.Model):
    """
    Represents a single day's diet log for a user.
    This will be the parent for all food items on a specific date.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_logs')
    date = models.DateField()

    class Meta:
        # Ensures a user can only have one diet log per day
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username}'s Diet Log for {self.date}"

class FoodItem(models.Model):
    """
    Represents a single food item within a meal, linked to a DietLog.
    """
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
    ]

    diet_log = models.ForeignKey(DietLog, on_delete=models.CASCADE, related_name='food_items')
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES)
    name = models.CharField(max_length=200)
    calories = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.calories} kcal) for {self.diet_log.user.username}"
