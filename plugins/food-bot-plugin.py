import time
crontable = []
outputs = []

def process_message(data):
    channel = data['channel']
    buff = str(data['text']).split(' ')

    if buff[0].lower() == 'help':
        outputs.append([channel, "`help` - Shows this screen."
                                "\n"
                                "\n`menu` - Get the menu for today."
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
        show_menu(channel)

    elif buff[0].lower() == 'rate':
        rate(channel, buff)

    elif buff[0].lower() == 'comment':
        enter_comment(channel, buff)

    elif buff[0].lower() == 'get rating':
        get_average_ratings(channel)

    else:
        outputs.append([channel, "Sorry, I do not understand this command. Type `help` to get `HELP`"])


def show_menu(channel):
    outputs.append([channel, "Show menu was called...Code functionality in progress"])

def check_meal_option(meal, option, channel):
    if meal.lower() != 'breakfast' and meal.lower() != 'lunch':
        outputs.append([channel, "Sorry, valid meal selections are `breakfast` and `lunch` only. :)"])

    elif option.lower() != 'a' and option.lower() != 'b':
        outputs.append([channel, "Sorry, valid option selections are `A` and `B` only. :)"])

def rate(channel, buff):
    meal = buff[1]
    option = buff[2]
    rating = buff[3]

    check_meal_option(meal, option, channel)

    if str(rating).isdigit():
        outputs.append([channel, "You have rated for this meal."])

    outputs.append([channel, "Rate was called...Code functionality in progress"])

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