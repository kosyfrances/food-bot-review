[![Coverage Status](https://coveralls.io/repos/andela-kanyanwu/food-bot-review/badge.svg?branch=feature_coveralls_integration&service=github)](https://coveralls.io/github/andela-kanyanwu/food-bot-review?branch=feature_coveralls_integration)

# Food-bot-review

Food-bot is used for getting real-time feedback about meals served within the Andela community. It also lets you know which meal will be served when you want it to.

### Tech
Food-bot is a Slack bot written in python that connects via the RTM API. It was built upon Python-rtmbot, a callback based bot engine cloned from https://github.com/slackhq/python-rtmbot.

### Collaboration

Want to contribute? Great!

You need to have postgres installed and set up on your machine. You also need python, and a virtual environment set up.

Follow these processes to configure the bot and run locally:

Create a bot on [Slack](https://www.slack.com) that you will use to test whatever you do.

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

**To get the latest food-bot database from heroku stage:**

First we will need to add you as a collaborator.

On your terminal,

**Create a database named food_bot locally:**
```
createdb food_bot
```
**Create tables:**
```
CREATE TABLE menu_table (id SERIAL PRIMARY KEY,
                   day VARCHAR(10) NOT NULL,
                   food VARCHAR(60) NOT NULL,
                   meal VARCHAR(10) NOT NULL,
                   option INT NOT NULL,
                   week INT NOT NULL
                 );

CREATE TABLE rating (id SERIAL PRIMARY KEY,
                    date timestamp without time zone default (now() at time zone 'utc'),
                    user_id VARCHAR(20),
                    menu_id INT REFERENCES menu_table(id),
                    rate INT NOT NULL,
                    comment TEXT
                   );
```
**Download the database backup from heroku:**
```
heroku pg:backups capture --app APPNAME
```
**Be sure to replace APPNAME with the app name of app on staging**

Next,
```
 curl -o latest.dump `heroku pg:backups --app APPNAME public-url`
```
**Restore to local database**
```
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U MYUSER -d food_bot latest.dump
```
**Be sure to replace MYUSER with your postgres username.**

You can click [here](https://devcenter.heroku.com/articles/heroku-postgres-import-export) to read more about importing databases from heroku


**We will work on creating a script that would do the setup automatically for you but for now, please follow these steps and let any of the collaborators know if you have any issues.**

### Database structure
**Database name** - food_bot

**Number of tables** - 2

**Tables** -  meal, rating

Rating has a many to one relationship to Meal via the meal_id.

**Structure of the meal table:**

id | day | food | meal | option | week

**Structure of the rating table:**

id | date | user_id | meal_id | rate | comment

### Installation

In your virtual environment, install everything in the requirements.txt file

```
pip install -r requirements.txt
```

### Start the bot

You will need to always restart the bot as the server does not automatically detect any change.

```
./rtmbot.py
```
### Development
- Checkout to a new branch from master when working on any task.
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
- If everything is fine and there haven't been any commits yet:
```
$(FEATURE_BRANCH): git push
```
- You will need to git push --force if the rebase rewrote any commits, but first confirm with git status that you're on the correct branch.
- Create pull request against the STAGING branch when you are done for code review.
- After review, your code-reviewer will merge your branch to staging branch, and if there are no issues, the pull request will be merged and branch will be deleted.
