from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'imageupload'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


def vars_for_template(player):
    return dict(
        image_path='imageupload/1.jpg'.format(player.round_number)
    )


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage]
