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
    BASE_URL = 'https://www.jobstreet.co.id/id/{}-jobs/in-Indonesia'.format(query)
    params = {'sort': 'createdAt', 'pg' : page}

    response = requests.get(BASE_URL, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    response.close()

    relevant_divs = soup.findAll('div', attrs={'data-search-sol-meta' : True})
    
    jobs = []
    for div in relevant_divs:
        try:
            data_container = div.div.div.article.div.div.div
            child_container1 = data_container.div
            child_container2 = child_container1.next_sibling
            job = {}

            job['position'] = next(div.find('div', attrs={'class' : 'z1s6m00 l3gun70 l3gun74 l3gun72'}).stripped_strings)
            job['created_at'] = child_container2.time['datetime']
            job['location'] = next(div.find('span', attrs={'class' : 'z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 y44q7ih'}).stripped_strings)
            job['company'] = next(div.find('span', attrs={'class' : 'z1s6m00 bev08l1 _1hbhsw64y _1hbhsw60 _1hbhsw6r'}).stripped_strings)
            job['source'] = 'jobstreet.co.id'
            job['url'] = 'https://www.jobstreet.co.id/{}'.format(div.find('a', attrs={'class' : 'jdlu994 jdlu996 jdlu999 y44q7i2 z1s6m00 z1s6m0f _1hbhsw6h'})['href'])

            if job_is_timely(job):
                jobs.append(job)
            
        
        except FileNotFoundError:
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