import requests
import csv
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import time

def job_is_timely(job):
    today = date.today()
    delta = timedelta(days=60)

    two_months_ago = today - delta
    datetime_format = '%Y-%m-%d'
    datetime_str = datetime.strptime(job['created_at'], datetime_format)
    return datetime_str.date() > two_months_ago

def scrape_jobs(query):
    jobs = []
    BASE_URL = 'https://www.linkedin.com/jobs/search?keywords={}&location=Indonesia'.format(query)

    display = Display(visible=0, size=(1920, 1080))  
    display.start()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("-disable-notifications")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920x1080")

    wd = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)
    wd.get(BASE_URL)

    max_page = 40 # could be wrong
    try:
        num = int(wd.find_element(By.CSS_SELECTOR, 'h1>span').get_attribute('innerText'))
        num = int(num / 25) + 1
    except:
        num = max_page


    for i in range(min(num, max_page)): 
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')

        try:
            element = wd.find_element(By.CLASS_NAME, 'two-pane-serp-page__results-list').find_element(By.TAG_NAME, 'button')
            element.click()
            time.sleep(3)
        except:
            pass
            time.sleep(3)

    job_lists = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    job_lists = job_lists.find_elements(By.TAG_NAME, 'li')

    print(len(job_lists))

    for job_container in job_lists:
        try:
            job = {}

            job['position'] = job_container.find_element(By.CLASS_NAME, 'base-search-card__title').get_attribute('innerText')
            job['created_at'] = job_container.find_element(By.CLASS_NAME, 'job-search-card__listdate').get_attribute('datetime')
            job['location'] = job_container.find_element(By.CLASS_NAME, 'job-search-card__location').get_attribute('innerText').split(',')[0]
            job['company'] = job_container.find_element(By.CLASS_NAME, 'base-search-card__subtitle').get_attribute('innerText')
            job['source'] = 'linkedin.com/jobs'
            job['url'] = job_container.find_element(By.TAG_NAME, 'a').get_attribute('href')

            if job_is_timely(job):
                jobs.append(job)
        except:
            pass
    
    print('{}: {}'.format(query, len(jobs)))
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