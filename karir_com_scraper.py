import requests
import csv
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

def job_is_timely(job):
    today = date.today()
    delta = timedelta(days=60)

    two_months_ago = today - delta
    datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    datetime_str = datetime.strptime(job['created_at'], datetime_format)
    return datetime_str.date() > two_months_ago

def scrape_jobs_on_page(query, page):
    BASE_URL = "https://karir.com/search"
    params = {"q" : query, "page" : page}
    response = requests.get(BASE_URL, params=params)

    jobs = []

    soup = BeautifulSoup(response.content, "html.parser")
    relevant_divs = soup.find_all("div", {"class" : "row opportunity-box"})

    for relevant_div in relevant_divs:
        data_container = relevant_div.header

        job = {}

        job['position'] = next(data_container.a.stripped_strings)
        job['created_at'] = data_container.time['datetime']
        try:
            job['location'] = next(data_container.find("span", {"class" : "tdd-location"}).stripped_strings).split(" - ")[1]
        except:
            job['location'] = next(data_container.find("span", {"class" : "tdd-location"}).stripped_strings).split(" - ")[0]
        job['company'] = next( data_container.div.stripped_strings)
        job['source'] = 'karir.com'
        job['url'] = 'https://karir.com' + data_container.a['href']
        job['query'] = query

        if job_is_timely(job):
            jobs.append(job)

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
    with open('/home/sampanggabean22/scraping/result.txt', mode='w', newline="") as result_csv:
        column_headers = ['position', 'created_at', 'location', 'company', 'source', 'url', 'query']

        result_writer = csv.writer(result_csv, delimiter=',')
        result_writer.writerow(column_headers)

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
