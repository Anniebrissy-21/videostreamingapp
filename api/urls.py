from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("profiles",views.UserProfileView,basename="profile")
# router.register("videos",views.VideoView,basename="video")

urlpatterns=[
    path("register/",views.RegistrationView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]+router.urls