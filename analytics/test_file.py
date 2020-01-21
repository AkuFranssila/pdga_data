# -*- coding: utf-8 -*-
import requests
import json
#https://emessukeskus-cache.s3-eu-west-1.amazonaws.com/fi/exhibitor/14185.json

#SHARD = 28
SHARD = CRAWLER_PARAMS['shard']

event_ids = [i for i in range(10000,17000)]

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


chunked_list = chunkIt(event_ids, 50)

all_data = []

for list in chunked_list[SHARD]:
    link_works = False
    try:
        req = requests.get("https://emessukeskus-cache.s3-eu-west-1.amazonaws.com/fi/exhibitor/" + str(list) + ".json")
        #req = requests.get("https://messukeskus.com/wp-json/em/v1/exhibitors/?events=13838")
        link_works = True
    except:
        None

    if link_works and req.status_code == 200:
        if len(req.json()) > 0:
            for c in req.json():
                c = c["meta"]
                data = {}

                COUNTRY_MAPPING = {"Finland": "FI", "Sweden": "SE", "Norway": "NO", "Netherlands": "NL", "Estonia": "EE", "Russia": "RU", "Denmark": "DK", "Germany": "DE"}

                first_name = c["contactFirstName"]
                last_name = c["contactLastName"]
                email = c["contactPersonEmail"]
                if email == "":
                    email = c["contactEmail"]
                phone = c["phone"]
                company_name = c["companyName"]
                company_website = c["homepage"]
                if company_website == "":
                    company_website = c["exhibitorWeb"]
                company_country = c["exhibitorCountry"]

                try:
                    country = COUNTRY_MAPPING[company_country]
                except:
                    country = "FI"

                contact_data = {"first_name":first_name, "last_name":last_name, "email":email, "phone": phone}
                for contact in contact_data.keys():
                    if contact_data[contact] == "":
                        contact_data.pop(contact)

                contact = contact_data
                contact["title"] = ""
                data['contacts'] = [contact]
                data['link'] = company_website
                data['company_name'] = company_name
                data['country'] = country
                all_data.append(data)

print (json.dumps(all_data, indent=4))
