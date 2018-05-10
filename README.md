# WeConnect-Api
[![Build Status](https://travis-ci.org/King-Benx/WeConnect-Api-with-database.svg?branch=master)](https://travis-ci.org/King-Benx/WeConnect-Api-with-database)
[![Maintainability](https://api.codeclimate.com/v1/badges/e8559133a6c764fb9fdf/maintainability)](https://codeclimate.com/github/King-Benx/WeConnect-Api-with-database/maintainability) [![Coverage Status](https://coveralls.io/repos/github/King-Benx/WeConnect-Api-with-database/badge.svg?branch=master)](https://coveralls.io/github/King-Benx/WeConnect-Api-with-database?branch=master)
## DESCRIPTION

WeConnect provides a platform that brings businesses and individuals together. This platform
creates awareness for businesses and gives the users the ability to write reviews about the
businesses they have interacted with.

## WALK-THROUGH OF API
### [WeConnect Api Walk-through](https://youtu.be/52F-R9n-rsw)

## LINK TO API
### [WeConnect-API](https://weconnect-api-database.herokuapp.com)

## __Project captures the following routes__

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/v1/auth/login | Logs in a user |
| POST | api/v1/auth/logout | Logs out a user |
| POST | api/v1/auth/reset-password | Resets a users password |
| POST | api/v1/auth/register | Register a new user |
| GET | api/v1/businesses | Retrieves all businesses |
| POST | api/v1/businesses | Creates a new business |
| GET | api/v1/businesses/filter | Filter business by location/category |
| GET | api/v1/businesses/search | Search for a business by name |
| DELETE | api/v1/businesses/&lt;businessId&gt; | Delete a business |
| GET | api/v1/businesses/&lt;businessId&gt; | Get a business by id |
| PUT | api/v1/businesses/&lt;businessId&gt; | Update a specific business  |
| GET | api/v1/businesses/&lt;businessId&gt;/reviews | Get reviews of a business |
| POST | ap1/v1/businesses/&lt;businessId&gt;/reviews | Post a review about a business|

## BUILT WITH

* Flask - Python Framework used

## SETTING UP APPLICATION

1. Create a folder weconnect-api-with-database

    Clone repository to the folder

    **```git clone https://github.com/King-Benx/WeConnect-Api-with-database.git```**

2. Create a virtual environment that you are going to use while running the application locally

    **```$ virtualenv weconnect-env```**

    **```$ source weconnect-env/bin/activate```**

**NB: [More Information on setting up Virtual environments here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)**

3. Install all project dependencies using

    **```pip3 install -r requirements.txt```**

4. Set up a secret key for security purposes of your application

    **```SECRET_KEY = '<your_secret_key>'```**

5. For testing purposes create a postgresql database and set an environment variable TEST_DATABASE to set your DATABASE URI

    **```TEST_DATABASE = 'postgres://<db_user_name>:<password>@localhost/<database_name>'```**

6. For development purposes create a postgresql database and set an environment variable DEV_DATABASE to set your DATABASE URI

    **```DEV_DATABASE = 'postgres://<db_user_name>:<password>@localhost/<database_name>'```**

7. For staging purposes (stage before production ready) create a postgresql database and set an environment variable STAGING_DATABASE to set your DATABASE URI

    **```STAGING_DATABASE = 'postgres://<db_user_name>:<password>@localhost/<database_name>'```**

8. For production purposes create a postgresql database and set an environment variable WECONNECT_DATABASE to set your DATABASE URI

    **```WECONNECT_DATABASE = 'postgres://<db_user_name>:<password>@localhost/<database_name>'```**

**NB: [More Information on setting up postgresql here](https://wixelhq.com/blog/how-to-install-postgresql-on-ubuntu-remote-access)**
## RUNNING APPLICATION

1. Set the APPLICATION_CONFIG to define your settings. Select from (testing,development,staging,production)

    **```APPLICATION_CONFIG = <new_config>```**

2.  To launch the application, run the following command in your terminal

    **```python manage.py runserver```**

3. To launch the shell, run the following command in your terminal

    **```python manage.py shell```**

4. To run tests on the application, run the following command in your terminal

    **```python manage.py run_test```**

## Author

Asiimwe Benard
