from .views import getJobData
from django.urls import path

urlpatterns = [
    path('', getJobData, name='getJobData')

]