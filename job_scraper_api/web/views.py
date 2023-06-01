from django.shortcuts import render
import requests
from urllib.parse import urlencode

# Create your views here.
def index(request):

    # check query params
    programmer = request.GET.get('programmer')
    data = request.GET.get('data')
    network = request.GET.get('network')
    cyber_security = request.GET.get('cyber_security')

    queries = ''

    if programmer:
        queries += 'Programmer,'
    if data:
        queries += 'Data,'
    if network:
        queries += 'Network,'
    if cyber_security:
        queries += 'Cyber Security'

    date_mode = request.GET.get('date_mode')
    date = request.GET.get('date')
    location = request.GET.get('location')
    company = request.GET.get('company')
    page = request.GET.get('page')

    if not queries:
        queries = None
    
    if not date_mode or not date:
        date_mode = None
        date = None
    
    if not location:
        location = None

    if not company:
        company = None

    if not page:
        page = 1
    else:
        page = int(page)

    params = {
        'query' : queries,
        'date_mode' : date_mode,
        'date' : date,
        'location' : location,
        'company' : company,
        'page' : page,
        'request' : request
    }

    response = requests.get('http://localhost:8000/jobs', params=params)
    next = None
    prev = None
    if response.status_code == 404:
        jobs = None
    else:
        jobs = response.json()
        if jobs.get('next'):
            current_params = request.GET.copy()
            current_params['page'] = page + 1
            next = f"{request.path}?{urlencode(current_params)}"
        if jobs.get('previous'):
            current_params = request.GET.copy()
            current_params['page'] = page - 1
            prev = f"{request.path}?{urlencode(current_params)}"

    result = {
        'jobs' : jobs,
        'page' : page,
        'next' : next,
        'prev' : prev
    }
    
    return render(request, 'index.html', result)