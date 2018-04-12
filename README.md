# WeConnect-Api-with-database
[![Build Status](https://travis-ci.org/King-Benx/WeConnect-Api-with-database.svg?branch=master)](https://travis-ci.org/King-Benx/WeConnect-Api-with-database)
## DESCRIPTION

WeConnect provides a platform that brings businesses and individuals together. This platform
creates awareness for businesses and gives the users the ability to write reviews about the
businesses they have interacted with.

## LINK TO API
### [WeConnect-API-with-postgres](https://weconnect-api-database.herokuapp.com)

A default user has already been created

### CREDENTIALS

    {
      'email':'johndoe@mail.com',
      'password':'pass'
    }

## FEATURES THAT THE APPLICATION ENCOMPASSES

1.  An API connecting to a postgress database

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
