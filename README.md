# Reddit API Clone

A Reddit API Clone built using Django and Django REST Framework (DRF).

## Technology Stack

![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=brightgreen) ![image](https://img.shields.io/badge/Django%20Rest%20Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)


## Features
- User
    - Authentication
        - Signup / Login / Password Change / Password Reset
    - can get any user by username
    - can change username after every 14 days from last changed date
- Subreddit
    - create (Name Must be unique)
    - can be deleted only by the owner
    - users can join subreddit
    - Moderators
        - can ban users from joining / interacting with the subreddit
    - about, description, links
    - can have pinned posts/comments
    - comments can be locked by default
- Posts
    - user can create posts in any subreddit (only if they have joined the subreddit)
    - only text post supported for now
    - Moderators
        - can update/delete user posts
        - can lock posts to prevent further interaction
            - post cant be updated when locked
- Comments
    - user can comment on a post (no need to join the subreddit)
    - comments can be nested indefinitely
    - comments can be locked (no child comment can be added/edited)


## Installation & Setup

### Clone the Repo
- `git clone https://github.com/wh0th3h3llam1/reddit-api.git`

### Create a virtual environment using `venv`
- `python -m venv reddit-api`

### Install the requirements
- `pip install -r requirements.txt`

### Migrate the database
- `python manage.py migrate`

### Create Super User
- `python manage.py createsuperuser`

### Run Server
- `python manage.py runserver`

> Server should be live at `127.0.0.1:8000`


## Licence
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=for-the-badge&logo=appveyor)](https://opensource.org/licenses/MIT)
