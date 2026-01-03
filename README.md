# Team Jet-6 Small Group project

## Team members
The members of the team are:
- Sabah Abdullah Abdulkarem Al-Aswadi
- Moyondafoluwa Bliss Modupe Akinwande
- Aniekan Essen-Kolo
- *enter full name 4 here*
- *enter full name 5 here (or delete if not applicable)*

## Project structure
The project is called `recipify`.  It currently consists of a single app `recipes`.

## Deployed version of the application
The deployed version of the application can be found at [recipifyjet6.pythonanywhere.com](https://recipifyjet6.pythonanywhere.com).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  The project source code has been developed using Python 3.12, so you are recommended to use the same version.  From the root of the project:

```
$ python3.12 -m venv venv
$ source venv/bin/activate
```

If your system does not have `python3.12` installed and you are unable to install Python 3.12 as a version you can explicitly refer to from the CLI, then replace `python3.12` by `python3` or `python`, provide this employs a relatively recent version of Python.

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

This will create sample data and a superuser account for admin access.

Run all tests with:
```
$ python3 manage.py test
```

## Admin Access

For testing the admin panel and moderation features, a superuser account is automatically created when running the `seed` command:

**Admin Credentials:**
- Username: `admin`
- Password: `admin123`

Access the admin panel at: `http://localhost:8000/admin/`

**Admin Features:**
- View and manage all users, recipes, and comments
- Review and handle user-submitted reports
- Moderate content (hide/delete recipes and comments)
- Send warnings to users
- View notifications and system activity

**Note:** These credentials are for development and testing only. In production, create a secure admin account using:
```
$ python3 manage.py createsuperuser
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

ChatGPT was used for seeding, specifically to generate the data fixtures in `recipes/management/RecipeFixtures`