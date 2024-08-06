from .models import  Post, File, Create_assignments, Submit_assignments
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

class FileForm(forms.ModelForm):
    class Meta:
        model= File
        fields= ["title","file"]

class CreateAssignmentForm(forms.ModelForm):
    class Meta:
        model=  Create_assignments
        fields= ["title","subject","assignment"]

class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model=  Submit_assignments
        fields= ["roll_no","assignment"]

class CreateMeeting(forms.Form):
    topic=forms.CharField(max_length=100)
    date = forms.DateField(widget = forms.widgets.DateInput(attrs={'type': 'date'}), label = 'Date', required = True,)
    time = forms.TimeField(widget = forms.widgets.TimeInput(attrs={'type': 'time'}), label = 'Time', required = True,)
    duration=forms.IntegerField(help_text='Duration of meeting in minutes',required=True)

    description= forms.CharField(widget= forms.widgets.TextInput(attrs={'type':'text'}),required=False,help_text='if any_')

    class Meta:
        fields= "__all__"
 
# class JoinLinkList(forms.ModelForm):
#     class Meta:
#         model= JoinURL_List
#         fields= ["meeting_id"]