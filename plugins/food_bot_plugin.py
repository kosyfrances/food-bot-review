from custom_sql import CustomSQL
from mako.template import Template

# crontable = []
outputs = []


def send_response(template_name, channel, context=None):
    import os

    context = context or {}
    template_path = os.path.join('templates', template_name) + '.txt'
    template = Template(filename=template_path)
    rendered_template = template.render(**context)
    outputs.append([channel, rendered_template])
    return rendered_template


def process_message(data):
    if data['channel'].startswith("D"):
        if 'subtype' in data:
            return

        channel = data['channel']
        buff = str(data['text']).split(' ')
        user_id = data['user']
        text_buffer = buff[0].lower()

        if 'reply_to' in data and data['reply_to'] is None:
            return

        elif text_buffer == 'help':
            Response.show_help(channel)

        elif text_buffer == 'menu':
            Response.show_menu(channel, buff)

        elif text_buffer == 'rate':
            Response.rate(channel, buff, user_id)

        elif text_buffer == 'comment':
            Response.enter_comment(channel, buff)

        elif text_buffer == 'get-rating':
            Response.get_average_ratings(channel)

        else:
            Response.show_error(channel)


def get_day_of_week():
    import datetime
    return datetime.datetime.now().strftime('%A').lower()


class Response:

    @staticmethod
    def show_help(channel):
        return send_response('help_response', channel)

    @staticmethod
    def convert_menu_list_to_dict(menu):
        menu_dict = {}
        for meal in menu:
            food = meal[0]
            mealtime = meal[1]
            option = meal[2]
            if mealtime not in menu_dict:
                menu_dict[mealtime] = {}
            assert (option not in menu_dict[mealtime])
            menu_dict[mealtime][option] = food
        return menu_dict

    @staticmethod
    def show_menu(channel, buff):
        import datetime
        if len(buff) == 1:
            day = get_day_of_week()

        if len(buff) > 1:
            day = buff[1].lower()

        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            sql = CustomSQL()
            week = (datetime.datetime.now().isocalendar()[1] % 2) + 1

            # if week == 0:
            #     week = 2

            variables = (day, str(week),)
            query_string = "SELECT food, meal, option FROM menu_table WHERE day = (%s) AND week = (%s)"
            menu = sql.query(query_string, variables)

            if menu:
                menu_dict = Response.convert_menu_list_to_dict(menu)
                send_response('menu_response', channel, {'menu': menu_dict})

        elif day in ['saturday', 'sunday']:
            send_response('weekend_meal_error', channel)

        else:
            send_response('invalid_day_error', channel)


    # def check_meal_option(meal, option, channel):
    #     if meal.lower() != 'breakfast' and meal.lower() != 'lunch':
    #         outputs.append([channel, "Sorry, valid meal selections are `breakfast` and `lunch` only. :)"])

    #     elif option.lower() != 'a' and option.lower() != 'b':
    #         outputs.append([channel, "Sorry, valid option selections are `A` and `B` only. :)"])

    @staticmethod
    def rate(channel, buff, user_id):
        print "Rate functionality in progress"
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

    @staticmethod
    def enter_comment(channel, buff):
        print "Comment functionality in progress"
    #     meal = buff[1]
    #     option = buff[2]
    #     comment = buff[3:]

    #     check_meal_option(meal, option, channel)

    #     str_comment = ""

    #     for i in comment:
    #         str_comment = str_comment + i + ' '

    #     str_comment = str_comment.rstrip(' ')

    #     outputs.append([channel, "Code functionality in progress. Your comment is: " + str_comment])

    @staticmethod
    def get_average_ratings(channel):
        print "Get average ratings functionality in progress"
    #     outputs.append([channel, "Get average rating was called...Code functionality in progress"])

    @staticmethod
    def show_error(channel):
        send_response('wrong_command', channel)
