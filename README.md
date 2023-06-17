# CaloriesAPI
a REST API for the input of calories in Python

# api/models.py
# - Assumption: The `role` field in the `User` model is limited to the provided choices.
# - Choice: The `expected_calories` field in the `User` model is optional.

# api/views.py
# - Assumption: The API follows a standard CRUD (Create, Read, Update, Delete) pattern for users and entries.
# - Assumption: Only authenticated users can access the API endpoints.

# api/tests.py
# - Assumption: The test cases cover the basic functionality of user registration and entry creation.
# - Assumption: The test cases use the Django REST Framework test client for making API requests.

# calorie_tracker/urls.py
# - Assumption: The API root is located at the root URL ("/").
# - Assumption: The API authentication endpoints are accessible at "/api-auth/".

# calorie_tracker/serializers.py
# - Assumption: The `UserSerializer` and `EntrySerializer` define the fields to be serialized for user and entry objects.

# admin.py
# - Choice: The `User` and `Entry` models are registered with the Django admin for easy management.
