from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.home,name="home"),
    path('base',views.base,name="base"),
    path('announce',views.announce,name="announce"),
    path('create_post', views.create_post, name='create_post'),
    path('assignments',views.assignments,name="assignments"),
    path('create_assignments',views.create_assignments,name="create_assignments"),
    path('created_assignments/<int:pk>/delete/',views.delete_created_assignment,name='delete_assignment'),
    path('submit_assignments',views.submit_assignments,name="submit_assignments"),
    path('search_assignments',views.search_assignments,name="search_assignments"),
    path('submitted_assignments/<int:pk>/delete/',views.delete_submitted_assignment,name='delete_submitted_assignment'),
    path('timetable',views.timetable,name="timetable"),
    path('notes',views.notes,name="notes"),
    path('upload_file',views.upload_file,name='upload_file'),
    path('notes/<int:pk>/delete/',views.delete_file,name='delete_file'),
    path('search_notes',views.search_notes,name="search_notes"),
    path('broadcast/',include("broadcast.urls")),
    path('create_meeting',views.create_meeting,name="create_meeting"),
    path('classroom',views.classroom,name="classroom"),
    path('Meeting/<int:id>/delete_meeting',views.delete_meeting,name="delete_meeting"),
    path('meeting_list',views.meeting_list,name="meeting_list"),
    path('getmeeting',views.getmeeting,name="getmeeting"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()