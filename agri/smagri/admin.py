from django.contrib import admin

# Register your models here.
from .models import Crop  # Import your Crop model

admin.site.register(Crop)