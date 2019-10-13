# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import logging
import sys
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


print (FindNewestMemberId())
