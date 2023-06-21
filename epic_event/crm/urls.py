from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import ProspectViewset, ClientViewset

company_router = SimpleRouter()
company_router.register('prospect', ProspectViewset, basename='prospect')
company_router.register('client', ClientViewset, basename='client')

app_name = 'crm'
urlpatterns = [
    path('', include(company_router.urls))
]