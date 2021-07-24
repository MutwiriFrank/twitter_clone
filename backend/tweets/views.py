from django.shortcuts import render, redirect
from  django.http.response import  HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status

from tweets.models import Tweet, Comment
from . forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer, CommentSerializer , TweetUpdateSerializer
import random 

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
   
    return  render(request, 'tweets/home.html', context={}, status=200)

#using serializer
class TweetCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TweetCreateSerializer
    
    def post(self, request, *args, **kwargs):
        
        # 1 way
        
        # data = request.data or None
        # user = self.request.user or None
        # Tweet = Tweet.objects.create(
        #     content = data['content'],
        #     user = user
        # )
        
        serializer = TweetCreateSerializer(data = request.data or None)

        if serializer.is_valid( raise_exception=True ):
            print(serializer)
            serializer.save(user=request.user)
            return JsonResponse({}, status=201)
        return JsonResponse({}, status=401)


class TweetListView(APIView):
    serializer_class = TweetSerializer
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class TweetDetailView(APIView):
    serializer_class = TweetSerializer
    permission_classes = [AllowAny, ]
    
    def get(self, request, tweet_id, *args, **kwargs):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
            
        except:
            return Response("Tweet does not exist")
        if tweet:
            serializer = TweetSerializer(tweet)
            print('serializer :', serializer)
            print('data :', serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class TweetUpdateView(APIView):
    serializer_class = TweetUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request, tweet_id, *args, **kwargs):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except:
            return Response("tweet does not exist", status=status.HTTP_400_BAD_REQUEST)
        print(tweet)
        serializer = TweetUpdateSerializer(tweet)
        print('data :', serializer.data)
        return Response(serializer.data)
    
    def put(self, request, tweet_id, *args, **kwargs):
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except:
            return Response("tweet does not exist", status=status.HTTP_400_BAD_REQUEST)
        if tweet.user == request.user:
           
            serializer = TweetUpdateSerializer(tweet, data = request.data)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response('tweet updated', status=status.HTTP_200_OK)
                
        return Response("You are not the owner of this tweet")
        

class TweetDeleteView(APIView):
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated, ]
    
    def delete(self, request, tweet_id, *args, **kwargs):
        try:
            tweet = Tweet.objects.filter(id=tweet_id)
        except:
            return Response("Tweet does not exist")
        if tweet:
            try:
                tweet = tweet.filter(user=request.user).delete()
            except:
                return Response("You are not the owner of this tweet")
            
            
            return Response("Tweet deleted", status=status.HTTP_200_OK)   
  
  
class TweetLikeRetweetView(APIView):  
    '''
    This view is responsible for like, unlike and retweet action
    '''
    permission_classes = [IsAuthenticated, ]
    serializer_class = TweetActionSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = TweetActionSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            tweet_id = data.get("id")
            action = data.get("action")
            content = data.get("content")
             

            try:
                tweet = Tweet.objects.get(id=tweet_id)
            except:
                return  ("Tweet does not exist")
            if action == 'like':
                tweet.likes.add(request.user)
                print("added")
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif action == 'unlike':
                tweet.likes.remove(request.user) 
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif action == 'retweet':
                pass
                # new_retweet = Tweet.objects.create(
                #     user=request.user,
                #     parent = tweet,
                #     content = content,
                #     )
                # serializer = TweetSerializer(new_retweet)
                # print("serializer 11 ",serializer.data)
                # data = serializer.data
                # data
                # print("data", serializer.data['content'])
        return Response(serializer.data, status=status.HTTP_200_OK)


# class TweetsProfileView(APIView): 
#     # to be used in a users profile to list out their posts
#     permission_classes = [AllowAny, ]
#     serializer_class = TweetSerializer
    
#     def get(self, request, username, *args, **kwargs):
#         try:
#             user = User.objects.get(username=username)
#         except:
#             return Response("This user no longer exists")
        
