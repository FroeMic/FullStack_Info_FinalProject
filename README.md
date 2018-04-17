# FullStack_Info_FinalProject
Final Project for InfoC265 at UC Berkeley in Spring 2018

## How to Contribute

To contribute select an issue from the [Project Board](https://github.com/FroeMic/FullStack_Info_FinalProject/projects/1), assign it to yourself and get going.

Be sure to follow the **Gitflow** (our branching model) while doing so. You can find a [Step-by-Step Guide](https://share.nuclino.com/p/GitFlow-How-To-Bf6rSHUFJdB7PUpgRi_uxU) on Nuclino. If still in doubt, just ask on Slack.

## Initial Setup

After **initially cloning** the repository make sure that

1. All the dependecies in `requirements.txt` are installed. You can install them by running `pip install -r requirements.txt`.
2. You created and configured the dotenv file (`.env`). Just copy and rename the `.env.example`.
3. You created the database. In your terminal navigate to this folder and run `python` to bring up the python interactive shell. Then run the following three commands: `import app`, then `app._create_database()` and finally `exit()`.

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
