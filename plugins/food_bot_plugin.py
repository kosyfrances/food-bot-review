from datetime import datetime
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
    if data['channel'].startswith('D'):
        if 'subtype' in data:
            return

        channel = data['channel']
        buff = data['text'].encode('ascii', 'ignore').split(' ')
        user_id = data['user']
        text_buffer = buff[0].lower()

        if 'reply_to' in data and data['reply_to'] is None:
            return

        elif text_buffer == 'help' and len(buff) == 1:
            Response.show_help(channel)

        elif text_buffer == 'menu':
            Response.show_menu(channel, buff)

        elif text_buffer == 'rate' and len(buff) > 3:
            Response.rate(channel, buff, user_id)

        else:
            Response.show_error(channel)


class Helper:
    """
    Contains helper functions for validation and and sending the right context
    """
    @staticmethod
    def get_day_of_week():
        return datetime.now().strftime('%A').lower()

    @staticmethod
    def get_date():
        return datetime.now()

    @staticmethod
    def get_week_number():
        from config import Config
        config = Config()

        week = (datetime.now().isocalendar()[1] % 2)
        config_week = config['WEEK']

        if config_week == 'A':
            if week == 0:
                week = 2

        # fall back code here when the week switches
        if config_week == 'B':
            week += 1

        return week

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
        return the template name and correct context for menu
        """
        if len(buff) == 1:
            day = Helper.get_day_of_week()

        if len(buff) > 1:
            day = buff[1].lower()

        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            sql = CustomSQL()
            week = Helper.get_week_number()

            variables = (day, week,)
            query_string = 'SELECT food, meal, option FROM menu_table WHERE day = (%s) AND week = (%s)'
            menu = sql.query(query_string, variables)

            if menu:
                menu_dict = Helper.convert_menu_list_to_dict(menu)
                return {'template': 'menu_response',
                        'context': {'menu': menu_dict, 'day': day}}

        elif day in ['saturday', 'sunday']:
            return {'template': 'weekend_meal_error', 'context': {}}

        else:
            return {'template': 'invalid_day_error', 'context': {}}

    @staticmethod
    def check_meal_selected(meal):
        if meal and isinstance(meal, str):
            if meal.lower() not in ['breakfast', 'lunch']:
                return False
            else:
                return True

    @staticmethod
    def check_option_selected(option, day, week, meal):
        variables = (meal, day, week,)
        sql = CustomSQL()

        query_string = 'SELECT count(option) FROM menu_table WHERE meal = (%s) AND day = (%s) AND week = (%s)'
        option_count_sql = sql.query(query_string, variables)
        option_count = int(option_count_sql[0][0])

        try:
            option_int = int(option)
        except ValueError:
            option_int = 0

        if option_int not in range(1, option_count + 1):
            return {'bool': False, 'option': option_count}
        else:
            return {'bool': True}

    @staticmethod
    def check_rating(rating_val):
        try:
            rating = int(rating_val)
        except ValueError:
            rating = 0

        if rating not in range(1, 6):
            return False
        else:
            return True

    @staticmethod
    def check_multiple_rating(user_id, meal):
        sql = CustomSQL()
        variables = (user_id, meal,)

        query = 'SELECT count(rating.id) FROM rating INNER JOIN menu_table ON menu_table.id = menu_id WHERE rating.user_id = (%s) AND menu_table.meal = (%s) AND rating.created_at::date = now()::date'
        result = sql.query(query, variables)
        if int(result[0][0]) > 0:
            return True

    @staticmethod
    def get_rate_template_context(buff, user_id):
        """
        return the template name and correct context for rating and comment
        """
        day = Helper.get_day_of_week()
        week = Helper.get_week_number()

        if day in ['saturday', 'sunday']:
            return {'template': 'weekend_rate_error', 'context': {}}

        else:
            meal = buff[1]
            option = buff[2]
            rating = buff[3]
            comment = ' '.join(buff[4:]) or 'no comment'

            check_option = Helper.check_option_selected(option, day, week,
                                                        meal)

            if not Helper.check_meal_selected(meal):
                return {'template': 'invalid_meal', 'context': {}}

            if not check_option['bool']:
                return {'template': 'invalid_option',
                        'context': {'option_count': check_option['option']}}

            if not Helper.check_rating(rating):
                return {'template': 'invalid_rating', 'context': {}}

            if Helper.check_multiple_rating(user_id, meal):
                return {'template': 'multiple_rating', 'context': {}}

            variables = (meal, day, week, option,)
            sql = CustomSQL()
            query_string = 'SELECT id FROM menu_table WHERE meal = (%s) AND day = (%s) AND week = (%s) AND option = (%s)'
            result = sql.query(query_string, variables)
            food_menu_id = int(result[0][0])
            get_date = Helper.get_date()
            variables = (user_id, food_menu_id, rating, comment, get_date,)
            query_string = "INSERT INTO rating (user_id, menu_id, rate, comment, created_at) VALUES (%s, %s, %s, %s, %s)"
            sql.command(query_string, variables)
            return {'template': 'rating_response', 'context': {}}


class Response:

    @staticmethod
    def show_help(channel):
        return send_response('help_response', channel)

    @staticmethod
    def show_menu(channel, buff):
        show_menu_dict = Helper.get_menu_template_context(buff)
        send_response(show_menu_dict['template'], channel,
                      show_menu_dict['context'])

    @staticmethod
    def rate(channel, buff, user_id):
        rate_context_dict = Helper.get_rate_template_context(buff, user_id)
        send_response(rate_context_dict['template'], channel,
                      rate_context_dict['context'])

    @staticmethod
    def show_error(channel):
        send_response('wrong_command', channel)
