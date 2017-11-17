# DigitalCrafts Alumni Registry

### This app makes it easy for employers to view active job seekers from [DigitalCrafts](http://digitalcrafts.com "DigitalCrafts Homepage").

Created by [Eric Schow](https://ericmschow.com "Eric's Portfolio"), a DigitalCrafts alumnus from the April 2017 Houston cohort, with the hope that future alumni will improve it with new features.

## Technologies
* __VueJS__ - latest and greatest Javascript front-end framework
* __Tornado__ - trusty and reliable Python back-end framework
* __Peewee__ - standard and simple Python object-relational-model
* __PostgreSQL__ - fast and powerful relational database
# __OAuth2__ - secure and user-friendly authentication

### To setup locally, for testing

* Clone repository & setup virtual environment
* `pip3 install -r requirements.txt`
* to use less & watch-run, `npm install`
* create SECRETS.ENV file containing `PORT`, `DATABASE_URL`, `SECRET`, `GOOGLE_SECRET`, and `GOOGLE_ID`, from the Heroku env
* Consider whether to swap Vue from Production mode by changing the CDN in the HTML pages
* `python3 app.py` and go! Check the command line for the server. It will automatically redeploy on changes to `app.py`.
* To deploy, `git push heroku`
