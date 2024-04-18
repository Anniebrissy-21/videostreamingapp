"""
URL configuration for videostreamingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static


from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("register/",views.RegistrationView.as_view(),name="signup"),
    path("",views.SignInView.as_view(),name="login"),

    path("profile/add",views.ProfileCreateView.as_view(),name="profile-add"),
    path("profile/<int:pk>/",views.ProfileDetailView.as_view(),name="profile"),
    path("profile/<int:pk>/change/",views.ProfileEditView.as_view(),name="profile-edit"),

    path("index/",views.IndexView.as_view(),name="index"),

    path("videos/add/",views.VideoCreateView.as_view(),name="video-add"),
    path("videos/<int:pk>/change/",views.VideoUpdateView.as_view(),name="video-edit"),
    path("videos/<int:pk>/delete/",views.VideoDeleteView.as_view(),name="video-delete"),
    path("videos/<int:pk>/",views.VideoDetailView.as_view(),name="video-detail"),

    path('stream-video/<int:video_id>/', views.stream_video, name='stream_video'),

    path("api/",include("api.urls"))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
