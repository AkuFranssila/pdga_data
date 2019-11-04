# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import sys
import datetime
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#Check the latest member
def FindNewestMemberId():
    response = requests.get('https://www.pdga.com/players?FirstName=&LastName=&PDGANum=&Status=All&Class=All&MemberType=All&City=&StateProv=All&Country=All&Country_1=All&UpdateDate=&order=PDGANum&sort=desc')
    soup = BeautifulSoup(response.content, "html.parser")
    latest_member = soup.find(class_="odd views-row-first").find_all('td')[1].text.strip()

    try:
        test_latest_id = int(latest_member)
        if test_latest_id < 100000:
            sys.exit('Latest ID found was ' + test_latest_id + '. Latest ID is most likely not correct.')
    except:
        sys.exit('Errors testing latest PDGA ID found')
    logging.info('The latest member ID is ' + latest_member)
    return int(latest_member)


def TournamentDate(crawl_option):
    if crawl_option == 'all':
        start_date = '1979-01-01'
        end_date = str(datetime.datetime.today().year) + '-12-31'
        url = "https://www.pdga.com/tour/search?date_filter[min][date]=" + start_date + "&date_filter[max][date]=" + end_date
        return url
    elif crawl_option == 'latest':
        start_date = str(datetime.date.today().year) + '-' + str(datetime.date.today().month - 2 if datetime.date.today().month > 1 else 12) + '-' + str(datetime.date.today().day)
        end_date = str(datetime.datetime.today().year) + '-12-31'
        url = "https://www.pdga.com/tour/search?date_filter[min][date]=" + start_date + "&date_filter[max][date]=" + end_date
        return url
    elif crawl_option == 'test':
        start_date = '2019-11-1'
        end_date = '2019-11-5'
        url = "https://www.pdga.com/tour/search?date_filter[min][date]=" + start_date + "&date_filter[max][date]=" + end_date
        return url
    else:
        sys.exit('Option is not "all" or "latest". Unable to execute TournamentDate')

def TournamentLastPage(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    last_page = soup.find(class_="pager-last last").find('a')['href'].split('page=')[1]
    last_page = int(last_page)
    return last_page

#print (TournamentLastPage(TournamentDate("latest")))
#print (TournamentDate("latest"))
