from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Job
from .serializers import JobSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET'])
def getAllData(request):
    jobs = Job.objects.all()
    paginator = PageNumberPagination()
    paged_jobs = paginator.paginate_queryset(jobs, request)
    serializer = JobSerializer(paged_jobs, many = True)
    return paginator.get_paginated_response(serializer.data)