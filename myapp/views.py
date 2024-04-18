from typing import Any
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,DetailView,ListView,UpdateView,TemplateView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.views.decorators import gzip

from myapp.forms import RegistrationForm,LoginForm,ProfileForm,VideoForm
from myapp.models import UserProfile,Video

from django.http import StreamingHttpResponse
import cv2
import threading
# Create your views here.


class RegistrationView(CreateView):
    template_name="signin.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("login")


class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                print("Login Success")
                return redirect("index")
                
        print("Invalid Credentials")
        return render(request,"signin.html",{"form":form})


class ProfileCreateView(CreateView):
    template_name="profile_add.html"
    form_class=ProfileForm
    success_url=reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


 
class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

    def get_context_data(self,**kwargs: Any):
        context=super().get_context_data(**kwargs)
        qs=self.request.user.video_profile.all()
        context["videos"]=qs
        return context

class ProfileEditView(UpdateView):
    template_name="profile_edit.html"
    form_class=ProfileForm
    model=UserProfile
    success_url=reverse_lazy("index")


class IndexView(ListView):
    template_name="index.html"
    context_object_name="data"
    model=Video

    def post(self,request,*args,**kwargs):
        title=request.POST.get("box")
        qs=Video.objects.filter(title__icontains=title)
        return render(request,"index.html",{"data":qs})

    

class VideoCreateView(CreateView):
    template_name="video_add.html"
    form_class=VideoForm
    success_url=reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
class VideoUpdateView(UpdateView):
    template_name="video_update.html"
    form_class=VideoForm
    model=Video
    success_url=reverse_lazy("index")

class VideoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Video.objects.get(id=id).delete()
        return redirect("index")
    
class VideoDetailView(DetailView):
    template_name="video_detail.html"
    model=Video
    context_object_name="data"


def stream_video(request, video_id):
    video = Video.objects.get(pk=video_id)
    video_url = video.video_url

    def generate_frames():
        cap = cv2.VideoCapture(video_url)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                # Convert frame to bytes
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                break
        cap.release()

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

# @gzip.gzip_page
# def Home(request):

#     try:
#         camera=VideoCamera()
#         return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')
    
#     except:
#         pass

#     return render(request,"video_stream.html")


# class VideoCamera(object):

#     def __init__(self,request):
#         self.video=cv2.VideoCapture(0)
#         (self.grabbed, self.frame)=self.video.read()
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         image=self.frame
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
    
#     def update(self):
#         while True:
#             (self.grabbed, self.frame)=self.video.read()


# def gen(camera):
#     while True:
#         frame=camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


