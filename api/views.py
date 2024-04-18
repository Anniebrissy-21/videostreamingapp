from django.shortcuts import render
from django.contrib.auth.models import User

from api.serializer import UserSerialization,ProfileSerializer,VideoSerializer

from rest_framework import views,viewsets
from rest_framework.response import Response
from rest_framework import authentication,permissions

from myapp.models import UserProfile,Video

from django.http import StreamingHttpResponse
import cv2
import threading

class RegistrationView(views.APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerialization(data=request.data)

        if serializer.is_valid():
            user_object=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerialization(user_object)
            return Response(data=serializer.data)
        
        else:
            return Response(data=serializer.errors)

class UserProfileView(viewsets.ModelViewSet):

    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()

    def get_queryset(self):

        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):

        return serializer.save(user=self.request.user)



# class VideoView(viewsets.ModelViewSet):
#     authentication_classes=[authentication.TokenAuthentication]
#     permission_classes=[permissions.IsAuthenticated]

#     serializer_class=VideoSerializer
#     queryset=Video.objects.all()


#     def get_queryset(self):

#         return UserProfile.objects.filter(user=self.request.user)
    
#     def perform_create(self, serializer):

#         return serializer.save(user=self.request.user)
    

#     def stream_video(request, video_id):
#         video = Video.objects.get(pk=video_id)
#         video_url = video.video_url

#         def generate_frames():
#             cap = cv2.VideoCapture(video_url)
#             while(cap.isOpened()):
#                 ret, frame = cap.read()
#                 if ret:
#                 # Convert frame to bytes
#                     ret, buffer = cv2.imencode('.jpg', frame)
#                     if ret:
#                         yield (b'--frame\r\n'
#                             b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
#                 else:
#                     break
#             cap.release()

#         return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
