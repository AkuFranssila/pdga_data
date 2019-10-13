# Collect PDGA Data

This project is to collect all player and tournament data available on PDGA. PDGA does not offer any API to fetch the player data so all data needs to be crawled and then parsed to correct format and saved to MongoDB. As the project goes forward the work will focus on creating REST API that can be used to fetch data through an UI.

## Technologies used

- Python
  - Pymongo
  - Requests
  - Logging
  - BeautifulSoup
- MongoDB
- Cronjobs
- GitHub

## TODO
- [x] Add PDGA project finally to GitHub
- [ ] Fix any missing fields in player crawling and fields that need to be added to db
- [ ] Save files instead of directly uploading to DB
- [ ] Add merge page where logic happens for player and tournament parsing, change some fields from crawling to merge (address, name parsing)
- [ ] Crawl players and add to database
- [ ] Check any mistakes/errors after all players crawled and rerun files if fixable in merge
- [ ] Add crawling for tournaments
- [ ] Add parsing for tournaments
- [ ] Check any mistakes/errors after all tournaments crawled and rerun files if fixable in merge
- [ ] Create cronjobs and automate the process
- [ ] Create API for the data (mongoDB + python + Flask)
- [ ] Create webpage where to show pdga data
- [ ] Make the data searchable through filters and/or remade statistics. (React)
- [ ] Tests
