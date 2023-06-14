from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewset

user_router = SimpleRouter()
user_router.register('user', UserViewset, basename='user')

app_name = 'authentication'
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(user_router.urls))
]