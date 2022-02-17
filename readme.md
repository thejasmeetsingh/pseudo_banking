# Pseudo Banking

Please follow below steps for running the project:

1. Clone or Download the Project from here: https://github.com/thejasmeetsingh/pseudo_banking.git
2. Navigate into the project and install the requirements using: `pip install -r requirements.txt` command. Or create a virtual environment and then install the requirements.
3. Create a PostgresSQL Database on your machine. You can either create a Database using the same credentials given in `.env` file or create a different database and update the database credentials in `.env` file.
4. Run `./manage.py migrate` command. For migrating the model changes into the database.
5. Then, go to "django shell" by running `./manage.py shell` command. After that import the `populate_transactions()` function from `populate_transactions.py` file, Execute the function. It will populate the database with some records for our testing.
6. Then finally, run the server by using this command `./manage runserver` and Test the APIs.

You can use postman collection for testing the APIs. Import the collection from either this link: https://www.getpostman.com/collections/ff8852f55477828bf59f or Just import as JSON from `postman_collection.json` file.
