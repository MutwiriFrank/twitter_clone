from .models import Tweet, Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(allow_null=True, required=False)
    content = serializers.SerializerMethodField(allow_null=True, required=False)
    class Meta:
        model = Comment
        fields =  ('id','image','content','user','tweet')
      
        
    def get_content(self, obj):
        try:
            content = obj.content
        except:
            content = None
        return content   
        
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    


# create only serializer    
class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id','content', 'likes']
        
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        maximum_content_length = 400
        
        if len(value) >  maximum_content_length :
            raise serializers.ValidationError("This tweet is damn too long")
        return value
    
 
# Read only serializer    
class TweetSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(allow_null=True, required=False, read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)
    all_comments = CommentSerializer(source='comments', many=True)
    class Meta:
        model = Tweet
        fields = ['id','content', 'likes', 'is_retweet', 'image', 'all_comments', 'user']
        
    def get_likes(self, obj):
        likes = obj.likes

        return obj.likes.count()
    
    def get_content(self, obj):
        
        if obj.is_retweet:
            
            content = obj.parent.content
          
        return obj.content
    
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    
 
class TweetUpdateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(allow_null=True, required=False)


    class Meta:
        model = Tweet
        fields = ['id','content', 'image',  ]
        
    
    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    
    
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField( required=False,  allow_blank=True)
    
    def validate_actions(self, value):
        value = value.lower().strip()
        TWEET_ACTION_OPTIONS = ('like','unlike','retweet')
        
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid value')
        return value
    



    
    
    