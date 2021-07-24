from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL
# Create your models here.

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweet_likes_objects_user")
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="tweets_liked_user") # quotes because tweet model is below
    timestamp = models.DateTimeField(auto_now_add=True)
    

class Tweet(models.Model):
    id  = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL) # for retweet. A tweet will not have a parent unless it is retweeted
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'tweets')
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/tweet_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)	

    class Meta:
        ordering = ['-id']
        
        
    def __str__(self):
        return f'Tweet  {self.id}  by {self.user.username}'
    
        
    @property
    def is_retweet(self):
        # if parent == none its not a retweet if parent != None is not a retweet
        return self.parent != None


class Comment(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/comment_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    #parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return f'Comment {self.id} by {self.user.username}'
    
