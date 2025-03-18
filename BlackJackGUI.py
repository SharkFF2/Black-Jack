import tkinter as tk
from tkinter import messagebox
import random
import time

# Numbers and suits
suits = ['hearts', 'diamonds', 'spades', 'clubs']
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def create_deck():
    deck = [{'suit': suit, 'rank': rank, 'value': value} for suit in suits for rank, value in ranks.items()]
    random.shuffle(deck)
    return deck

deck = create_deck()

def calculate_hand(hand):
    value = sum(card['value'] for card in hand)
    num_aces = sum(1 for card in hand if card['rank'] == 'A')

    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1

    return value

class BlackJackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.player_money = 100
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.purchased_power_ups = []

        self.setup_ui()

    def setup_ui(self):
        self.money_label = tk.Label(self.root, text=f"Money: ${self.player_money}")
        self.money_label.pack()

        self.bet_label = tk.Label(self.root, text="Bet: $0")
        self.bet_label.pack()

        self.player_hand_label = tk.Label(self.root, text="Player's Hand: ")
        self.player_hand_label.pack()

        self.dealer_hand_label = tk.Label(self.root, text="Dealer's Hand: ")
        self.dealer_hand_label.pack()

        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        self.bet_button = tk.Button(self.root, text="Place Bet", command=self.place_bet)
        self.bet_button.pack()

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit)
        self.hit_button.pack()

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand)
        self.stand_button.pack()

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.pack()

    def place_bet(self):
        try:
            self.bet = int(self.bet_entry.get())
            if self.bet > self.player_money:
                messagebox.showerror("Error", "You don't have enough money to place that bet.")
            else:
                self.player_money -= self.bet
                self.money_label.config(text=f"Money: ${self.player_money}")
                self.bet_label.config(text=f"Bet: ${self.bet}")
                self.start_game()
        except ValueError:
            messagebox.showerror("Error", "Invalid bet amount.")

    def start_game(self):
        self.player_hand = [deck.pop(), deck.pop()]
        self.dealer_hand = [deck.pop(), deck.pop()]
        self.update_hand_labels()

    def update_hand_labels(self):
        self.player_hand_label.config(text="Player's Hand: " + ', '.join([f"{card['rank']} of {card['suit']}" for card in self.player_hand]) +
                                      f" (Total: {calculate_hand(self.player_hand)})")
        self.dealer_hand_label.config(text=f"Dealer's Hand: {self.dealer_hand[0]['rank']} of {self.dealer_hand[0]['suit']}")

    def hit(self):
        self.player_hand.append(deck.pop())
        self.update_hand_labels()
        if calculate_hand(self.player_hand) > 21:
            messagebox.showinfo("Bust", "Player busts! Dealer wins.")
            self.reset_game()

    def stand(self):
        self.dealer_turn()
        self.determine_winner()

    def dealer_turn(self):
        while calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(deck.pop())
            self.update_hand_labels()
            time.sleep(1)

    def determine_winner(self):
        player_score = calculate_hand(self.player_hand)
        dealer_score = calculate_hand(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            messagebox.showinfo("Result", "Player wins!")
            self.player_money += self.bet * 2
        elif player_score == dealer_score:
            messagebox.showinfo("Result", "Push! (tie)")
            self.player_money += self.bet
        else:
            messagebox.showinfo("Result", "Dealer wins!")

        self.money_label.config(text=f"Money: ${self.player_money}")
        self.reset_game()

    def reset_game(self):
        self.bet = 0
        self.bet_label.config(text="Bet: $0")
        self.player_hand = []
        self.dealer_hand = []
        self.update_hand_labels()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackJackApp(root)
    root.mainloop()