import random  # Random library is imported to shuffle the deck of cards

# Constants are defined
SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]  # Suits of a standard deck
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]  # Card values of a standard deck
BLACKJACK = 21  # The target sum in Blackjack
ACE_ALT_VALUE = 10  # The alternative value of an ace in Blackjack
INITIAL_MONEY = 1000  # The starting amount of money for the player
DEALER_MINIMUM_VALUE = 17  # The minimum sum the dealer has to reach before stopping

# Card class represents a single card from a standard deck
class Card: 
    def __init__(self, suit, value):  # Constructor assigns a suit and value to a card
        self.suit = suit 
        self.value = value 

    def __repr__(self):  # Represent the card as a string
        return f"{self.value} of {self.suit}"

# Deck class represents a deck of cards
class Deck: 
    def __init__(self):  # Constructor generates a standard deck of cards
        self.cards = [Card(suit, value) for suit in SUITS for value in VALUES]

    def shuffle(self):  # Shuffle the deck if it contains more than one card
        if len(self.cards) > 1:
            random.shuffle(self.cards)
    
    def deal(self):  # Deal a card from the deck
        if len(self.cards) > 1:
            return self.cards.pop(0)

# Hand class represents a hand of cards held by a player or dealer
class Hand: 
    def __init__(self, dealer=False):  # Constructor creates an empty hand
        self.dealer = dealer 
        self.cards = []
        self.value = 0 

    def add_card(self, card):  # Add a card to the hand
        self.cards.append(card)

    def calculate_value(self):  # Calculate the sum of the hand
        self.value = 0 
        aces = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    aces += 1
                    self.value += 11
                else:
                    self.value += 10

        while self.value > BLACKJACK and aces:
            self.value -= ACE_ALT_VALUE
            aces -= 1

    def get_value(self):  # Get the sum of the hand
        self.calculate_value()
        return self.value
    
    def display(self):  # Print the cards in the hand
        if self.dealer:  # If the hand belongs to the dealer, hide the first card
            print("hidden")
            print(self.cards[1])
        else:  # If the hand belongs to the player, show all cards
            for card in self.cards: 
                print(card)
            print("Value:", self.get_value())

