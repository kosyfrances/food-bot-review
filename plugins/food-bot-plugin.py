import psycopg2
import datetime

crontable = []
outputs = []


class CustomSQL(object):
    def __init__(self):
        self.cursor = ""
        self.conn = ""

    def connect(self):
        conn_string = "host='localhost' dbname='food_bot'"

        print "Connecting to database\n ->%s" % (conn_string)

        self.conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object
        # you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        print "Connected!\n"

    def disconnect(self):
        print "Closing connection!\n"
        self.conn.close()

    # def command(self, query_string):
    #     self.connect()
    #     self.cursor.execute(query_string)
    #     self.cursor.execute('commit')
    #     self.disconnect()

    def query(self, query_string, variables):
        self.connect()
        self.cursor.execute(query_string, variables)
        result = []
        for row in self.cursor:
            result.append(row)

        self.disconnect()
        print result
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
                        "\n`menu [day of week]` - Get the menu for any day."
                        "\n"
                        "\n`rate [meal] [option] [rating]`- Rate today's meal."
                        "\n`Example: rate lunch A 10`"
                        "\n Type `menu` to get the meal options."
                        "\n"
                        "\n`comment [meal] [option] [comment]` - Tell me about the meal today."
                        "\n `Example: comment breakfast B I enjoyed the meal.`"
                        "\n Type `menu` to get the meal options."
                        "\n"
                        "\n`get ratings` - Get the average food rating"
                        ])

    elif buff[0].lower() == 'menu':
        show_menu(channel, buff)

    elif buff[0].lower() == 'rate':
        print "rate was called"
        # rate(channel, buff, user_id)

    elif buff[0].lower() == 'comment':
        print "comment was called"
        # enter_comment(channel, buff)

    elif buff[0].lower() == 'get rating':
        print "get rating was called"
        # get_average_ratings(channel)

    else:
        outputs.append([channel, "Wrong command yo! Type `help` to get `HELP`"])


def week_day(day):
    week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                 'saturday', 'sunday']
    return week_days[day]

def show_menu(channel, buff):
    if len(buff) == 1:
        int_day = datetime.datetime.today().weekday()
        day = week_day(int_day)

    if len(buff) > 1:
        day = buff[1].lower()
        if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                       'saturday', 'sunday']:
            outputs.append([channel, "Hey, this is not a valid day of the week."])
            return

    if day.lower() in ['saturday', 'sunday']:
        outputs.append([channel, "Sorry hungry person, No weekend meals.Use the vending machine. :stuck_out_tongue_winking_eye:"])
        return

    sql = CustomSQL()
    query_string = "SELECT food, meal, option FROM food_menu WHERE day = (%s)"
    variables = (day,)
    menu = sql.query(query_string, variables)

    if menu:
        response = ""
        for meal in menu:
            response = response + str(meal[0]) + '\t' + str(meal[1]) + '\t'+ str(meal[2]) + '\t' + str(meal[3]) + '\n'

        print response

        outputs.append([channel, str(response)])

# def check_meal_option(meal, option, channel):
#     if meal.lower() != 'breakfast' and meal.lower() != 'lunch':
#         outputs.append([channel, "Sorry, valid meal selections are `breakfast` and `lunch` only. :)"])

#     elif option.lower() != 'a' and option.lower() != 'b':
#         outputs.append([channel, "Sorry, valid option selections are `A` and `B` only. :)"])

# def rate(channel, buff, user_id):
#     meal = buff[1]
#     option = buff[2]
#     rating = buff[3]

#     day_of_week = day_of_week_to_string(datetime.datetime.today().weekday())

#     #Get food menu id
#     query_string = 'SELECT id_food_menu FROM food_bot_schema.food_menu where meal = "' + meal + '" and food_menu.meal_option = "' + option.upper() + '" and day_of_week = "' + day_of_week + '"'
#     sql = CustomSQL()
#     food_menu_id = sql.query(query_string)[0][0]

#     check_meal_option(meal, option, channel)

#     if str(rating).isdigit():
#         query_string = 'insert into ratings (rating, comment, id_users, id_food_menu, date_served) values (' + str(rating) + ', NULL, "' + str(user_id) + '", ' + str(food_menu_id) + ', sysdate() )'
#         sql.command(query_string)
#         outputs.append([channel, "You have rated for this meal."])
#     else:
#         outputs.append([channel, "Your rating must be a number. Type `help` to get help."])

# def enter_comment(channel, buff):
#     meal = buff[1]
#     option = buff[2]
#     comment = buff[3:]

#     check_meal_option(meal, option, channel)

#     str_comment = ""

#     for i in comment:
#         str_comment = str_comment + i + ' '

#     str_comment = str_comment.rstrip(' ')

#     outputs.append([channel, "Code functionality in progress. Your comment is: " + str_comment])

# def get_average_ratings(channel):
#     outputs.append([channel, "Get average rating was called...Code functionality in progress"])

