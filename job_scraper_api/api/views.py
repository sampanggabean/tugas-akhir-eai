from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Job
from .serializers import JobSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.
@api_view(['GET'])
def getJobData(request):

    # check query params
    queries = request.GET.get('query')
    date_mode = request.GET.get('date_mode')
    date = request.GET.get('date')
    location = request.GET.get('location')
    company = request.GET.get('company')

    jobs = Job.objects.all()

    if queries:
        queries = queries.split(',')
        q_objects = Q()
        for query in queries:
            q_objects |= Q(query__icontains=query)
        jobs = jobs.filter(q_objects)
        
    if date_mode and date: 
        if date_mode == 'before':
            jobs = jobs.filter(created_at__lt=date)
        if date_mode == 'after':
            jobs = jobs.filter(created_at__gt=date)
    if location:
        jobs = jobs.filter(location=location)
    if company:
        jobs = jobs.filter(Q(company__icontains=company))

    paginator = PageNumberPagination()
    paged_jobs = paginator.paginate_queryset(jobs, request)
    serializer = JobSerializer(paged_jobs, many = True)
    return paginator.get_paginated_response(serializer.data)
