# Flask Project
This is a basic Flask application to write/view blogs.

### Why Flask?
- Flask is a lightweight web framework for Python, designed to help developers build web applications quickly and with minimal overhead. 
  
- It's known as a "micro-framework" because it provides the essentials to get started with web development while giving you the flexibility to add more components as needed.

#### Advantages of flask
- Lightweight and flexible
- Simplicity
- Modular
- Jinja2 Templating
- Extensible


#### Prerequisites
- Python
- pip (Python Package Installer)

## Installation
- Clone the repository
  ```
  git clone https://github.com/a-anuj/flask-projects.git
  ```
- Create the virtual environment
  ```
  venv\Scripts\activate
  ```
- Install the required packages
  ```
  pip install -r requirements.txt
  ```
- To Start the application
  ```
  flask run
  ```

### Setting up the database
- I have used MySQL database to store all the information.
  
- MySQL is a reliable, open-source relational database management system known for its high performance and ease of use.

- Create a MySQL database
  ```
  CREATE DATABASE your_database_name;
  ```
  or Use the create_db python file.

- Update the database configuration in app.py:
  ```
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/your_database_name'
  ```

- In the Python Shell
  ```
  from app import db
  db.create_all()
  ```

### Setting up the migrations
- Initialize Flask-Migrate
    ```
    flask db init
    ```
- Create a migration
  ```
  flask db migrate -m "Details about migration"
  ```
- Applying the migration
  ```
  flask db upgrade
  ```

