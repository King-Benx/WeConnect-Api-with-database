# WeConnect-Api-with-database
[![Build Status](https://travis-ci.org/King-Benx/WeConnect-Api-with-database.svg?branch=master)](https://travis-ci.org/King-Benx/WeConnect-Api-with-database)
[![Maintainability](https://api.codeclimate.com/v1/badges/e8559133a6c764fb9fdf/maintainability)](https://codeclimate.com/github/King-Benx/WeConnect-Api-with-database/maintainability) [![Coverage Status](https://coveralls.io/repos/github/King-Benx/WeConnect-Api-with-database/badge.svg)](https://coveralls.io/github/King-Benx/WeConnect-Api-with-database)
## DESCRIPTION

WeConnect provides a platform that brings businesses and individuals together. This platform
creates awareness for businesses and gives the users the ability to write reviews about the
businesses they have interacted with.

## LINK TO API
### [WeConnect-API-with-postgres](https://weconnect-api-database.herokuapp.com)

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
| GET | api/v1/businesses/&lt;businessId&gt; | Get a business by Id |
| PUT | api/v1/businesses/&lt;businessId&gt; | Update a specific business  |
| GET | api/v1/businesses/&lt;businessId&gt;/reviews | Get reviews of a business |
| POST | ap1/v1/businesses/&lt;businessId&gt;/reviews | Post a review about a business|

## BUILT WITH

* Flask - Python Framework used

## RUNNING THE APPLICATION

1. Create a folder weconnect-api-with-database

    Clone repository to the folder

    **```git clone https://github.com/King-Benx/WeConnect-Api-with-database.git```**

2. Create a virtual environment that you are going to use while running the application locally

    **```$ virtualenv weconnect-env```**

    **```$ source weconnect-env/bin/activate```**

### MORE INFORMATION ON VIRTUAL ENVIRONMENTS

### [Setting up Virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)

3. A file that contains all necessary extensions exists within the app, to get all dependencies run the following command

    **```pip3 install -r requirements.txt```**

4. Configurations are handled by the **config.py** file and any environmental variables should occur in this file.
5. Set up postgresql database and copy connection string in format.

    **```DATABASE_URI='postgres://<db_user_name>:<password>@localhost/<database_name>'```**

6. To start the Api, you set up the following environment varriables

    Set up the environment to use, the default is set to Development Configurations, to change set the environment variable

    **```APPLICATION_CONFIG = <new_config>```**

    Set path to the database

    **```WECONNECT-DATABASE = <'postgres://<db_user_name>:<password>@localhost/<database_name>'>```**

7.  To launch the application run the following command in your terminal

    **```python manage.py runserver```**

8. To launch the shell run the following command in your terminal

    **```python manage.py shell```**

9. To run tests on the application, run the following command in your terminal

    **```python manage.py run_test```**

## Author

Asiimwe Benard
