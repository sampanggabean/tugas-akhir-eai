import requests
import csv
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import json

def job_is_timely(job):
    today = date.today()
    delta = timedelta(days=60)

    two_months_ago = today - delta
    datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    datetime_str = datetime.strptime(job['created_at'], datetime_format)
    return datetime_str.date() > two_months_ago

def scrape_jobs_on_page(query, page):
    BASE_URL = 'https://www.kalibrr.com/id-ID/job-board/te/' + query + '/co/Indonesia/' + str(page)
    params = {'sort' : 'Freshness'}

    response = requests.get(BASE_URL, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    response.close()

    if soup.find('div', attrs={'class' : 'k-mx-4 k-my-4'}) is not None:
        return []

    script = json.loads(soup.find('script', id='__NEXT_DATA__').string)
    relevant_dict = script['props']['pageProps']['jobs']
    
    jobs = []
    for job_info in relevant_dict:
        try:
            job = {}

            job['position'] = job_info.get('name', 'NULL')
            job['created_at'] = job_info.get('createdAt', 'NULL')
            job['location'] = job_info.get('googleLocation', {}).get('addressComponents', {}).get('city', 'NULL')
            job['company'] = job_info.get('companyName', 'NULL')
            job['source'] = 'kalibrr.com'
            job['url'] = 'https://www.kalibrr.com/id-ID/c/{}/jobs/{}/{}'.format(job_info.get('companyInfo', {}).get('code', 'NULL'), job_info.get('id', 'NULL'), job_info.get('slug', 'NULL'))

            if job_is_timely(job):
                jobs.append(job)
            
        
        except:
            print("job failed to scrape")
    return jobs


def scrape_jobs(query):
    jobs = []
    page = 1

    scraped_jobs = scrape_jobs_on_page(query, page)
    jobs += scraped_jobs
    while len(scraped_jobs) != 0:
        page += 1
        scraped_jobs = scrape_jobs_on_page(query, page)
        jobs += scraped_jobs
    
    return jobs

def write_to_csv(jobs):
    with open('result.txt', mode='a', newline="") as result_csv:
        column_headers = ['position', 'created_at', 'location', 'company', 'source', 'url']

        result_writer = csv.writer(result_csv, delimiter=',')

        for i in range(len(jobs)):
            data_iter = jobs[i]
            row = []

            for column_header in column_headers:
                row.append(data_iter[column_header])
            
            result_writer.writerow(row)

def main():
    queries = ['Programmer', 'Data', 'Network', 'Cyber Security']
    jobs = []
    for query in queries:
        jobs += scrape_jobs(query)
        print(query + ' ' + str(len(jobs)))
    write_to_csv(jobs)

if __name__ == "__main__":
    main()