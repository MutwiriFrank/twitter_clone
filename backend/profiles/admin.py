from django.contrib import admin
from .models import Profile, FollowerRelation, Skills, Review

admin.site.register(Profile)

admin.site.register(Skills)

admin.site.register(FollowerRelation)

admin.site.register(Review)