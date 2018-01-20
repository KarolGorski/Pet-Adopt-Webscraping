webscraping-adopt-a-pet.herokuapp.com
=====================================
Webscraping pet objects from a local animal shelter's website, displaying them in the JSON format and storing them in a database.

Routes:
1. /
   returns a JSONified list of animals in the shelter
2. /db
   password protected, triggers a process of inserting freshly web-scraped pets data into db


Python libraries used:
* flask (web server)
* beautifulsoup4 (for webscraping)
* requests (downloading html pages to parse with beautifulsoup)
* pony ORM (creating and inserting pet objects into the database)