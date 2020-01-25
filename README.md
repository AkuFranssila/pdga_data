# Collect PDGA Data

This project is to collect all player and tournament data available on PDGA. PDGA does not offer any API to fetch the player data so all data needs to be crawled and then parsed to correct format and saved to MongoDB. As the project goes forward the work will focus on creating REST API that can be used to fetch data through an UI.

## Technologies used

- Python
  - MongoEngine
  - Requests
  - Logging
  - BeautifulSoup
- MongoDB
- Cronjobs
- GitHub
- CircleCI

## TODO
- [x] Add PDGA project finally to GitHub
- [x] Fix any missing fields in player crawling and fields that need to be added to db
- [x] Switch to MongoEngine
- [x] Create schemas for MongoDB documents
- [x] Save files instead of directly uploading to DB
- [x] Add merge file where logic happens for player and tournament parsing, change some fields from crawling to merge (address, name parsing)
- [x] Crawl players and add to database
- [x] Change parsing logic to be simpler so that the data type checks are done inside functions instead of creating more and more rules to parser
- [x] Check any mistakes/errors after all players crawled and rerun files if fixable in merge
- [x] Add crawling for tournaments
- [x] Add parsing for tournaments
- [x] Check any mistakes/errors after all tournaments crawled and rerun files if fixable in merge
- [x] Add CircleCI for automated testing
- [x] Create tests
- [x] Fix any errors and problems found after tests are done
- [x] Refactor whole crawling process to collect the whole page instead of crawling it for player and tournament data
- [x] Save the crawled pages to AWS S3
- [x] Refactor the parsing process to parse the crawled full html page
- [x] Save parsed data as json to AWS S3
- [x] Add Slack integration and send messages about important data processes to Slack channel for monitoring purposes.
- [ ] Refactor sending data to mongodb for player and tournaments
- [ ] Create statistics for players, tournaments
- [ ] Create statistics on country level + all
- [ ] Create cronjobs and automate the process
- [ ] Create API for the data (mongoDB + python + Flask)
- [ ] Create webpage where to show pdga data
- [ ] Make the data searchable through filters and/or remade statistics. (React)
