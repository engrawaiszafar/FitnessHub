# core/tests.py
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
import datetime
from .models import Exercise  # <-- We need this new import


# Note: APITestCase creates a new, clean database for every single test function.
# This means tests don't interfere with each other.

class FitnessHubAPITests(APITestCase):

    def setUp(self):
        """
        This 'setUp' function runs before EVERY test function.
        We use it to create our reusable test users.
        """
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # We also create a re-usable exercise for user1
        self.exercise1 = Exercise.objects.create(
            user=self.user1,
            name='Bench Press',
            muscle_group='Chest'
        )

    # --- Test 1: User Registration & Login (Public Endpoints) ---

    def test_create_user(self):
        """
        Tests the /api/register/ endpoint.
        """
        payload = {'username': 'newtestuser', 'password': 'password123'}
        response = self.client.post('/api/register/', payload)

        # 201 (Created) means success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the user is actually in the database
        self.assertTrue(User.objects.filter(username='newtestuser').exists())

    def test_get_token(self):
        """
        Tests the /api/token/ endpoint.
        """
        payload = {'username': 'user1', 'password': 'password123'}
        response = self.client.post('/api/token/', payload)

        # 200 (OK) means success
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the response body contains a 'token'
        self.assertIn('token', response.data)

    # --- Test 2: Security & Permissions ---

    def test_unauthenticated_access(self):
        """
        Tests that a logged-out user CANNOT access protected data.
        """
        # We don't log in (no self.client.force_authenticate)
        # We now test the '/api/sets/' endpoint, which is protected.
        response = self.client.get('/api/sets/')

        # 401 (Unauthorized) is the expected failure
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_data_isolation(self):
        """
        Tests that User 1 CANNOT see User 2's data. This is critical.
        """
        # 1. User 1 logs in and creates a WorkoutSet (using the exercise we made in setUp)
        self.client.force_authenticate(user=self.user1)
        today = datetime.date(2025, 11, 4)
        self.client.post('/api/sets/', {
            'exercise': self.exercise1.id,
            'date': today,
            'reps': 10,
            'weight': 135
        })

        # 2. User 2 logs in
        self.client.force_authenticate(user=self.user2)

        # 3. User 2 tries to GET all sets
        response = self.client.get(f'/api/sets/?date={today}')

        # User 2 should get a 200 (OK) response, but the list of
        # sets should be empty (length 0).
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # --- Test 3: Workout Planner API (Authenticated) ---

    def test_create_exercise_and_set(self):
        """
        Tests the "happy path" for the workout planner.
        A user logs in, creates an exercise, then logs a set.
        """
        # 1. Log in as user1
        self.client.force_authenticate(user=self.user1)
        today = datetime.date(2025, 11, 4)

        # 2. Create a new Exercise
        exercise_payload = {
            'name': 'Squat',
            'muscle_group': 'Legs'
        }
        ex_response = self.client.post('/api/exercises/', exercise_payload)
        self.assertEqual(ex_response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the new exercise
        exercise_id = ex_response.data['id']

        # 3. Create a new WorkoutSet for that exercise
        set_payload = {
            'exercise': exercise_id,
            'date': today,
            'reps': 8,
            'weight': 225
        }
        set_response = self.client.post('/api/sets/', set_payload)
        self.assertEqual(set_response.status_code, status.HTTP_201_CREATED)

        # 4. List the sets for today and check that the data is correct
        list_response = self.client.get(f'/api/sets/?date={today}')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]['exercise_name'], 'Squat')
        self.assertEqual(list_response.data[0]['reps'], 8)

    # --- Test 4: Diet Planner API (Authenticated) ---

    def test_create_diet_log_and_add_food(self):
        """
        Tests the "happy path" for the diet planner.
        A user creates a log for the day, then adds food to it.
        """
        # 1. Log in as user1
        self.client.force_authenticate(user=self.user1)
        today = datetime.date(2025, 11, 4)

        # 2. Create a new DietLog for today
        log_payload = {'date': today}
        log_response = self.client.post('/api/dietlogs/', log_payload)
        self.assertEqual(log_response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the new log
        diet_log_id = log_response.data['id']

        # 3. Add a FoodItem to that log
        food_payload = {
            'diet_log_id': diet_log_id,
            'name': 'Apple',
            'calories': 95,
            'meal_type': 'Snacks'
        }
        food_response = self.client.post('/api/fooditems/', food_payload)
        self.assertEqual(food_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(food_response.data['name'], 'Apple')

        # 4. Get the DietLog and check that the food item is nested
        list_response = self.client.get(f'/api/dietlogs/?date={today}')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data[0]['food_items']), 1)
        self.assertEqual(list_response.data[0]['food_items'][0]['name'], 'Apple')