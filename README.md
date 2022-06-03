
# HXO recruitment task




## Demo

https://hexocean-task-mr.herokuapp.com 

(only browsable api)

endpoints:

- api/
    - images/
    - images/upload/
    - images/<int:id>/create_temp/
    - images/temporary_links/
    - /auth/login/    -> for auth purposes


dummy users: 
usernames: "Jan" (Enterprise), "Tom" (Premium), "Bob" (Basic), 
password: testpassword123

## Installation

1. Clone this repository and install project dependencies in a virtual enviroment by running
`pip install -r requirements.txt` from project's root directory.

-------
2. Create PostgreSQL database

---------
3. Create .env file and provide the following variables:

`SECRET_KEY`

PostgreSQL database fields:
```
NAME
USER
PASSWORD
PORT
```
-------

4. Run migrations: `python manage.py migrate`
    
## my approach and thoughts

- Subscriptions could be approached in different ways, e.g. using built-in permissions sytem, extending user's model with boolean fields or choice field. I have decided to create a separate model for subscription to handle functionality of creating other configurable subscriptions. This approach however doesn't really contain 'built-in' or hardcoded tiers. I've found this approach the most flexible and easy to use within api. 
- solution of generating thumbnails works well, but django-cleanup doesn't delete them while correlated object is deleted from database due to no model-level relation
- running tests also creates thumbnails, and that is rather unwanted (if some tests fails with errors, collectstatic might be necessary. This happened after heroku configuration)
- I assume that the architecture of temporary links could be done better, my main concern is that TemporaryLink objects doesn't delete themselves automatically - they stop working, but keep existing in database until someone opens their address. This could be handled using e.g. cron scripts
## Feedback

I would deeply appreciate feedback about my solution.

