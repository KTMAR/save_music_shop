# Create your tasks here
import random
import string

from celery import shared_task
from .models import MediaType


@shared_task
def create_new_object():
    random_name = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
    new_object = MediaType.objects.create(name=random_name)
    return new_object.name

