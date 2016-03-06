[![Coverage Status](https://coveralls.io/repos/andela-kanyanwu/food-bot-review/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-kanyanwu/food-bot-review?branch=master)
# Food-bot-review

Food-bot is used for getting real-time feedback about meals served within the Andela community. It also lets you know which meal will be served when you want it to.

### Tech
Food-bot is a Slack bot written in python that connects via the RTM API. It was built upon Python-rtmbot, a callback based bot engine cloned from https://github.com/slackhq/python-rtmbot.

### Collaboration

Want to contribute? Great!

You need to have postgreSQL installed and set up on your machine. You also need python, and a virtual environment set up.

Clone the repository from [GitHub](https://www.github.com)
```
git clone https://github.com/andela-kanyanwu/food-bot-review.git
```

### Installation

In your virtual environment, install everything in the requirements.txt file

```
pip install -r requirements.txt
```

**create a `.env.yml` file and add it to your root file, have the following config in the .env.yml file.**

__.env.yml format:__

```
    SECRET_KEY:
      'some-random-crazy-value'
    DEBUG:
      'True'
```

## Database

On your terminal,
```
createdb food_bot
```
You can use PgAdmin or its alternative to create the database.

*Run the following command to create the tables*
```
python django_foodbot/manage.py migrate
```

### Populate your local database with foodbot data.

*Run the following command to populate your local database with data from the fixtures*
```
python django_foodbot/manage.py loaddata initial_data.json
```

## Set up your environment to test the bot locally
*Ask any of the collaborators for a slack bot api key. You will also be added to the food-review slack organisation where you can test foodbot while working.*

Follow these processes to configure the bot and run locally:

On your terminal,
```
cp doc/example-config/rtmbot.conf .
```
```
vi rtmbot.conf
```
```
DEBUG: True
SLACK_TOKEN: "xoxb-11111111111-222222222222222"
ENVIRONMENT: 'local'
DAEMON: False
```
Be sure to replace the _SLACK_TOKEN_ in the rtmbot.conf file with the one from the bot you created.

### Start the bot

You will need to always restart the bot as the server does not automatically detect any change.

```
./rtmbot.py
```
### Development
- *Checkout* to a new branch from master when working on any task.
```
$(master) git checkout -b FEATURE_BRANCH
#=> Switched to a new branch 'FEATURE_BRANCH'
```
- The first time you perform a push, use the following syntax to set up your local branch to track the remote:
```
git push --set-upstream origin FEATURE_BRANCH
```

### Pull requests and code reviews
- Fetch the changes from the remote and rebase your feature branch on top of the remote master
```
$(FEATURE_BRANCH): git fetch
$(FEATURE_BRANCH): git rebase origin/master
```
- If everything is fine and there haven't been any commit yet:
```
$(FEATURE_BRANCH): git push
```
- You will need to git push --force if the rebase rewrote any commit but first confirm with *git status* that you are on the correct branch.
- Create pull request against the STAGING branch when you are done for code review.
- After review, your code reviewer will merge your branch to staging branch. *meal-bot* on the food-review slack is tied to the staging branch.  If everything works fine on *meal-bot*, your branch will be deleted and the staging branch will be merged to master.
- Please note that the master branch is tied to *food_bot* on Andela slack. Do not push or merge to master until you are sure *meal-bot* on the food-review slack has no issues.
