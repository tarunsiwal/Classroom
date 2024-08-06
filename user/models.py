from django.db import models
from django.contrib.auth.models import User

class Additional_Fiels(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    phone_number= models.CharField('Phone Number',max_length=13,default="+91")
    rollno= models.CharField('Roll Number', max_length=10,help_text="Format : year/class/rollno")
  
    def __str__(self):
        return self.phone_number
    