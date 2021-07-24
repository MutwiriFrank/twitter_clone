from django.urls import path
from .views import (ProfileDetailView, ProfileUpdateView
                     )

app_name =  'profiles'

urlpatterns = [


   
    path('profile_update/', ProfileUpdateView.as_view(), name="profile_update" ),
     path('<str:username>/', ProfileDetailView.as_view(), name="profile" ),
    # path('tweet/create/', TweetCreateView.as_view(), name="tweet_create" ),
    # path('tweets/', TweetListView.as_view(), name="tweet_list" ),
    
]