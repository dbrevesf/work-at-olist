# Work at Olist - Telephone Bill Project

## Project Documentation

* Description

  This project was made for the selection process of a software engineer role at Olist. I was asked to implement an application that receives call detail records and calculates monthly bills for a given phone number and it would be necessary to provide a HTTP REST API to attend the requirements. Beside the application itself, I also was asked to write the project documentation and the API documentation. Both documentation will be presented below. 

* Installing

  The installation process of this project it's very simple. Once you have the Python and Pip installed, you just need to clone this repository, enter in the project root directory and execute: 

  ```pip install -r requirements.txt```

  It's a good practice create a virtual enviroment, but that's up to you.

  After all the requirements is installed, we need to install PostgreSQL and create a database for our project. The database credentials could vary depend on the enviroment that you'll work, but, for run it locally, create an user, a database and a password with the same value: 'olist'. It will make it easy for you.

  If you have any trouble to use PostgreSQL, access this [link](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e) that you'll have all the informations that you need. 
  
  Now, with everything installed, it's time to apply the Django's migration to create our database tables. So, on a terminal, inside the root directory of the project, you'll execute:

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

  The ```makemigrations``` generates a lot of files that the command ```migrate``` will use. 

  Obs: If you're planning to host this project on Heroku, be aware that you'll need to commit the migrations files and apply just the ```migration``` there. Unfortunately, the command ```makemigrations``` don't work on Heroku instances. 

  Now everything's setup and you can run your server locally through the command:

  ```python manage.py runserver```


* Testing

  There are several unit tests written for this project. All of them is located on ```work-at-olist/api/views/test```. To run this tests, access the root directory of the project and execute:

  ```python manage.py test api/views/```

  at the time of this documentation, there was 77 unit tests covering all the API endpoints.

* Work Enviroment

  This project was developed in a MacBook with the following specs:

  * Model: MacBook Pro Retina 13-inch
  * Processor: Intel Core i5 2,7 GHz
  * Memory: 8 Gb
  * O.S.: macOS High Sierra

  The software specifications of this project are:

  * Programming Language: Python 3.6.5
  * Frameworks: 
    * Django 2.1.1
    * Django Rest Framework 3.8.2
  * Database: PostgreSQL
  * IDE: Sublime Text 3.1.1


* Production

  The application is hosted on a Heroku instance and can be accessed through the link: https://dbrevesf-olist-production.herokuapp.com/

  The Django Framework provides an administrator interface that could help you to create, remove, update or delete some database entries. To access it: https://dbrevesf-olist-production.herokuapp.com/admin

  Besides the admin page, you can also access the API interface. It's a helpful interface, generated by the Django Rest Framework, to handle REST APIs with ease. For access it: https://dbrevesf-olist-production.herokuapp.com/api


## API Documentation

To start the API documentation, it's important to explain how the system was designed. Our application have 4 models: Call, CallDetail, PriceRule and PriceRuleDetail. 

### Call (id, source, destination)

This model represents every single call between two numbers: source and destination. Everytime someone make a call, a new object from Call is created. 

### CallDetail (id, call_id, start, timestamp)

Every Call is composed of two CallDetail objects. The ```start``` value is a boolean and if it's ```True```, then it's when the call started and if it's ```False```, it's when the call ended. It's forbidden to assign two CallDetail with the same start value and with the same timestamp value. 

### PriceRule (id, created_date) 

This model represents a new price rule. The value of ```created_date``` informs when the rule was created. It's important because we can have a lot of price rules through the time but we have to guarantee that a Call made in the past won't have its bill value changed. So, this model helps us to keep track of the price rules so we can calculate past bills without save them in the database.

### PriceRuleDetails(id, price_id, standing_charge, call_charge, start, end)

Every PriceRule is composed of many PriceRuleDetails. Every PriceRuleDetail can cover a period of time and apply variable charges per minute (call_charge) and fixed charge by call (standing_charge). To compute a bill, we need to look for the PriceRuleDetail that fits the period of time of the calls. 

### Endpoints

Now That we already learnt about the models, we can describe the API endpoints:

**/api/call**

* ```GET /api/call/```: get the list of all the calls

  *HTTP 200 OK*

  ```json
  [
      {
          "id": 8,
          "source": "99988526423",
          "destination": "9993468278"
      },
      {
          "id": 9,
          "source": "99988526423",
          "destination": "9993468278"
      }
  ]
  ```

* ```GET /api/call/<id>```: get the call if it exists

  *HTTP 200 OK*

  ```json
  {
      "id": 8,
      "source": "99988526423",
      "destination": "9993468278"
  }
  ```

  *HTTP 404 NOT FOUND*

  ```json
  {
    "detail": "Not Found"
  }
  ```

* ```POST /api/call/```: create a new call

  *HTTP 201 CREATED*

  ```json
  {
      "id": 8,
      "source": "99988526423",
      "destination": "9993468278"
  }
  ```





