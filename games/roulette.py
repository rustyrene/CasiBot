import random
from collections import namedtuple

class RouletteError(Exception):
    def __init__(self, message="Invalid Bet"):
        self.message = message
        super().__init__(self.message)

# Mapping roulette options to payout
Color = {
    "RED": 2,
    "BLACK": 2,
    "GREEN": 14
}

Bet = namedtuple("Bet", ["color", "value"])

def roll():
    return random.randint(0, 36)

def validateBets(*args):
    args = args[0]
    bets = []
    for bet in args:
        color = None
        try:
            if bet.color.lower().startswith("r"):
                color = "RED"
            elif bet.color.lower().startswith("b"):
                color = "BLACK"
            elif bet.color.lower().startswith("g"):
                color = "GREEN"
            else:
                raise RouletteError("Unidentified color for bet. Please provide a valid color. (Red/Black/Green)")
        except AttributeError:
            raise RouletteError("Tried to identify a color. Found Number")
        
        try:
            value = int(bet.value)
            if value <= 0:
                raise RouletteError("The minimum amount to bet is 1")
            bets.append(Bet(color=color, value=value))
        except ValueError:
            raise RouletteError("The bet amount must be numerical")
    return bets

def play(*args):
    # Parse and sanatize bets
    bets = []
    args = args[0]
    try:
        for i in range(0, len(args)-1, 2):
            bets.append(Bet(args[i], args[i+1]))
    except IndexError:
        raise RouletteError("Invalid bets. Bets must contain a color and a value")
    
    if (len(args) < 2):
        raise RouletteError("Invalid bets. Bets must contain a color and a value")
    
    bets = validateBets(bets)

    # Generate winning color
    spin = roll()
    winning_color = None
    if spin == 0:
        winning_color = "GREEN"
    elif spin %2 == 0:
        winning_color = "BLACK"
    else:
        winning_color = "RED"

    prize = 0
    for bet in bets:
        if bet.color == winning_color:
            prize += int(bet.value)
        else:
            prize -= int(bet.value)

    return (prize, winning_color)

if __name__ == "__main__":
    import sys
    prize = play(sys.argv[1:])
    print(f"Your prize: {prize}")
