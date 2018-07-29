# FullStack_Info_FinalProject
Final Project for INFo 290T Full-Stack Web Development at UC Berkeley in Spring 2018

## How to Contribute

To contribute select an issue from the [Project Board](https://github.com/FroeMic/FullStack_Info_FinalProject/projects/1), assign it to yourself and get going.

Be sure to follow the **Gitflow** (our branching model) while doing so. You can find a [Step-by-Step Guide](https://share.nuclino.com/p/GitFlow-How-To-Bf6rSHUFJdB7PUpgRi_uxU) on Nuclino. If still in doubt, just ask on Slack.

## Initial Setup

After **initially cloning** the repository make sure that

1. All the dependecies in `requirements.txt` are installed. You can install them by running `pip install -r requirements.txt`.
2. You created and configured the dotenv file (`.env`). Just copy and rename the `.env.example`.
3. You created the database. In your terminal navigate to this folder and run `python` to bring up the python interactive shell. Then run the following three commands: `import app`, then `app.create_database()` and finally `exit()`.
4. You seeded the database. Navigate to `/resources/scripts/import_books` and follow the instructions to seed the database you just created.
5. Now run `python run.py` to start up the server. It will automatically check whether Jobs for synchronyzing the local database against the goodreads and amazon APIs exist and create them if not so. If you want to run the jobs immediately (it still takes time, since it is done book after book) stop the server and bring up the python interactive shell. Then run the following three commands: `import app`, then `app.run_sync_jobs()` and finally `exit()`.

## Folder Structure

```
|— requirements.txt     (all the required python packages)
|— .env                 (store environment variables that should not end up on github)
|— config.py            (loads variables from .env)
|— run.py               (runs the flask server)
|— resources/           (resources related to the development)
|— app/                     
    |— data/            (user generated data. Not pushed to github.)
    |— forms/           (all forms)
    |— models/          (all SQLAlchemy models)
    |— static/          (static files i.e. css, js, images)
    |- tasks/           (asynchronous background jobs)
    |— templates/       (Jinja2 templates)
    |— utils/           (additional functions such as custom decorators)
    |— __init__.py      
    |— routes.py        (the routes of our app (formerly views.py) )  
```
