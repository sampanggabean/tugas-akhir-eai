from .views import getJobData
from django.urls import path

urlpatterns = [
    path('jobs', getJobData, name='getJobData')

]