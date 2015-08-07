import datetime
import mysql.connector
crontable = []
outputs = []

class CustomSQL(object):
    def __init__(self):
        self.cnx = ""
        self.cursor = ""

    def connect(self):
        self.cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='food_bot_schema')
        self.cursor = self.cnx.cursor()

    def disconnect(self):
        self.cursor.close()
        self.cnx.close()

    def command(self, query_string):
        self.connect()
        self.cursor.execute(query_string)
        self.cursor.execute('commit')
        self.disconnect()

    def query(self, query_string):
        self.connect()
        self.cursor.execute(query_string)

        result = []
        for row in self.cursor:
            result.append(row)

        self.disconnect()
        return result

def process_message(data):
    channel = data['channel']
    buff = str(data['text']).split(' ')
    user_id = data['user']

    if buff[0].lower() == 'help':
        outputs.append([channel, "`help` - Shows this screen."
                                "\n"
                                "\n`menu` - Get the menu for today."
                                "\n"
                                "\n`menu [day of week]` - Get the menu for a specific week day."
                                 "\n"
                                "\n`rate [meal] [option] [rating]` - Rate today's meal. "
                                "\n`Example: rate lunch A 10`"
                                "\n Type `menu` to get the meal options for the one you want to rate."
                                "\n"
                                "\n`comment [meal] [option] [comment]` - Tell me what you think about the meal today."
                                "\n `Example: comment breakfast B The food was tasty. I enjoyed it`"
                                "\n Type `menu` to get the meal options for the one you want to comment on."
                                "\n"
                                "\n`get ratings` - Get the average food rating and number of reviewers today"
                        ])

    elif buff[0].lower() == 'menu':
        show_menu(channel, buff)

    elif buff[0].lower() == 'rate':
        rate(channel, buff, user_id)

    elif buff[0].lower() == 'comment':
        enter_comment(channel, buff)

    elif buff[0].lower() == 'get rating':
        get_average_ratings(channel)

    else:
        outputs.append([channel, "Sorry, I do not understand this command. Type `help` to get `HELP`"])

    # except:
    #     outputs.append([channel, "Sorry, I do not understand this command. Type `help` to get `HELP`"])

def day_of_week_to_string(int_day_of_week):
    if int_day_of_week == 0:
        day_of_week = 'Monday'
    elif int_day_of_week == 1:
        day_of_week = 'Tuesday'
    elif int_day_of_week == 2:
        day_of_week = 'Wednesday'
    elif int_day_of_week == 3:
        day_of_week = 'Thursday'
    elif int_day_of_week == 4:
        day_of_week = 'Friday'
    elif int_day_of_week == 5:
        day_of_week = 'Saturday'
    elif int_day_of_week == 6:
        day_of_week = 'Sunday'
    return day_of_week


def show_menu(channel, buff):
    if len(buff) == 1:
        int_day_of_week = datetime.datetime.today().weekday()
        day_of_week = day_of_week_to_string(int_day_of_week)

    if len(buff) > 1:
        day_of_week = buff[1].title()

    if day_of_week == 'Saturday' or day_of_week == 'Sunday':
        outputs.append([channel, "Sorry hungry fellow, No menu for weekends."])
        return

    sql = CustomSQL()
    query_string =  "select day_of_week, meal, meal_option, meal_items from food_menu where day_of_week = '" + day_of_week + "'"
    menu = sql.query(query_string)

    if menu:
        response = ""
        for meal in menu:
            response = response + str(meal[0]) + '\t' + str(meal[1]) + '\t' + str(meal[2]) + '\t' + str(meal[3]) + '\n'

        outputs.append([channel, str(response)])
        return
    else:
        outputs.append([channel, "Hey, this is not a valid day of the week."])

def check_meal_option(meal, option, channel):
    if meal.lower() != 'breakfast' and meal.lower() != 'lunch':
        outputs.append([channel, "Sorry, valid meal selections are `breakfast` and `lunch` only. :)"])

    elif option.lower() != 'a' and option.lower() != 'b':
        outputs.append([channel, "Sorry, valid option selections are `A` and `B` only. :)"])

def rate(channel, buff, user_id):
    meal = buff[1]
    option = buff[2]
    rating = buff[3]

    day_of_week = day_of_week_to_string(datetime.datetime.today().weekday())

    #Get food menu id
    query_string = 'SELECT id_food_menu FROM food_bot_schema.food_menu where meal = "' + meal + '" and food_menu.meal_option = "' + option.upper() + '" and day_of_week = "' + day_of_week + '"'
    sql = CustomSQL()
    food_menu_id = sql.query(query_string)[0][0]

    check_meal_option(meal, option, channel)

    if str(rating).isdigit():
        query_string = 'insert into ratings (rating, comment, id_users, id_food_menu, date_served) values (' + str(rating) + ', NULL, "' + str(user_id) + '", ' + str(food_menu_id) + ', sysdate() )'
        sql.command(query_string)
        outputs.append([channel, "You have rated for this meal."])
    else:
        outputs.append([channel, "Your rating must be a number. Type `help` to get help."])

def enter_comment(channel, buff):
    meal = buff[1]
    option = buff[2]
    comment = buff[3:]

    check_meal_option(meal, option, channel)

    str_comment = ""

    for i in comment:
        str_comment = str_comment + i + ' '

    str_comment = str_comment.rstrip(' ')

    outputs.append([channel, "Code functionality in progress. Your comment is: " + str_comment])

def get_average_ratings(channel):
    outputs.append([channel, "Get average rating was called...Code functionality in progress"])

