from .views import getAllData
from django.urls import path

urlpatterns = [
    path('jobs', getAllData, name='getAllData')
]