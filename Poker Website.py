from bakery import assert_equal
from dataclasses import dataclass
from drafter import *
from random import randint

# Helper functions

def hand_to_string(cards: list[int]) -> str:
    """
        Taking a list of cards and printing it for the user to see
        Args:
        cards: list[int]): list of cards numerically
        str: represents the card as a string for the user
    """
        #[1,4,12] -> "1 4 Q"
        
    hand_string = ""
    for card in cards:
        hand_string = hand_string + convert_hand(card) + " "
    hand_string.strip()
    return hand_string

def convert_hand(card: int) -> str:
    """
        convert_hands converts a integer representing a card into a string
        Args:
        card(int): card numerically represents the card
        str: represents the card as a string for the user
    """
    if card >= 2 and card < 10:
        return str(card)
    if card == 10:
        return "X"
    elif card == 11:
        return "J"
    elif card == 12:
        return "Q"
    elif card == 13:
        return "K"
    elif card == 14:
        return "A"

def sort_hand(hand:list[int]) -> list:
    '''
Args:
hand: represents a list of three integers
list[int]: represent sa list of integers, represents the card as an integer
'''
    if hand[0] < hand[1]:
        hand[0], hand[1] = hand[1], hand[0]
    if hand[1] < hand[2]:
        hand[1], hand[2] = hand[2], hand[1]
    if hand[0] < hand[1]:
        hand[0], hand[1] = hand[1], hand[0]
    return hand

def has_triple(hand: list[int]) -> bool:
    """
    Args
Hand represents three matching integers that become a "triple"
list[int] represents a list of integers
The function takes in integers and produces whether or not the list is a "triple" or not a triple
by showing true/false
    """
    has_triple_bool = True
    if(hand[0] != hand[1]):
        has_triple_bool = False
    elif(hand[0] != hand[2]):
        has_triple_bool = False
    elif(hand[1] != hand[2]):
        has_triple_bool = False
    return has_triple_bool

def has_straight(hand: list[int]) -> bool:
    ''' 
Hand checks if there is a direct consecutive order from largest to smallest. Has to be 3, 2, 1
and not 4, 2, 1 or 5, 3, 2
'''
    if (hand[0] == hand[1] + 1 and hand[1] + 1 == hand[2] + 2):
        return True
    else:
        return False

def has_pair(hand: list[int]) -> bool:
    '''
    The argument 'hand' checks whether or not there is two identical cards in the same list of integers
    if there are two of the same integers, the code will come back with True, if not
    Then it will come back as False
    '''
    if hand[0] == hand[1]:
        return True
    elif hand[1] == hand[2]:
        return True
    else:
        return False

def score_hand(hand: list[int]) -> int:
    '''
    The arguement, hand, represents a list of three integers and returns a score after calculations.
    '''
    
    if has_straight(hand):
        return ((15 * (16**3))+ (hand[0] * (16**2)) + (hand[1]*16) + hand[2])
    elif has_triple(hand):
        return ((16 * (16**3))+ (hand[0] * (16**2)) + (hand[1]*16) + hand[2])
    elif has_pair(hand):
        if hand[0] == hand[1]:
            feature = hand[0]
        else:
            feature = hand[1]
        return ((feature *(16**3)) + (hand[0] * (16 ** 2)) + (hand[1] * 16) + hand[2])
    else:
        return ((hand[0] * (16**2)) + (hand[1] * 16) + hand[2])

def dealer_plays(hand:list[int]) -> bool:
    '''
The arguement, hand, represents a feature, a queen, or somethinng higher. The lowest
score that is possible to calculate is 5123.
'''
    if((score_hand(hand) >= 5123) or (14 in hand) or (13 in hand) or (12 in hand)):
        return True
    else:
        return False

def deal() -> list[int]:
    '''
deal represents a random card dealing/deals a random hand'''
    return[randint(2, 14), randint(2, 14), randint(2, 14)]
        
# The actual website code

@dataclass
class State:
    name: str
    points: int
    round_start: bool
    player_cards: list[int]
    dealer_cards: list[int]
    ''' Intitalized Variables to indicate the parameters for the Poker Game. A list of randomized
integers is needed to properly play the poker game'''
@route
def index(state: State) -> Page:
    
    return Page(state, [
        "Welcome to Haiya's Magnificent Poker Game!",
        CheckBox("confirmation", state.round_start),
        Button("Ready to Play?", begin)
    ])
'''The index creates the website, it directs you to the first page, which shows the Game Name with a
checkbox confirming whether or not the player want's to play the game'''
@route
def begin(state: State, confirmation: bool) -> Page:
    """ Updates the state with the new player name, then redirects to another page. """
    if confirmation:
        return rules(state)
    else:
        return index(state)
'''Second page, indicates the rules of the game, and requires a check box confirmation of whether or
not the player is ready to play the game. The option "No" redirects the player to the "That's Fine,
then" page'''
@route
def rules(state: State) -> Page:
    return Page(state, [
        "Rules: ",
        "You will be given 3 cards, you will be up against a computer. You must make the judgement call to either pass or fold. To fold, you must have Three of a Kind (e.g., JJJ or 333), A pair is when exactly two of the three cards have the same rank (e.g., AAX or 422), or a A straight is when the three cards form a sequence (e.g., 987 or JX9). Ready to Play?",
        CheckBox("confirmation", state.round_start),
        Button("Yes",yes),
        Button("No",no)
        ])
