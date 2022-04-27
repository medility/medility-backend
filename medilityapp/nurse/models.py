from django.db import models
from accounts.models import User

# Create your models here.
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    primary_pincode = models.IntegerField()
    secondary_pincode = models.IntegerField() 
    
    def __str__(self):
        return str(self.user)
    