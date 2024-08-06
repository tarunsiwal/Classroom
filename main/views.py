from django.shortcuts import redirect, render

from .forms import PostForm, FileForm, CreateAssignmentForm, SubmitAssignmentForm, CreateMeeting
from .models import Meeting_details, Post, File, Create_assignments, Submit_assignments, JoinURL_List
from django.contrib.auth.decorators import permission_required, login_required
from broadcast.views import ZoomMeetings, broadcast_sms, timestring
from django.contrib import messages
from django.contrib.auth.models import User
# from notifications.signals import notify

# Create your views here.
def home(request):
    return render(request, 'home.html',{})

@login_required(login_url='/user/login_user')
def base(request):
    user=User.objects.get(username=request.user)
    return render(request, 'base.html',{'user':user})

# --------------------------------announcement----------------------------------

def announce(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user and request.user.has_perm("main.delete_post")):
                post.delete()
      
    posts = posts[::-1]
    return render(request, 'announce.html', {"posts": posts,})

@permission_required("main.add_post",login_url='/announce',raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            message=f'there is an Announcement by {request.user}'
            broadcast_sms(request,message)
            return redirect("announce")
    else:
        form = PostForm()
    return render(request, 'create_post.html', {"form":form})

# --------------------------------assignments----------------------------------

def assignments(request):
    submitted_file = Submit_assignments.objects.all()
    submitted_file = submitted_file[::-1]
    created_file = Create_assignments.objects.all()
    created_file = created_file[::-1]
    return render(request, 'assignments.html',{'submitted_files':submitted_file, 
        'created_files':created_file
        })

@permission_required("main.add_post",login_url='/assignments',raise_exception=True)
def create_assignments(request):
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignments = form.save(commit=False)
            assignments.author = request.user
            assignments.save()
            message=f'New Assignment by {request.user}'
            broadcast_sms(request,message)
            return redirect("assignments")
    else:
        form = CreateAssignmentForm()
    
    return render(request, 'create_assignments.html',{'form':form})

@permission_required("main.add_post",login_url='/assignments',raise_exception=True)
def delete_created_assignment(request, pk):
    if request.method == 'POST':
        file = Create_assignments.objects.get(pk=pk)
        file.delete()
    return redirect('assignments')

def submit_assignments(request):
    if request.method == 'POST':
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignments = form.save(commit=False)
            assignments.author = request.user
            assignments.save()
            return redirect("assignments")
    else:
        form = SubmitAssignmentForm()
    return render(request, 'submit_assignments.html',{'form':form})

def delete_submitted_assignment(request, pk):
    if request.method == 'POST':
        file = Submit_assignments.objects.get(pk=pk)
        file.delete()
    return redirect('assignments')

def search_assignments(request):
	if request.method == "POST":
		searched = request.POST['searched']
		file =Create_assignments.objects.filter(title__icontains=searched) or Create_assignments.objects.filter(subject__icontains=searched)
		return render(request, 'search_assignments.html',{'searched':searched, 'files':file})
	else:
		return render(request,
		'search_assignments.html',
		{})


def timetable(request):
    
    return render(request, 'timetable.html',{})

# ------------------------------------notes----------------------------------------

def notes(request):
    file = File.objects.all()
    file = file[::-1]
    return render(request, 'notes.html', {'files': file})

@permission_required("main.add_post",login_url='/notes',raise_exception=True)
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.author = request.user
            file.save()
            message=f'New Notes have been uploaded by {request.user}'
            broadcast_sms(request,message)
            return redirect("notes") 
    else:
        form = FileForm()
    
    return render(request, "upload_files.html", {'form':form})

@permission_required("main.add_post",login_url='/notes',raise_exception=True)
def delete_file(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
    return redirect('notes')

def search_notes(request):
	if request.method == "POST":
		searched = request.POST['searched']
		file =File.objects.filter(title__icontains=searched) or File.objects.filter(created_at__icontains=searched)
		return render(request, 'search_notes.html',	{'searched':searched, 'files':file})
	else:
		return render(request,
		'search_notes.html',
		{})


# ------------------------------------classroom----------------------------------------

def classroom(request):
    list_items=JoinURL_List.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("joinurl_list-id")
        if post_id:
            post = JoinURL_List.objects.filter(id=post_id).first()
            if post and (post.author == request.user):
                post.delete()
    
    return render(request,'classroom.html',{'list_items':list_items})


def getmeeting(request):
    meeting=''
    if request.method == "POST":
        tipped = request.POST['tipped']
        zoom_meeting=ZoomMeetings()
        meeting = zoom_meeting.Getmeeting(tipped)
        
        join_url=meeting['join_url']
        password=meeting['password']
        start_time=meeting['start_time']
        description=meeting['topic']
        author = request.user
        start_time = timestring(start_time)
        JoinURL_List.objects.create(author=author,password=password,join_url=join_url,start_time=start_time, description=description)
        messages.success(request,'Join link is available for students.')
    
        return redirect('/classroom')
    else:
        meeting=False
        return render(request,{'meeting': meeting})

@permission_required("main.add_post",login_url='/classroom',raise_exception=True)
def create_meeting(request):
    if request.method == "POST":
        form = CreateMeeting(request.POST)
        if form.is_valid():
            fields = form.cleaned_data
            meeting=ZoomMeetings()
            meeting_id, start_link, password, start_time=meeting.CreateMeeting(fields)
            Meeting_details.objects.create(meeting_id=meeting_id,start_link=start_link, password=password, start_time=start_time)
            message=f'New class is arranged by {request.user}'
            broadcast_sms(request,message)
            messages.success(request,'The meeting has been created successfully')
            return redirect('/classroom')

    else:
        form = CreateMeeting()
    return render(request,'create_meeting.html',{'form':form})


def meeting_list(request):
    new_meeting_list=''
    if request.method == 'POST':
        zoom_meeting=ZoomMeetings()
        new_meeting_list = zoom_meeting.Displaymeetinglist()
        
            
    return render(request,'meeting_list.html',{'meeting_list': new_meeting_list})

def delete_meeting(request, id):
    if request.method == 'POST':
        zoom_meeting=ZoomMeetings()
        zoom_meeting.DeletMeeting(id)
        messages.error(request,'Meeting deleted successfully')
        return redirect('/classroom')



