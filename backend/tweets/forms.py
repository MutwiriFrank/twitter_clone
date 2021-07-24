from django import forms

from .models import Tweet

class  TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get("content")
        maximum_content_length = 400
        
        if len(content) >  maximum_content_length :
            raise forms.ValidationError("This tweet is damn too long")
        return content