'''The Rules portion of the website, the route is a page that shows the rules of the game'''
@route
def yes(state: State, confirmation: bool) -> Page:
    """ The page for the game, which will start soon. """
    if confirmation:
        return Page(state,[
            "Enter your name: ",
            TextBox("name", "Player 1"),
            Button("Continue", setup_round)
            ])
    else:
        return rules(state)
'''This route redirects to another page that asks for the players name, and is updated when a new
name is shown.'''
@route
def no(state: State) -> Page:
    return Page(state, [
        "That's fine, then"
        ])
'''This route shows the page that indicates what happens when you choose "No" instead of "Yes"'''
@route
def setup_round(state: State, name: str) -> Page:
    state.name = name
    return play_cards(state)
'''Sets up the poker game, it produces three random cards and the options whether to "Pass" or "Fold"'''
@route
def play_cards(state: State) -> Page:
    if (state.points >= 20):
        return win(state)
    elif (state.points <= -200):
        return lose(state)
    
    state.player_cards = sort_hand(deal())
    return Page(state, [
        "Hello, " + state.name + "!",
        "Your cards: " + hand_to_string(state.player_cards),
        Button("Play", play),
        Button("Fold", fold),
        "Points: " + str(state.points)
    ])
'''Randomizes the cards after Passing or Folding and indicates if you have won or lost and the points
you receive'''
@route
def play(state:State) -> Page:
    state.dealer_cards = sort_hand(deal())
    if not dealer_plays(state.dealer_cards):
        state.points += 10; # Player gets ten points, the dealer folds
        return Page(state, [
            "Your hand: " + hand_to_string(state.player_cards),
            "Dealer's hand: " + hand_to_string(state.dealer_cards),
            "Dealer folded. You get 10 points.",
            Button("Continue", play_cards)
        ])
    else:
        if(score_hand(state.player_cards) >= score_hand(state.dealer_cards)):
            state.points += 20; # Player gets 20 points
            return Page(state, [
                "Your hand: " + hand_to_string(state.player_cards),
                "Dealer's hand: " + hand_to_string(state.dealer_cards),
                "Dealer lost. You get 20 points.",
                Button("Continue", play_cards)
            ])
        else:
            state.points -= 20; # Player loses 20
            return Page(state, [
                "Your hand: " + hand_to_string(state.player_cards),
                "Dealer's hand: " + hand_to_string(state.dealer_cards),
                "Dealer won. You lose 20 points.",
                Button("Continue", play_cards)
            ])
'''Shows the options of what happens when you pass or fold, indicates the dealers hand and how many points
you win or lose'''
@route
def fold(state: State) -> Page:
    state.points -= 10
    return play_cards(state)
'''This portion indicates what happens when you fold, you lose 10 points if you fold'''
@route
def win(state: State) -> Page:
    return Page(state, [
        "Congratulations, You win!",
        Button("Play again?", index)
        ])
'''When you hit the winning point threshold, it will redirect you to the winning page'''
@route
def lose(state: State) -> Page:
    return Page(state, [
        "You Lose!",
        CheckBox("confirmation", state.round_start),
        Button("Play again?", check_playagain)
        ])
'''If you hit the losing threshold, then the losing page will show up and the option to play again
which redirects the player to the first page'''
@route
def check_playagain(state: State, confirmation: bool):
    if confirmation:
        return index(state)
    else:
        return lose(state)
'''Asks if you want to play again after winning the game'''
start_server(State("", 0, False, [], []))
'''Starts the Website'''

#Unit Tests
assert_equal(
 index(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[])),
 Page(state=State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]),
     content=["Welcome to Haiya's Magnificent Poker Game!",
              CheckBox(name='confirmation', default_value=False),
              Button(text='Ready to Play?', url='/begin')]))

assert_equal(
 begin(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]), True),
 Page(state=State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]),
     content=['Rules: ',
              'You will be given 3 cards, you will be up against a computer. You must make the judgement call to '
              'either pass or fold. To fold, you must have Three of a Kind (e.g., JJJ or 333), A pair is when exactly '
              'two of the three cards have the same rank (e.g., AAX or 422), or a A straight is when the three cards '
              'form a sequence (e.g., 987 or JX9). Ready to Play?',
              CheckBox(name='confirmation', default_value=False),
              Button(text='Yes', url='/yes'),
              Button(text='No', url='/no')]))

assert_equal(
 begin(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]), False),
 Page(state=State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]),
     content=["Welcome to Haiya's Magnificent Poker Game!",
              CheckBox(name='confirmation', default_value=False),
              Button(text='Ready to Play?', url='/begin')]))

assert_equal(
 no(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[])),
 Page(state=State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]), content=["That's fine, then"]))

assert_equal(
 yes(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]), True),
 Page(state=State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]),
     content=['Enter your name: ',
              TextBox(name='name', kind='text', default_value='Player 1'),
              Button(text='Continue', url='/setup_round')]))

assert_equal(
 setup_round(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]), 'Player 1'),
 Page(state=State(name='Player 1', points=0, round_start=False, player_cards=[11, 8, 6], dealer_cards=[]),
     content=['Hello, Player 1!',
              'Your cards: J 8 6 ',
              Button(text='Play', url='/play'),
              Button(text='Fold', url='/fold'),
              'Points: 0']))

assert_equal(
 index(State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[])),
 Page(state=State(name='', points=0, round_start=False, player_cards=[], dealer_cards=[]),
     content=["Welcome to Haiya's Magnificent Poker Game!",
              CheckBox(name='confirmation', default_value=False),
              Button(text='Ready to Play?', url='/begin')]))