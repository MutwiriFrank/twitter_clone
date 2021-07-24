from rest_framework.serializers import ModelSerializer, SerializerMethodField, StringRelatedField
from .models import Profile, Skills


class SkillsSerializer(ModelSerializer):
    
    class Meta:
        model = Skills
        fields = ['name']


class ProfileSerializer(ModelSerializer):

    user = SerializerMethodField(read_only=True)
    skills = StringRelatedField(many=True)
    # skills = SkillsSerializer(many=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'profile_picture', 'skills', 'other_skills']
        
        
    def get_user(self, obj):
        return obj.user.username
    
    # def get_skills(self, obj):
    
    
    
class ProfileUpdateSerializer(ModelSerializer):
    
    user = SerializerMethodField(read_only=True)
    
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'location', 'profile_picture', 'skills', 'other_skills']
        # fields = "__al__"
        
    def get_user(self, obj):
        return obj.user.username
    
    # def get_skills(self, obj):
    #     return obj.skills.name


        
