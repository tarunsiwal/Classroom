from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    description= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title + "\n" + self.description


class File(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=50)
    file= models.FileField(upload_to='file/')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title + "\n" + self.file

class Create_assignments(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=50)
    subject= models.CharField(max_length=50)
    assignment= models.FileField(upload_to='created_assignments/')
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + "\n" + self.student
    
class Submit_assignments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_no= models.CharField('Roll Number', help_text='format:year/class/roll no.', max_length=50)
    assignment= models.FileField(help_text='rename file with subject_rollno.', upload_to='submitted_assignments/')
    submited_at=('submitted_at', models.DateTimeField(auto_now_add=True))

    def __str__(self):
        return self.roll_no

class Meeting_details(models.Model):

    meeting_id=models.SlugField(max_length=50)
    start_link=models.URLField(max_length=500)
    password=models.CharField(max_length=10)
    start_time=models.CharField(max_length=50)

    def __str__(self):
        return self.meeting_id

class JoinURL_List(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    join_url=models.CharField( max_length=250)
    password=models.CharField(max_length=10)
    start_time=models.CharField(max_length=50)
    description=models.CharField(max_length=350)


    def __str__(self):
        return self.join_url


