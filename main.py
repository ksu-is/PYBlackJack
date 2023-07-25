# Import the random library
import random 

# Define constants
SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]  # The four suits in a deck of cards
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]  # The possible values for a card
BLACKJACK = 21  # The value of a blackjack
ACE_ALT_VALUE = 10  # The alternate value of an ace
INITIAL_MONEY = 1000  # The initial amount of money the player starts with
DEALER_MINIMUM_VALUE = 17  # The minimum value the dealer must reach before stopping

# Define the Card class
class Card: 
    def __init__(self, suit, value):  # The constructor for a card
        self.suit = suit  # The suit of the card
        self.value = value  # The value of the card

    def __repr__(self):  # The string representation of a card
        return f"{self.value} of {self.suit}"  # Returns the value and suit of the card

# Define the Deck class
class Deck: 
    def __init__(self):  # The constructor for a deck
        # Generate a list of all possible cards
        self.cards = [Card(suit, value) for suit in SUITS for value in VALUES]

    def shuffle(self):  # Shuffles the deck
        if len(self.cards) > 1:  # Only shuffle the deck if there are more than one card
            random.shuffle(self.cards)  # Use the random library to shuffle the deck
    
    def deal(self):  # Deals a card
        if len(self.cards) > 1:  # Only deal a card if there are cards left in the deck
            return self.cards.pop(0)  # Remove the top card from the deck and return it

# Define the Hand class
class Hand: 
    def __init__(self, dealer=False):  # The constructor for a hand
        self.dealer = dealer  # Whether this hand belongs to the dealer
        self.cards = []  # The cards in the hand
        self.value = 0  # The value of the hand

    def add_card(self, card):  # Adds a card to the hand
        self.cards.append(card)  # Append the card to the list of cards

    def calculate_value(self):  # Calculates the value of the hand
        self.value = 0  # Reset the value
        aces = 0  # The number of aces in the hand
        for card in self.cards:  # For each card in the hand
            if card.value.isnumeric():  # If the card value is a number
                self.value += int(card.value)  # Add the value of the card to the total value
            else:  # If the card value is not a number
                if card.value == "A":  # If the card is an ace
                    aces += 1  # Increase the count of aces by 1
                    self.value += 11  # Add 11 to the total value
                else:  # If the card is a face card
                    self.value += 10  # Add 10 to the total value

        # Adjust the value for aces
        while self.value > BLACKJACK and aces:  # While the value is over 21 and there are aces
            self.value -= ACE_ALT_VALUE  # Subtract 10 from the value
            aces -= 1  # Subtract 1 from the count of aces

    def get_value(self):  # Gets the value of the hand
        self.calculate_value()  # Calculate the value of the hand
        return self.value  # Return the value of the hand
    
    def display(self):  # Displays the hand
        if self.dealer:  # If the hand belongs to the dealer
            print("hidden")  # Hide the first card
            print(self.cards[1])  # Show the second card
        else:  # If the hand does not belong to the dealer
            for card in self.cards:  # For each card in the hand
                print(card)  # Print the card
            print("Value:", self.get_value())  # Print the value of the hand

