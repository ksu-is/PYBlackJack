import random 

SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
BLACKJACK = 21
ACE_ALT_VALUE = 10
INITIAL_MONEY = 1000
DEALER_MINIMUM_VALUE = 17

class Card: 
    def __init__(self, suit, value): 
        self.suit = suit 
        self.value = value 

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck: 
    def __init__(self): 
        self.cards = [Card(suit, value) for suit in SUITS for value in VALUES]

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

class Hand: 
    def __init__(self, dealer=False):
        self.dealer = dealer 
        self.cards = []
        self.value = 0 

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
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

    def get_value(self):
        self.calculate_value()
        return self.value
    
    def display(self):
        if self.dealer: 
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards: 
                print(card)
            print("Value:", self.get_value())

class Game: 
    def __init__(self):
        self.money = INITIAL_MONEY

    def play(self):
        playing = True 

        while playing: 
            self.bet = self.get_bet()  # Move the bet to the beginning of the round

            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand(dealer=True)

            for _ in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())
            
            print("Your hand is:")
            self.player_hand.display()
            print()
            print("Dealer's hand is: ")
            self.dealer_hand.display()

            game_over = False

            while not game_over: 
                player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()

                if player_has_blackjack or dealer_has_blackjack:
                    game_over = True 
                    self.show_blackjack_results(
                        player_has_blackjack , dealer_has_blackjack, self.bet)
                    continue 
                
                print("\nChoose your action:")
                print("[1] - Hit")
                print("[2] - Stand")
                print("[3] - Double Down")
                if self.can_split(self.player_hand):
                    print("[4] - Split")

                choice = self.get_choice(["1", "2", "3", "4"])

                if choice == '1':
                    self.hit(self.player_hand)
                    if self.is_bust(self.player_hand):
                        print("You have lost!")
                        self.money -= self.bet
                        game_over = True
                
                elif choice == '2':
                    self.stand()
                    game_over = True
                
                elif choice == '3':
                    self.double_down(self.player_hand)
                    if self.is_bust(self.player_hand):
                        print("You have lost!")
                        self.money -= 2 * self.bet
                        game_over = True
                    else:
                        self.bet *= 2
                
                elif choice == '4':
                    self.split_hand()
                
            print(f"You now have ${self.money}")

            again = input("Play Again?")
            while again.lower() not in ["y" , "n"]:
                again = input("Please enter Y or N ")
            if again.lower() == "n":
                print("Thanks for playing, Come back soon!")
                playing = False
            else:
                game_over = False

    def hit(self, hand):
        hand.add_card(self.deck.deal())
        hand.display()

    def stand(self):
        while self.dealer_hand.get_value() < DEALER_MINIMUM_VALUE:
            self.dealer_hand.add_card(self.deck.deal())
        
        print("\nDealer's final hand:")
        self.dealer_hand.display()
        
        player_hand_value = self.player_hand.get_value()
        dealer_hand_value = self.dealer_hand.get_value()

        print("Final Results")
        print("Your hand:", player_hand_value)
        print("Dealer's hand:", dealer_hand_value)

        if self.is_bust(self.dealer_hand):
            print("Dealer has busted! You win!")
            self.money += self.bet
        elif player_hand_value > dealer_hand_value:
            print("You Win!")
            self.money += self.bet
        elif player_hand_value == dealer_hand_value:
            print("Tie!")
        else: 
            print("Dealer Wins!")
            self.money -= self.bet

    def double_down(self, hand):
        self.hit(hand)

    def split_hand(self):
        if not self.can_split(self.player_hand):
            print("Cannot split hand!")
            return

        # Create a new hand and move one card to the new hand
        self.player_hand2 = Hand()
        self.player_hand2.add_card(self.player_hand.cards.pop())

        # Deal a new card to each hand
        self.player_hand.add_card(self.deck.deal())
        self.player_hand2.add_card(self.deck.deal())

        print("\nFirst hand:")
        self.player_hand.display()
        print("\nSecond hand:")
        self.player_hand2.display()

        # Play the first hand
        print("\nPlaying first hand...")
        self.play_hand(self.player_hand)

        # Play the second hand
        print("\nPlaying second hand...")
        self.play_hand(self.player_hand2)

    def play_hand(self, hand):
        game_over = False
        while not game_over:
            print("\nChoose your action:")
            print("[1] - Hit")
            print("[2] - Stand")
            print("[3] - Double Down")

            choice = self.get_choice(["1", "2", "3"])

            if choice == '1':
                self.hit(hand)
                if self.is_bust(hand):
                    print("You have lost!")
                    self.money -= self.bet / 2
                    game_over = True
            
            elif choice == '2':
                self.stand()
                game_over = True
            
            elif choice == '3':
                self.double_down(hand)
                if self.is_bust(hand):
                    print("You have lost!")
                    self.money -= self.bet
                    game_over = True
                else:
                    self.bet *= 2

    def is_bust(self, hand):
        return hand.get_value() > BLACKJACK

    def can_split(self, hand):
        return len(hand.cards) == 2 and self.card_value(hand.cards[0]) == self.card_value(hand.cards[1])

    def card_value(self, card):
        if card.value.isnumeric():
            return int(card.value)
        elif card.value == "A":
            return 11
        else:
            return 10

    def get_bet(self):
        while True:
            bet = input(f"You have ${self.money}. How much do you want to bet?")
            if bet.isnumeric() and 0 < int(bet) <= self.money:
                return int(bet)
            print("Invalid bet. Please enter a number between 1 and your current amount of money.")

    def get_choice(self, valid_choices):
        while True:
            choice = input()
            if choice in valid_choices:
                return choice
            print(f"Invalid choice. Please enter one of {valid_choices}.")

    def check_for_blackjack(self):
        player = self.player_hand.get_value() == BLACKJACK
        dealer = self.dealer_hand.get_value() == BLACKJACK

        return player, dealer
    
    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack, bet):
        if player_has_blackjack and dealer_has_blackjack:
            print("Both players have blackjack! Draw!")

        elif player_has_blackjack: 
            print("Player has BLACKJACK! Congratulations! Player wins!")
            self.money += 1.5 * bet
        
        elif dealer_has_blackjack:
            print("Dealer has blackjack! Dealer wins!")
            self.money -= bet

if __name__ == "__main__":
    g = Game()
    g.play()
