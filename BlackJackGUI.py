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

def award_power_up():
    power_ups = ['extra_card', 'double_winnings']
    if random.random() < 0.2:  # 20% chance to get a power-up
        return random.choice(power_ups)
    return None

class BlackJackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("600x400")  # Set the window size
        self.root.resizable(True, True)  # Allow window resizing
        self.player_money = 100
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.player_power_ups = []

        self.setup_ui()

    def setup_ui(self):
        # Create frames for better organization
        self.top_frame = tk.Frame(self.root, bg="green")
        self.top_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.middle_frame = tk.Frame(self.root, bg="darkgreen")
        self.middle_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        self.bottom_frame = tk.Frame(self.root, bg="green")
        self.bottom_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Configure grid weights to make widgets expand
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Top frame widgets
        self.money_label = tk.Label(self.top_frame, text=f"Money: ${self.player_money}", bg="green", fg="white", font=("Helvetica", 14))
        self.money_label.grid(row=0, column=0, padx=10, sticky="w")

        self.bet_label = tk.Label(self.top_frame, text="Bet: $0", bg="green", fg="white", font=("Helvetica", 14))
        self.bet_label.grid(row=0, column=1, padx=10, sticky="e")

        # Middle frame widgets
        self.player_hand_label = tk.Label(self.middle_frame, text="Player's Hand: ", bg="darkgreen", fg="white", font=("Helvetica", 12))
        self.player_hand_label.grid(row=0, column=0, padx=10, sticky="w")

        self.dealer_hand_label = tk.Label(self.middle_frame, text="Dealer's Hand: ", bg="darkgreen", fg="white", font=("Helvetica", 12))
        self.dealer_hand_label.grid(row=1, column=0, padx=10, sticky="w")

        # Bottom frame widgets
        self.bet_entry = tk.Entry(self.bottom_frame, font=("Helvetica", 12))
        self.bet_entry.grid(row=0, column=0, padx=10, sticky="ew")

        self.bet_button = tk.Button(self.bottom_frame, text="Place Bet", command=self.place_bet, bg="white", fg="black", font=("Helvetica", 12))
        self.bet_button.grid(row=0, column=1, padx=10, sticky="ew")

        self.hit_button = tk.Button(self.bottom_frame, text="Hit", command=self.hit, bg="white", fg="black", font=("Helvetica", 12))
        self.hit_button.grid(row=1, column=0, padx=10, sticky="ew")

        self.stand_button = tk.Button(self.bottom_frame, text="Stand", command=self.stand, bg="white", fg="black", font=("Helvetica", 12))
        self.stand_button.grid(row=1, column=1, padx=10, sticky="ew")

        self.power_up_button = tk.Button(self.bottom_frame, text="Use Power-up", command=self.use_power_up, bg="white", fg="black", font=("Helvetica", 12))
        self.power_up_button.grid(row=2, column=0, padx=10, sticky="ew")

        self.reset_button = tk.Button(self.bottom_frame, text="Reset", command=self.reset_game, bg="white", fg="black", font=("Helvetica", 12))
        self.reset_button.grid(row=2, column=1, padx=10, sticky="ew")

        # Configure grid weights for bottom frame
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

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
        self.update_hand_labels(show_dealer_first_card=True)

    def update_hand_labels(self, show_dealer_first_card=False):
        self.player_hand_label.config(text="Player's Hand: " + ', '.join([f"{card['rank']} of {card['suit']}" for card in self.player_hand]) +
                                      f" (Total: {calculate_hand(self.player_hand)})")
        if show_dealer_first_card:
            self.dealer_hand_label.config(text=f"Dealer's Hand: {self.dealer_hand[0]['rank']} of {self.dealer_hand[0]['suit']}")
        else:
            self.dealer_hand_label.config(text="Dealer's Hand: " + ', '.join([f"{card['rank']} of {card['suit']}" for card in self.dealer_hand]) +
                                          f" (Total: {calculate_hand(self.dealer_hand)})")

    def hit(self):
        self.player_hand.append(deck.pop())
        self.update_hand_labels(show_dealer_first_card=True)
        if calculate_hand(self.player_hand) > 21:
            messagebox.showinfo("Bust", "Player busts! Dealer wins.")
            self.reset_game()

    def stand(self):
        self.dealer_turn()
        self.determine_winner()

    def dealer_turn(self):
        while calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(deck.pop())
            self.update_hand_labels(show_dealer_first_card=True)
            time.sleep(1)

    def determine_winner(self):
        self.update_hand_labels(show_dealer_first_card=False)  # Update to show the dealer's full hand
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
            self.player_money -= self.bet

        self.money_label.config(text=f"Money: ${self.player_money}")
        self.reset_game()

    def use_power_up(self):
        if not self.player_power_ups:
            messagebox.showinfo("Info", "You don't have any power-ups.")
            return
        power_up = self.player_power_ups.pop()
        if power_up == 'extra_card':
            self.player_hand.append(deck.pop())
            self.update_hand_labels(show_dealer_first_card=True)
            if calculate_hand(self.player_hand) > 21:
                messagebox.showinfo("Bust", "Player busts! Dealer wins.")
                self.reset_game()
        elif power_up == 'double_winnings':
            self.bet *= 2
            messagebox.showinfo("Info", "Your winnings for this round will be doubled!")

    def reset_game(self):
        self.bet = 0
        self.bet_label.config(text="Bet: $0")
        self.player_hand = []
        self.dealer_hand = []
        self.update_hand_labels(show_dealer_first_card=True)
        new_power_up = award_power_up()
        if new_power_up:
            self.player_power_ups.append(new_power_up)
            messagebox.showinfo("Power-up", f"Congratulations! You have earned a power-up: {new_power_up}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackJackApp(root)
    root.mainloop()