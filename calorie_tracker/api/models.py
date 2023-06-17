
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
import requests
from requests.exceptions import RequestException
"""
The API follows the REST architectural style and adheres to the principles of resource-based routing, stateless communication, and standard HTTP methods.
   - The endpoints are designed to have meaningful and consistent names, such as `/users/` and `/entries/`.
   - The API utilizes the Django REST Framework to handle request parsing, validation, serialization, and response formatting.
   - The API supports authentication using tokens and session-based authentication, providing flexibility for different client requirements.
"""
class User(AbstractUser):
    ROLES = [
        ('regular', 'Regular User'),
        ('user_manager', 'User Manager'),
        ('admin', 'Admin'),]
    role = models.CharField(choices=ROLES, max_length=20)
    expected_calories = models.PositiveIntegerField(null=True, blank=True)
   
    groups = models.ManyToManyField('auth.Group',
        related_name='api_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Entry(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    text = models.TextField()
    calories = models.PositiveIntegerField()
    is_below_expected = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.calories:
            try:
                #A request to the Calories API provider to get the calories for the entered meal
                api_url = 'https://www.nutritionix.com/api/v1/calories'
                response = requests.get(api_url, params={'meal': self.text})
            
                if response.status_code == 200:
                    data = response.json()
                    self.calories = data['calories']
                else:
                    raise ValueError(f"Calories API request failed with status code: {response.status_code}")

            except RequestException as e:
                raise ValueError(f"Calories API request failed: {str(e)}")


        total_calories = Entry.objects.filter(
            user=self.user,
            date=self.date
        ).exclude(pk=self.pk).aggregate(models.Sum('calories'))['calories__sum'] or 0

        if total_calories < self.user.expected_calories:
            self.is_below_expected = True
        else:
            self.is_below_expected = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
