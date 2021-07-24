from django.urls import path


from . views import (tweet_detail_view, home_view, tweet_list_view, tweet_create_view,
                     TweetCreateView,TweetListView, TweetDetailView, TweetDeleteView , TweetUpdateView, TweetLikeRetweetView,
                     CommentCreateView, CommentEditView, CommentDeleteView )

app_name =  'tweets'

urlpatterns = [
    path('', home_view, name='home'),

    # path('tweets/', tweet_list_view, name="tweet_list" ),
    # path('tweet_create/', tweet_create_view, name="tweet_create" ),
    path('tweet/create/', TweetCreateView.as_view(), name="tweet_create" ),
    path('tweets/', TweetListView.as_view(), name="tweet_list" ),
    # path('tweets/<str:username>/', TweetsProfileView.as_view(), name="profile_tweet_list" ),
    path('tweet/<int:tweet_id>/', TweetDetailView.as_view(), name="tweet_detail" ),
    path('tweet/delete/<int:tweet_id>/', TweetDeleteView.as_view(), name="tweet_delete" ),
    path('tweet/update/<int:tweet_id>/', TweetUpdateView.as_view(), name="tweet_update" ),
    path('tweet/action/', TweetLikeRetweetView.as_view(), name="tweet_action" ),
    
    
    path('tweet/<int:tweet_id>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/edit/<int:comment_id>/', CommentEditView.as_view(), name='comment_edit'),
    path('comment/delete/<int:comment_id>/', CommentDeleteView.as_view(), name='comment_delete'),
]