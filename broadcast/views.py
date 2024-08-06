from django.http import HttpResponse
from twilio.rest import Client
from user.models import Additional_Fiels
import jwt
import requests
import json
import datetime
from main.models import Meeting_details

# Broadcast SMS Text Messages TWILIO

def broadcast_sms(request,messages):
    message=messages
    message_to_broadcast = (f'''Message from CLASSROOM: {message} go check it!
    ''')
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    number_list=Additional_Fiels.objects.values_list('phone_number', flat = True)

    for recipient in number_list:
        if recipient:
            client.messages.create(to=recipient,
                                   from_='+18597109055',
                                   body=message_to_broadcast)

    return HttpResponse("messages sent!", 200)


class ZoomMeetings:

    def __init__(self):
        api_key = ''
        secret_key = ''
        self.email = 'tarunpanchal277@gmail.com'

        self.time_now = datetime.datetime.now()
        self.expiration_time = self.time_now + datetime.timedelta(seconds=20)
        self.expiration_in_seconds = round(self.expiration_time.timestamp())

        # token requirements
        self.headers = {"alg": "HS256","typ": "JWT"}
        self.payload = {"iss": api_key,"exp": self.expiration_in_seconds}

        # generate token
        self.request_token = jwt.encode(self.payload,secret_key,algorithm="HS256",headers=self.headers)
        

    def CreateMeeting(self,f):

        topic=f.get('topic')
        type=2
        duration=f.get('duration')
        date=f.get('date')
        time=f.get('time')
        start_time = f'{date}'+'T'+f'{time}'+':00Z'
        agenda=f.get('description')

        meeting_details = {"topic":topic,
                            "type": type,
                            "start_time": start_time,
                            "duration":duration,
                            "timezone": "Asia/India",
                            "agenda": agenda,
                            "recurrence": {"type": 1, "repeat_interval": 1},
                            "settings": {"host_video": "true",
                                "participant_video": "true",
                                "join_before_host": "False",
                                "mute_upon_entry": "False",
                                "watermark": "true",
                                "audio": "voip",
                                "auto_recording": "cloud"
                                }
                            }
        url = 'https://api.zoom.us/v2/users/'+self.email+'/meetings'
        header = {'authorization': 'Bearer '+self.request_token}
        zoom_create_meeting = requests.post(url,json=meeting_details, headers=header)
        json_data=json.loads(zoom_create_meeting.text)
        start_url=json_data['start_url']
        password =json_data['password']
        meeting_id=json_data['id']
        start_time=json_data['start_time']
        return meeting_id,start_url, password, start_time

    def DeletMeeting(self,meeting_id):
        url = 'https://api.zoom.us/v2/meetings/'+str(meeting_id)
        header = {'authorization': 'Bearer '+self.request_token}
        requests.delete(url, headers=header)

    def GetmeetingList(self):
        url = 'https://api.zoom.us/v2/users/'+self.email+'/meetings'
        header = {'authorization': 'Bearer '+self.request_token,'content-type':'application/json'}
        get_zoom_meeting = requests.get(url, headers=header)
        json_data=json.loads(get_zoom_meeting.text)
        return json_data['meetings']

    def Displaymeetinglist(self):

        zoom_meeting=ZoomMeetings()
        meeting_list = zoom_meeting.GetmeetingList()
        meeting_list = meeting_list[::-1]
        new_meeting_list=[]
        for meeting in meeting_list:
            ID=meeting['id']
            db_detail=Meeting_details.objects.filter(meeting_id=ID)
            meeting['start_url']="".join(db_detail.values_list('start_link', flat = True))
            meeting['password']="".join(db_detail.values_list('password', flat = True))
            st=meeting['start_time']
            meeting['start_time']=timestring(st)
            new_meeting_list.append(meeting)

        return new_meeting_list
    
    def Getmeeting(self,meeting_id):
        url = 'https://api.zoom.us/v2/meetings/'+str(meeting_id)
        header = {'authorization': 'Bearer '+self.request_token,'content-type':'application/json'}
        get_meeting = requests.get(url, headers=header)
        json_data=json.loads(get_meeting.text)
        return json_data

def timestring(string):
    st=string.split('T')
    dt=st[0]
    tm=st[1]
    tm=tm.split(':')
    hh=tm[0]
    mm=tm[1]
    tm=hh +':'+ mm
    return dt+', '+tm