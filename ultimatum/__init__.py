from otree.api import *

doc = """
The Ultimatum Game (2n players)
First, every player will be randomly paired with another player. In other words, you will 
have a counterpart, but you will not be told who it is. Your identity will also remain
 hidden from your counterpart.

The two participants in a pair will have two different roles: the proposer and the
 responder. You will be assigned randomly to a role, and it will be displayed on the next
 page.

The two of you will together receive 100 points. The experiment is about how to divide 
this amount. The proposer will make the responder a take-it-or-leave-it offer, which the
 responder can accept or reject. If the offer is rejected, both will receive 0 points.
Proposer's role
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'ultimatum/instructions.html'
    # Initial amount allocated to the dictator
    endowment = cu(100)
    offer_choices = currency_range(0, endowment, 10)
    offer_choices_count = len(offer_choices)

    possible_allocations = []
    for offer in offer_choices:
        possible_allocations.append(dict(
            p1_amount=offer,
            p2_amount=endowment - offer
        ))


class Subsession(BaseSubsession):
    pass


def make_strategy_field(number):
    return models.BooleanField(
        label="Would you accept an offer of {}?".format(cu(number)),
        widget=widgets.RadioSelectHorizontal,
        choices=[[False, 'No'], [True, 'Yes']],
    )


class Group(BaseGroup):
    amount_offered = models.CurrencyField(choices=Constants.offer_choices,)
    offer_accepted = models.BooleanField()

    response_0 = make_strategy_field(0)
    response_10 = make_strategy_field(10)
    response_20 = make_strategy_field(20)
    response_30 = make_strategy_field(30)
    response_40 = make_strategy_field(40)
    response_50 = make_strategy_field(50)
    response_60 = make_strategy_field(60)
    response_70 = make_strategy_field(70)
    response_80 = make_strategy_field(80)
    response_90 = make_strategy_field(90)
    response_100 = make_strategy_field(100)


def set_payoffs(group: Group):
    p1, p2 = group.get_players()
    amount_offered = group.amount_offered
    group.offer_accepted = getattr(group, 'response_{}'.format(int(amount_offered)))
    if group.offer_accepted:
        p1.payoff = Constants.endowment - amount_offered
        p2.payoff = amount_offered
    else:
        p1.payoff = 0
        p2.payoff = 0


class Player(BasePlayer):
    pass


class P1(Page):
    form_model = 'group'
    form_fields = ['amount_offered']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class P2(Page):
    form_model = 'group'
    form_fields = ['response_{}'.format(int(i)) for i in Constants.offer_choices]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    title_text = "Thank you"
    body_text = (
        "You can close this page. When the other player arrives, the payoff will be calculated."
    )


class Results(Page):
    pass


page_sequence = [
    P1,
    P2,
    ResultsWaitPage,
    Results,
]
