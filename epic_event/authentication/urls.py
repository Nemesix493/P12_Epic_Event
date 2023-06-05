from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'authentication'
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair')
]