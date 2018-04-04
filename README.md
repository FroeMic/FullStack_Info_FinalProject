# FullStack_Info_FinalProject
Final Project for InfoC265 at UC Berkeley in Spring 2018

## How to Contribute

To contribute select an issue from the [Project Board](https://github.com/FroeMic/FullStack_Info_FinalProject/projects/1), assign it to yourself and get going.

Be sure to follow the **Gitflow** (our branching model) while doing so. You can find a [Step-by-Step Guide](https://share.nuclino.com/p/GitFlow-How-To-Bf6rSHUFJdB7PUpgRi_uxU) on Nuclino. If still in doubt, just ask on Slack.



## Folder Structure

```
|— requirements.txt     (all the required python packages)
|— .env                 (store environment variables that should not end up on github)
|— config.py            (loads variables from .env)
|— run.py               (runs the flask server)
|— app/                     
    |— data/            (user generated data. Not pushed to github.)
    |— forms/           (all forms)
    |— models/          (all SQLAlchemy models)
    |— static/          (static files i.e. css, js, images)
    |— templates/       (Jinja2 templates)
    |— utils/           (additional functions such as custom decorators)
    |— __init__.py      
    |— routes.py        (the routes of our app (formerly views.py) )

```