"""Simple blackjack game."""
import random


class Card(object):
    """Card class."""

    def __init__(self, suit, val):
        """Initialize the Card class with a suit and value."""
        self.suit = suit
        self.val = val

    def __repr__(self):
        """Represent the card as a string."""
        return "{} of {}".format(self.val, self.suit)


class Deck(object):
    """Deck class."""

    def __init__(self, jokers=False):
        """Initialize the Deck class.

        If jokers, 2 cards inserted.
        """
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        cards = [str(x) for x in range(2, 11)] + ['J', 'Q', 'K', 'A']
        self._deck = []
        for card in cards:
            for suit in suits:
                self._deck.append(Card(suit, card))
        if jokers:
            self._deck += [Card('Misc.', 'Jkr1'), Card('Misc.', 'Jkr2')]

    def shuffle(self):
        """Shuffle the Deck."""
        random.shuffle(self._deck)

    def draw(self):
        """Remove top card from Deck, return it."""
        try:
            return self._deck.pop(0)
        except IndexError:
            raise IndexError('Deck is out of cards.')

    def peek(self):
        """Peek at the top card of the Deck."""
        try:
            return self._deck[0]
        except IndexError:
            raise IndexError('Deck is out of cards.')


class Player(object):
    """Player class."""

    def __init__(self, name, bank=100, dealer=False):
        """Initialize the Player class."""
        self.hand = []
        self.name = name
        self.bank = bank
        if dealer:
            self.dealer = True

    def draw_card(self, deck):
        """Draw a card from the top of the Deck."""
        self.hand.append(deck.draw())

    def get_hand(self):
        """Return hand of Player."""
        return self.hand

    def __repr__(self):
        """Representation of Player."""
        return self.name


class BlackJackGame(object):
    """Blackjack game class."""

    def __init__(self, num_players=1, deck=Deck(jokers=False),
                 players=[Player(name='Player1')]):
        """Initialize a new game."""
        self.num_players = num_players
        self.deck = deck
        self.players = players
        self.dealer = Player(name='Dealer', dealer=True, bank=1000000)

    def deal_round_of_cards(self):
        """Deal one card to each player and the dealer."""
        for player in self.players:
            if player.bank > 0:
                player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)

    def show_player_hand(self, player, show_all=False):
        """Show all except first card in a Player's hand."""
        if show_all:
            return player.get_hand()
        return player.get_hand()[1:]

    def account_for_aces(self, curr_total, num_aces=0):
        """Return the value to best help the player from number of aces."""
        if num_aces == 0:
            return 0

        ace_values = (1 + (num_aces - 1), 11 + (num_aces - 1))
        if ace_values[1] + curr_total > 21:
            return ace_values[0]
        return ace_values[1]

    def get_best_value(self, player):
        """Return the closest value to 21 if <= to 21.

        If the player hand is busted, return 0.
        """
        hand = player.hand
        total_value = 0
        aces = []

        for card in hand:
            try:
                total_value += int(card.val)
            except:
                if card.val in ['K', 'Q', 'J']:
                    total_value += 10
                if card.val == 'A':
                    aces.append(card)

        aces_val = self.account_for_aces(total_value, len(aces))
        return total_value + aces_val

    def check_busted(self, player):
        """Return boolean if player is busted."""
        if self.get_best_value(player) > 21:
            return True
        return False

    def show_table(self):
        """Show the cards on the table."""
        print('------------------' * 2)
        print('Here is the table:')
        print('------------------' * 2)
        print('{}: {}, (face-down card)'.format(self.dealer.name,
              self.show_player_hand(self.dealer)))

        for player in self.players:
            print('{}: {}'.format(player.name,
                  self.show_player_hand(player, show_all=True)))

        print('------------------' * 2)

    def start_round(self):
        """Start a round of the game."""
        self.deck.shuffle()
        self.deal_round_of_cards()
        self.deal_round_of_cards()


if __name__ == '__main__':
    """The game logic."""
    u_input = ''
    tmp_input = ''

    while u_input not in ['1', '2', '3']:
        u_input = input('How many players?  (max of 3): ')

    names = []
    players = []
    for i in range(int(u_input)):
        tmp_input = input('Name of player {}?'.format(str(i + 1)))
        names.append(tmp_input)
    for name in names:
        players.append(Player(name=name))

    print('Let\'s start the game!')
    game = BlackJackGame(players=players)
    game_in_progress = True

    while game_in_progress:
        bets = []
        for player in players:
            b = 0
            print('{}, you have {} dollars.'.format(player.name, player.bank))
            if player.bank > 0:
                while b <= 0 or b > player.bank:
                    b = int(input('{}, How much would you like to bet? '.format(player.name)))
                    if b <= 0 or b > player.bank:
                        print('--- Invalid bet, try again. ---')

        print('Dealing...')
        game.start_round()
        game.show_table()
        results = []
        discard_pile = []

        for p in players:
            tmp_input = ''
            done = False
            while (not done) and p.bank > 0:
                print('{}, it is your turn.'.format(p.name))
                print(game.show_player_hand(p, show_all=True))
                counter = 0

                while True:
                    tmp_input = input('(h)it or (s)tay?: ').lower()
                    if tmp_input == 's':
                        print(game.get_best_value(p))
                        results.append(game.get_best_value(p))
                        if game.check_busted(p):
                            print('Busted!')
                        discard_pile += p.hand
                        break
                    if tmp_input == 'h' and counter < 3:
                        counter += 1
                        p.draw_card(deck=game.deck)
                        print(game.show_player_hand(p, show_all=True))
                    else:
                        print('Command not recognized, or have 5 cards.')
                done = True

        # do dealer logic here
        # ...

        print('results: ', results)
        game.deck._deck += discard_pile

        # continue game?
        game_in_progress = False
