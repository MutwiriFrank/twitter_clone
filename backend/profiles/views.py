from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response  import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status

from .serializers import ProfileSerializer, ProfileUpdateSerializer
from .models import Profile
from tweets.models import Tweet
from tweets.serializers import TweetSerializer


class ProfileDetailView(APIView):
    # to be used in a users profile to list out their posts and details
    permission_classes = [IsAuthenticatedOrReadOnly ]
    serializer_class = ProfileSerializer
    
    def get(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__username=username)
        except:
            return Response("This user no longer exists")
        print(profile.user)
        
        if profile:
    
            profile_serializer = ProfileSerializer(profile)
 
            user = profile.user
            print(user)
            # profile_tweets = Tweet.objects.filter(user = user)
            profile_tweets = user.tweets.all()
            
            serializer_tweets = TweetSerializer(profile_tweets, many=True)
           
            print(profile_serializer.data)
            print(serializer_tweets.data)
            data = {
                 
                "profile_data": profile_serializer.data,
                "profile_tweets": serializer_tweets.data
            }
            
            return JsonResponse(data, status=200)
            
            
            
        return Response("This user has no posts")
          
          
class ProfileUpdateView(APIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    
    def put(self, request, *args, **kwargs):
        print("am here")
      
        try:
            profile = Profile.objects.get(user = request.user)
        except:
            return Response("You cant edit this profile")
        
        
        if profile:
            serializer = ProfileUpdateSerializer(profile, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    
        return Response("You have to login to update the profile")