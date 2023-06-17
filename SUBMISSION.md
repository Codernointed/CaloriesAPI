# Submission Checklist

## Repository Setup

- Clone the repository:
   git clone https://github.com/Codernointed/CaloriesAPI.git
- Install the dependencies:
    pip install -r requirements.txt

## Database Migration

- Apply the database migrations:
    python manage.py makemigrations
    python manage.py migrate

## Create Superuser

- Generate a superuser for testing:
    python manage.py createsuperuser


## Test Suite

- Run the tests:
 python manage.py test api.tests


## API Server

- Start the development server:
    python manage.py runserver
    The API server will be accessible at http://localhost:8000/.


## Pull Request

- [ ] A pull request has been raised for submission.