#         tweets = Tweet.objects.filter(user=user) 
#         if tweets:
#             serializer = TweetSerializer(tweets, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response("This user has no posts")
          

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer
    
    def post(self, request, tweet_id, *args, **kwargs):
        user = request.user
        try:
            tweet = Tweet.objects.get(id = tweet_id)
        except :
            return Response("tweet does not exist, try again", status=status.HTTP_400_BAD_REQUEST)
       
        if tweet:
            
            # serializer = CommentSerializer(data=request.data) 
            # print('am here')
            # if serializer.is_valid(raise_exception=True):
            data = request.data
            content = data.get("content")
            comment = Comment.objects.create(tweet=tweet, user=request.user, content=content )
            
            serializer = CommentSerializer(comment)
            
            return Response(serializer.data, status=status.HTTP_200_OK)


class CommentEditView(APIView): 
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer   
    
    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response("comment does not exist", status=status.HTTP_400_BAD_REQUEST)
        if comment:
            
            serializer = CommentSerializer(comment)
            
            return Response(serializer.data)
        
    def put(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response("comment does not exist", status=status.HTTP_400_BAD_REQUEST)
    
        if comment.user == request.user:
            data = request.data
            comment.id = data['id']
            comment.image = data['image']
            comment.content = data['content']
            comment.tweet.id = data['tweet']
            comment.user = request.user
            
            comment.save()
            
            return Response("updated")                
        return Response("You are not the owner of this comment")

class CommentDeleteView(APIView): 
    permission_classes = [AllowAny, ]
  
    
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return Response("Comment does not exist", status=status.HTTP_400_BAD_REQUEST)  

        if comment.user == request.user:
            comment.delete()
            return Response("Comment deleted successfully", status=status.HTTP_200_OK)
        else:
            return Response("you cant delete this comment ")
        

class Search(APIView): # full text search using postgres
    permission_classes = [AllowAny, ]
    
    def get(self, request):
        pass

    
class AddFollower(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        pass

    
    
class Followers(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        pass
    
    
class BlockFollower(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        pass
   
    
class UnFollow(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        pass
    
    
class Following(APIView):
    permission_classes = [IsAuthenticated, ]
    
    def get(self, request):
        pass
    
    
class TweetsForFollowing(APIView):
     permission_classes = [IsAuthenticated, ]   


#using forms

def tweet_create_view(request, *args, **kwargs):
    pass
#     if not request.user.is_authenticated:
#         data = {
#             "message":"You are not logged in"
#         }
#         return JsonResponse(data, status=401)
    
    
#     form = TweetForm(request.POST or None)
#     next_url = form.data.get("next") or None
#     if form.is_valid():
        
       

#         obj = form.save(commit=False)
#         obj.user = request.user
#         print(obj.user)
#         obj.save()
#         if request.is_ajax():
#             print("it is ajax call")
#             return JsonResponse(obj.serialize(), status=201)

#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#             print (next_url)
#             return redirect(next_url)
            
        
#     #     form = TweetForm()
        
#     #     context = {
#     #         "form": form
#     #     }
        
#     # if form.errors:
#     #     if request.is_ajax():
#     #         return JsonResponse(form.errors, status=400)
#     # return render(request,'tweets/home.html', context)

def tweet_detail_view(request,tweet_id, *args, **kwargs):
    data = {"id": tweet_id, }
    status = 200
    try:
        tweet = Tweet.objects.get(id= tweet_id)
        data['content'] = tweet.content
    except:
        data['message'] = "not found"
        status = 404
    
    
    return JsonResponse(data, status=status)

def tweet_list_view(request,  *args, **kwargs):
    
    qs = Tweet.objects.all()
    # tweets_list = [{"id": x.id, "content": x.content, "likes":random.randint(1, 100)} for x in qs ] # python object to dictionary// serializer
    tweets_list = [x.serialize() for x in qs ] 
    data = {
        "isAdmin": False,
        "response": tweets_list
    }

    return JsonResponse(data)