# Game class represents a game of Blackjack
class Game: 
    def __init__(self):  # Constructor initializes the player's money
        self.money = INITIAL_MONEY

    def play(self):  # Start a game of Blackjack
        playing = True 

        while playing:  # Keep playing until the player decides to stop
            self.bet = self.get_bet()  # Get the player's bet

            self.deck = Deck()  # Create a new deck and shuffle it
            self.deck.shuffle()

            self.player_hand = Hand()  # Create a new hand for the player
            self.dealer_hand = Hand(dealer=True)  # Create a new hand for the dealer

            for _ in range(2):  # Deal two cards to each player
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())
            
            print("Your hand is:")  # Show the player's hand
            self.player_hand.display()
            print()
            print("Dealer's hand is: ")  # Show the dealer's hand
            self.dealer_hand.display()

            game_over = False  # Set the game state to not over

            while not game_over:  # Keep playing until the game is over
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()  # Check if either player has Blackjack

                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True 
                    self.show_blackjack_results(
                        player_has_blackjack , dealer_has_blackjack, self.bet)  # Show the results of Blackjack
                    continue 
                
                print("\nChoose your action:")  # Ask the player to choose an action
                print("[1] - Hit")
                print("[2] - Stand")
                print("[3] - Double Down")
                if self.can_split(self.player_hand):  # If the player can split, give them the option
                    print("[4] - Split")

                choice = self.get_choice(["1", "2", "3", "4"])  # Get the player's choice

                if choice == '1':  # If the player chose to hit
                    self.hit(self.player_hand)  # Hit the player's hand
                    if self.is_bust(self.player_hand):  # If the player busts, they lose
                        print("You have lost!")
                        self.money -= self.bet
                        game_over = True
                
                elif choice == '2':  # If the player chose to stand
                    self.stand()  # Stand and determine the results
                    game_over = True
                
                elif choice == '3':  # If the player chose to double down
                    self.double_down(self.player_hand)  # Double down the player's hand
                    if self.is_bust(self.player_hand):  # If the player busts, they lose double
                        print("You have lost!")
                        self.money -= 2 * self.bet
                        game_over = True
                    else:
                        self.bet *= 2
                
                elif choice == '4':  # If the player chose to split
                    self.split_hand()  # Split the player's hand
                
            print(f"You now have ${self.money}")  # Show the player's current money

            again = input("Play Again?")  # Ask the player if they want to play again
            while again.lower() not in ["y" , "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == "n":  # If the player doesn't want to play again, thank them for playing
                print("Thanks for playing, Come back soon!")
                playing = False
            else:
                game_over = False

    def hit(self, hand):  # Hit a hand
        hand.add_card(self.deck.deal())  # Deal a card to the hand
        hand.display()  # Show the hand

    def stand(self):  # Stand with a hand
        while self.dealer_hand.get_value() < DEALER_MINIMUM_VALUE:  # While the dealer's hand is less than 17
            self.dealer_hand.add_card(self.deck.deal())  # Deal a card to the dealer's hand
        
        print("\nDealer's final hand:")  # Show the dealer's final hand
        self.dealer_hand.display()
        
        player_hand_value = self.player_hand.get_value()  # Get the player's hand value
        dealer_hand_value = self.dealer_hand.get_value()  # Get the dealer's hand value

        print("Final Results")  # Show the final results
        print("Your hand:", player_hand_value)
        print("Dealer's hand:", dealer_hand_value)

        if self.is_bust(self.dealer_hand):  # If the dealer busts, the player wins
            print("Dealer has busted! You win!")
            self.money += self.bet
        elif player_hand_value > dealer_hand_value:  # If the player has a higher hand, they win
            print("You Win!")
            self.money += self.bet
        elif player_hand_value == dealer_hand_value:  # If the hands are equal, it's a tie
            print("Tie!")
        else:  # Otherwise, the dealer wins
            print("Dealer Wins!")
            self.money -= self.bet

    def double_down(self, hand):  # Double down a hand
        self.hit(hand)  # Hit the hand

    def split_hand(self):  # Split a hand
        if not self.can_split(self.player_hand):  # If the hand can't be split, print a message and return
            print("Cannot split hand!")
            return

        # Create a new hand and move one card to the new hand
        self.player_hand2 = Hand()
        self.player_hand2.add_card(self.player_hand.cards.pop())

        # Deal a new card to each hand
        self.player_hand.add_card(self.deck.deal())
        self.player_hand2.add_card(self.deck.deal())

        print("\nFirst hand:")  # Show the first hand
        self.player_hand.display()
        print("\nSecond hand:")  # Show the second hand
        self.player_hand2.display()

        # Play the first hand
        print("\nPlaying first hand...")
        self.play_hand(self.player_hand)

        # Play the second hand
        print("\nPlaying second hand...")
        self.play_hand(self.player_hand2)

    def play_hand(self, hand):  # Play a hand
        game_over = False
        while not game_over:  # Keep playing until the game is over
            print("\nChoose your action:")  # Ask the player to choose an action
            print("[1] - Hit")
            print("[2] - Stand")
            print("[3] - Double Down")

            choice = self.get_choice(["1", "2", "3"])  # Get the player's choice

            if choice == '1':  # If the player chose to hit
                self.hit(hand)  # Hit the hand
                if self.is_bust(hand):  # If the player busts, they lose
                    print("You have lost!")
                    self.money -= self.bet / 2
                    game_over = True
            
            elif choice == '2':  # If the player chose to stand
                self.stand()  # Stand and determine the results
                game_over = True
            
            elif choice == '3':  # If the player chose to double down
                self.double_down(hand)  # Double down the hand
                if self.is_bust(hand):  # If the player busts, they lose double
                    print("You have lost!")
                    self.money -= self.bet
                    game_over = True
                else:
                    self.bet *= 2

    def is_bust(self, hand):  # Check if a hand is a bust
        return hand.get_value() > BLACKJACK

    def can_split(self, hand):  # Check if a hand can be split
        return len(hand.cards) == 2 and self.card_value(hand.cards[0]) == self.card_value(hand.cards[1])

    def card_value(self, card):  # Get the value of a card
        if card.value.isnumeric():  # If the card is a number, return its integer value
            return int(card.value)
        elif card.value == "A":  # If the card is an ace, return 11
            return 11
        else:  # Otherwise, return 10 (for face cards)
            return 10

    def get_bet(self):  # Get the player's bet
        while True:  # Keep asking until a valid bet is given
            bet = input(f"You have ${self.money}. How much do you want to bet?")  # Ask for the bet
            if bet.isnumeric() and 0 < int(bet) <= self.money:  # If the bet is a number and the player can afford it, return it
                return int(bet)
            print("Invalid bet. Please enter a number between 1 and your current amount of money.")  # Otherwise, print a message

    def get_choice(self, valid_choices):  # Get the player's choice
        while True:  # Keep asking until a valid choice is given
            choice = input()  # Get the choice
            if choice in valid_choices:  # If the choice is valid, return it
                return choice
            print(f"Invalid choice. Please enter one of {valid_choices}.")  # Otherwise, print a message

    def check_for_blackjack(self):  # Check if either player has Blackjack
        player = self.player_hand.get_value() == BLACKJACK  # Check the player's hand
        dealer = self.dealer_hand.get_value() == BLACKJACK  # Check the dealer's hand

        return player, dealer  # Return the results
    
    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack, bet):  # Show the results of Blackjack
        if player_has_blackjack and dealer_has_blackjack:  # If both players have Blackjack, it's a draw
            print("Both players have blackjack! Draw!")

        elif player_has_blackjack:  # If only the player has Blackjack, they win
            print("Player has BLACKJACK! Congratulations! Player wins!")
            self.money += 1.5 * bet
        
        elif dealer_has_blackjack:  # If only the dealer has Blackjack, they win
            print("Dealer has blackjack! Dealer wins!")
            self.money -= bet

if __name__ == "__main__":  # If this script is run as a standalone program (not imported as a module)
    g = Game()  # Create a new game
    g.play()  # Start the game
