from django.db import models
from accounts.models import User
# Create your models here.


class Society(models.Model):
    society_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pincode = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class DeviceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class CommunityUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_setup = models.BooleanField()
    setup_type = models.ManyToManyField(DeviceType)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    country = models.CharField(max_length=100)
    default_steps = models.IntegerField(default=5000)
    device_user_id = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.user.name


class CommunityActivityInfo(models.Model):
    community_user = models.ForeignKey(CommunityUserInfo, on_delete=models.CASCADE)
    target_steps = models.IntegerField()
    completed_steps = models.IntegerField()
    activity_date = models.DateField()

    def __str__(self) -> str:
        return '%s   %s/%s' % (self.community_user.user.name, self.completed_steps, self.target_steps)


class CommunityGroup(models.Model):
    name = models.CharField(max_length=100)
    

class CommunityGroupInfo(models.Model):
    communityUser = models.ForeignKey(CommunityUserInfo, on_delete=models.CASCADE)
    communityGroupInfo = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
