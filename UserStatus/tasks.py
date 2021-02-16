from __future__ import absolute_import
from celery.decorators import task
from django.contrib.auth.models import User,auth
from django.contrib.auth import get_user_model
from django.conf import settings
from django.apps import apps
from .models import User
@task(serializer='json')
def set_status_to_inactive(email):
    print("celery used")
    user = User.objects.get(email=email)
    user.status = 'Neutral'
    user.is_active_status = False
    user.save()