import datetime
from mako.template import Template
from custom_sql import CustomSQL

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

        elif text_buffer == 'get-rating':
            Response.get_average_ratings(channel)

        else:
            Response.show_error(channel)


def get_day_of_week():
    return datetime.datetime.now().strftime('%A').lower()


def get_date():
    return datetime.datetime.now().strftime("%A %b %d %Y")


def get_week_number():
    week = (datetime.datetime.now().isocalendar()[1] % 2) + 1
    # fall back code here
    # if week == 0:
    #     week = 2
    return week


def check_meal_selected(meal):
    if meal.lower() != 'breakfast' and meal.lower() != 'lunch':
        return {'bool': False}
    else:
        return {'bool': True }

def check_option_selected(option, day, week, meal):
    variables = (meal, day, week,)
    sql = CustomSQL()

    query_string = "SELECT count(option) FROM menu_table WHERE meal = (%s) AND day = (%s) AND week = (%s)"
    option_count_sql = sql.query(query_string, variables)
    option_count = int(option_count_sql[0][0])

    try:
        if int(option) > option_count:
            return {'bool': False, 'option': option_count}
    except ValueError:
        return {'bool': False, 'option': option_count}
    else:
        return {'bool': True }

def check_rating(rating_val):
    try:
        rating = int(rating_val)
        if rating not in range(1, 6):
            return {'bool': False}
        else:
            return {'bool': True }
    except ValueError:
        return {'bool': False}



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
    def get_menu_template_context(buff):
        """
        return the template name and correct context
        """
        if len(buff) == 1:
            day = get_day_of_week()

        if len(buff) > 1:
            day = buff[1].lower()

        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            sql = CustomSQL()
            week = get_week_number()

            variables = (day, week,)
            query_string = "SELECT food, meal, option FROM menu_table WHERE day = (%s) AND week = (%s)"
            menu = sql.query(query_string, variables)

            if menu:
                menu_dict = Response.convert_menu_list_to_dict(menu)
                return {'template': 'menu_response',
                        'context': {'menu': menu_dict}}

        elif day in ['saturday', 'sunday']:
            return {'template': 'weekend_meal_error', 'context': {}}

        else:
            return {'template': 'invalid_day_error', 'context': {}}

    @staticmethod
    def show_menu(channel, buff):
        show_menu_dict = Response.get_menu_template_context(buff)
        send_response(show_menu_dict['template'], channel,
                      show_menu_dict['context'])

    @staticmethod
    def get_rate_template_context(buff, user_id):
        # day = get_day_of_week()
        day = 'monday'
        week = get_week_number()
        # if day in ['saturday', 'sunday']:
        #     send_response('weekend_meal_error', channel)
        # else:
        meal = buff[1]
        option = buff[2]
        rating = buff[3]
        comment = " ".join(buff[4:]) or "no comment"

        check_option = check_option_selected(option, day, week, meal)

        if check_meal_selected(meal)['bool'] is False:
            return {'template': 'invalid_meal', 'context': {}}

        if check_option['bool'] is False:
            return {'template': 'invalid_option', 'context': {'option_count': check_option['option']}}

        if check_rating(rating)['bool'] is False:
            return {'template': 'invalid_rating', 'context': {}}

        variables = (meal, 'tuesday', week, option,)
        sql = CustomSQL()
        query_string = "SELECT id FROM menu_table WHERE meal = (%s) AND day = (%s) AND week = (%s) AND option = (%s) "
        result = sql.query(query_string, variables)
        food_menu_id = int(result[0][0])

        variables = (datetime.date(2005, 11, 18), user_id, food_menu_id, rating, comment)
        query_string = "INSERT INTO rating (date, user_id, menu_id, rate, comment) VALUES (%s, %s, %s, %s, %s)"
        sql.command(query_string, variables)
        return {'template': 'rating_response', 'context': {}}


    @staticmethod
    def rate(channel, buff, user_id):
        rate_context_dict = Response.get_rate_template_context(buff, user_id)
        send_response(rate_context_dict ['template'], channel, rate_context_dict['context'])

    @staticmethod
    def get_average_ratings(channel):
        print "Get average ratings functionality in progress"
    #     outputs.append([channel, "Get average rating was called...Code functionality in progress"])

    @staticmethod
    def show_error(channel):
        send_response('wrong_command', channel)
