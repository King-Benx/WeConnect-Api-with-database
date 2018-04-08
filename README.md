# WeConnect-Api-with-database
## DESCRIPTION
WeConnect provides a platform that brings businesses and individuals together. This platform 
creates awareness for businesses and gives the users the ability to write reviews about the 
businesses they have interacted with.

## FEATURES THAT THE APPLICATION ENCOMPASSES
1. An API connecting to a postgress database

## FlOW OF WEB APPLICATION
![wireframe](https://github.com/King-Benx/WeConnect-ui-designs/blob/master/designs/wireframes/wireframes.png)

## LINK TO WeConnect on Github Pages
### [WeConnect](https://king-benx.github.io/)

## LINK To WeConnect-API using non-persistent data
### [WeConnect-API (no database)](https://evening-gorge-56404.herokuapp.com/)

## BUILT WITH
* Bootstrap 3 - The Web framework used
* Jquery - JavaScript Library used
* Flask - Python Framework used
## RUNNING THE APPLICATION
1. Create a folder weconnect-api-with-database

   Clone repository to the folder
   ``` git clone https://github.com/King-Benx/WeConnect-Api-with-data-structures.git ```
2. A file that contains all necessary extensions exists within the app, to get all dependencies run the following command
  ```**pip3 install -r requirements.txt**```
3. Configurations are handled by the **config.py** file and any environmental variables should occur in this file.
4. Set up postgresql database and copy connection string in format.

    ``` DATABASE_URL='postgres://<db_user_name>:<password>@localhost/<database_name>' ```

5. To launch the application run the following command in your terminal
```**python manage.py runserver**```
6. To launch the shell run the following command in your terminal
``` **python manage.py shell**```
7. To run tests on the application, run the following command in your terminal
``` **python manage.py run_test**```
## Author
Asiimwe Benard