# Define the Game class
class Game: 
    def __init__(self):  # The constructor for the game
        self.money = INITIAL_MONEY  # The amount of money the player has

    def play(self):  # The main game loop
        playing = True  # Whether the player is still playing

        while playing:  # While the player is still playing
            self.bet = self.get_bet()  # Get the bet from the player

            self.deck = Deck()  # Create a new deck
            self.deck.shuffle()  # Shuffle the deck

            self.player_hand = Hand()  # Create a new hand for the player
            self.dealer_hand = Hand(dealer=True)  # Create a new hand for the dealer

            for _ in range(2):  # Deal two cards to each player
                self.player_hand.add_card(self.deck.deal())  # Deal a card to the player
                self.dealer_hand.add_card(self.deck.deal())  # Deal a card to the dealer
            
            print("Your hand is:")  # Print the player's hand
            self.player_hand.display()  # Display the player's hand
            print()  # Print a newline
            print("Dealer's hand is: ")  # Print the dealer's hand
            self.dealer_hand.display()  # Display the dealer's hand

            game_over = False  # Whether the game is over

            while not game_over:  # While the game is not over
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()  # Check for blackjack

                if player_has_blackjack or dealer_has_blackjack:  # If either player has blackjack
                    game_over = True  # The game is over
                    self.show_blackjack_results(
                        player_has_blackjack , dealer_has_blackjack, self.bet)  # Show the results
                    continue  # Skip the rest of the loop
                
                print("\nChoose your action:")  # Prompt the player to choose an action
                print("[1] - Hit")  # The player can choose to hit
                print("[2] - Stand")  # The player can choose to stand
                print("[3] - Double Down")  # The player can choose to double down
                if self.can_split(self.player_hand):  # If the player can split their hand
                    print("[4] - Split")  # The player can choose to split their hand

                choice = self.get_choice(["1", "2", "3", "4"])  # Get the player's choice

                if choice == '1':  # If the player chose to hit
                    self.hit(self.player_hand)  # Hit the player's hand
                    if self.is_bust(self.player_hand):  # If the player's hand is a bust
                        print("You have lost!")  # The player loses
                        self.money -= self.bet  # Subtract the bet from the player's money
                        game_over = True  # The game is over
                
                elif choice == '2':  # If the player chose to stand
                    self.stand()  # Stand
                    game_over = True  # The game is over
                
                elif choice == '3':  # If the player chose to double down
                    self.double_down(self.player_hand)  # Double down on the player's hand
                    if self.is_bust(self.player_hand):  # If the player's hand is a bust
                        print("You have lost!")  # The player loses
                        self.money -= 2 * self.bet  # Subtract double the bet from the player's money
                        game_over = True  # The game is over
                    else:  # If the player's hand is not a bust
                        self.bet *= 2  # Double the bet
                
                elif choice == '4':  # If the player chose to split
                    self.split_hand()  # Split the player's hand
                
            print(f"You now have ${self.money}")  # Print the player's current money

            again = input("Play Again?")  # Ask the player if they want to play again
            while again.lower() not in ["y" , "n"]:  # While the player's input is not "y" or "n"
                again = input("Please enter Y or N ")  # Prompt the player to enter "y" or "n"
            if again.lower() == "n":  # If the player does not want to play again
                print("Thanks for playing, Come back soon!")  # Thank the player for playing
                playing = False  # The player is not playing anymore
            else:  # If the player wants to play again
                game_over = False  # The game is not over

    def hit(self, hand):  # The hit action
        hand.add_card(self.deck.deal())  # Add a card to the hand
        hand.display()  # Display the hand

    def stand(self):  # The stand action
        while self.dealer_hand.get_value() < DEALER_MINIMUM_VALUE:  # While the dealer's hand is less than the minimum value
            self.dealer_hand.add_card(self.deck.deal())  # Add a card to the dealer's hand
        
        print("\nDealer's final hand:")  # Print the dealer's final hand
        self.dealer_hand.display()  # Display the dealer's final hand
        
        player_hand_value = self.player_hand.get_value()  # Get the value of the player's hand
        dealer_hand_value = self.dealer_hand.get_value()  # Get the value of the dealer's hand

        print("Final Results")  # Print the final results
        print("Your hand:", player_hand_value)  # Print the value of the player's hand
        print("Dealer's hand:", dealer_hand_value)  # Print the value of the dealer's hand

        if self.is_bust(self.dealer_hand):  # If the dealer's hand is a bust
            print("Dealer has busted! You win!")  # The player wins
            self.money += self.bet  # Add the bet to the player's money
        elif player_hand_value > dealer_hand_value:  # If the player's hand is greater than the dealer's hand
            print("You Win!")  # The player wins
            self.money += self.bet  # Add the bet to the player's money
        elif player_hand_value == dealer_hand_value:  # If the player's hand is equal to the dealer's hand
            print("Tie!")  # It's a tie
        else:  # If the dealer's hand is greater than the player's hand
            print("Dealer Wins!")  # The dealer wins
            self.money -= self.bet  # Subtract the bet from the player's money

    def double_down(self, hand):  # The double down action
        self.hit(hand)  # Hit the hand

    def split_hand(self):  # The split action
        if not self.can_split(self.player_hand):  # If the player cannot split their hand
            print("Cannot split hand!")  # Print that the player cannot split their hand
            return  # Return from the function

        # Create a new hand and move one card to the new hand
        self.player_hand2 = Hand()  # Create a new hand for the player
        self.player_hand2.add_card(self.player_hand.cards.pop())  # Move one card from the player's hand to the new hand

        # Deal a new card to each hand
        self.player_hand.add_card(self.deck.deal())  # Add a card to the player's hand
        self.player_hand2.add_card(self.deck.deal())  # Add a card to the new hand

        print("\nFirst hand:")  # Print the first hand
        self.player_hand.display()  # Display the first hand
        print("\nSecond hand:")  # Print the second hand
        self.player_hand2.display()  # Display the second hand

        # Play the first hand
        print("\nPlaying first hand...")  # Print that the first hand is being played
        self.play_hand(self.player_hand)  # Play the first hand

        # Play the second hand
        print("\nPlaying second hand...")  # Print that the second hand is being played
        self.play_hand(self.player_hand2)  # Play the second hand

    def play_hand(self, hand):  # Play a hand
        game_over = False  # Whether the game is over
        while not game_over:  # While the game is not over
            print("\nChoose your action:")  # Prompt the player to choose an action
            print("[1] - Hit")  # The player can choose to hit
            print("[2] - Stand")  # The player can choose to stand
            print("[3] - Double Down")  # The player can choose to double down

            choice = self.get_choice(["1", "2", "3"])  # Get the player's choice

            if choice == '1':  # If the player chose to hit
                self.hit(hand)  # Hit the hand
                if self.is_bust(hand):  # If the hand is a bust
                    print("You have lost!")  # The player loses
                    self.money -= self.bet / 2  # Subtract half the bet from the player's money
                    game_over = True  # The game is over
            
            elif choice == '2':  # If the player chose to stand
                self.stand()  # Stand
                game_over = True  # The game is over
            
            elif choice == '3':  # If the player chose to double down
                self.double_down(hand)  # Double down on the hand
                if self.is_bust(hand):  # If the hand is a bust
                    print("You have lost!")  # The player loses
                    self.money -= self.bet  # Subtract the bet from the player's money
                    game_over = True  # The game is over
                else:  # If the hand is not a bust
                    self.bet *= 2  # Double the bet

    def is_bust(self, hand):  # Check if a hand is a bust
        return hand.get_value() > BLACKJACK  # Return whether the hand's value is greater than 21

    def can_split(self, hand):  # Check if a hand can be split
        # Return whether the hand has two cards and the value of the two cards are the same
        return len(hand.cards) == 2 and self.card_value(hand.cards[0]) == self.card_value(hand.cards[1])

    def card_value(self, card):  # Get the value of a card
        if card.value.isnumeric():  # If the card value is a number
            return int(card.value)  # Return the value as an integer
        elif card.value == "A":  # If the card is an ace
            return 11  # Return 11
        else:  # If the card is a face card
            return 10  # Return 10

    def get_bet(self):  # Get the bet from the player
        while True:  # While the bet is invalid
            bet = input(f"You have ${self.money}. How much do you want to bet?")  # Prompt the player to enter their bet
            if bet.isnumeric() and 0 < int(bet) <= self.money:  # If the bet is a valid number and is less than or equal to the player's money
                return int(bet)  # Return the bet
            print("Invalid bet. Please enter a number between 1 and your current amount of money.")  # Print an error message

    def get_choice(self, valid_choices):  # Get a choice from the player
        while True:  # While the choice is invalid
            choice = input()  # Get the choice from the player
            if choice in valid_choices:  # If the choice is valid
                return choice  # Return the choice
            print(f"Invalid choice. Please enter one of {valid_choices}.")  # Print an error message

    def check_for_blackjack(self):  # Check for blackjack
        player = self.player_hand.get_value() == BLACKJACK  # Whether the player has blackjack
        dealer = self.dealer_hand.get_value() == BLACKJACK  # Whether the dealer has blackjack

        return player, dealer  # Return whether the player and dealer have blackjack
    
    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack, bet):  # Show the results of blackjack
        if player_has_blackjack and dealer_has_blackjack:  # If both the player and dealer have blackjack
            print("Both players have blackjack! Draw!")  # It's a draw

        elif player_has_blackjack:  # If the player has blackjack
            print("Player has BLACKJACK! Congratulations! Player wins!")  # The player wins
            self.money += 1.5 * bet  # Add 1.5 times the bet to the player's money
        
        elif dealer_has_blackjack:  # If the dealer has blackjack
            print("Dealer has blackjack! Dealer wins!")  # The dealer wins
            self.money -= bet  # Subtract the bet from the player's money

if __name__ == "__main__":  # If this script is being run directly
    g = Game()  # Create a new game
    g.play()  # Start the game
