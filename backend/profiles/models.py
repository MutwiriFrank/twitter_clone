from django.db import models
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


# Skills are added by teh user to indicate skills they are proficient in
class Skills(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=150, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class  Meta:
        verbose_name_plural="skills"
     

class FollowerRelation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=220, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    skills = models.ManyToManyField(Skills, related_name='personal_skills', null=True, blank=True)
    other_skills = models.CharField(max_length=220, null=True, blank=True)
    
    def __str__(self):
        return str(self.user.username)


class Review(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True )
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return str( self.product)  + " - " + (self.rating)



def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)

