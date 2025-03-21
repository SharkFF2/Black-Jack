import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import time

# Numbers and suits
suits = ['♥', '♦', '♠', '♣']
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
        self.root.geometry("800x600")  # Set the window size
        self.root.resizable(True, True)  # Allow window resizing
        self.player_money = 100
        self.bet = 0
        self.player_hand = []
        self.dealer_hand = []
        self.player_power_ups = []

        self.setup_ui()

    def setup_ui(self):
        # Create a style
        style = ttk.Style()
        style.configure("TFrame", background="#2E8B57")
        style.configure("TLabel", background="#2E8B57", foreground="white", font=("Helvetica", 14))
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TEntry", font=("Helvetica", 12), padding=6)
        style.configure("Large.TLabel", background="#2E8B57", foreground="white", font=("Helvetica", 18, "bold"))
        style.configure("Hand.TLabel", background="#2E8B57", foreground="white", font=("Helvetica", 20, "bold"))

        # Create frames for better organization
        self.top_frame = ttk.Frame(self.root, style="TFrame")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.middle_frame = ttk.Frame(self.root, style="TFrame")
        self.middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.bottom_frame = ttk.Frame(self.root, style="TFrame")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Top frame widgets
        self.money_label = ttk.Label(self.top_frame, text=f"💰 Money: ${self.player_money}", style="Large.TLabel")
        self.money_label.pack(side=tk.LEFT, padx=10)

        self.bet_label = ttk.Label(self.top_frame, text="💵 Bet: $0", style="Large.TLabel")
        self.bet_label.pack(side=tk.RIGHT, padx=10)

        # Middle frame widgets
        self.canvas = tk.Canvas(self.middle_frame, bg="#2E8B57", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        # Bottom frame widgets
        self.bet_entry = ttk.Entry(self.bottom_frame, style="TEntry")
        self.bet_entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.bet_button = ttk.Button(self.bottom_frame, text="Place Bet", command=self.place_bet, style="TButton")
        self.bet_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.hit_button = ttk.Button(self.bottom_frame, text="Hit", command=self.hit, style="TButton")
        self.hit_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.stand_button = ttk.Button(self.bottom_frame, text="Stand", command=self.stand, style="TButton")
        self.stand_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.power_up_button = ttk.Button(self.bottom_frame, text="Use Power-up", command=self.use_power_up, style="TButton")
        self.power_up_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.reset_button = ttk.Button(self.bottom_frame, text="Reset", command=self.reset_game, style="TButton")
        self.reset_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Configure grid weights for bottom frame
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

    def on_resize(self, event):
        self.update_hand_labels(show_dealer_first_card=True)

    def place_bet(self):
        try:
            self.bet = int(self.bet_entry.get())
            if self.bet > self.player_money:
                messagebox.showerror("Error", "You don't have enough money to place that bet.")
            else:
                self.player_money -= self.bet
                self.money_label.config(text=f"💰 Money: ${self.player_money}")
                self.bet_label.config(text=f"💵 Bet: ${self.bet}")
                self.start_game()
        except ValueError:
            messagebox.showerror("Error", "Invalid bet amount.")

    def start_game(self):
        self.player_hand = [deck.pop(), deck.pop()]
        self.dealer_hand = [deck.pop(), deck.pop()]
        self.update_hand_labels(show_dealer_first_card=True)

    def update_hand_labels(self, show_dealer_first_card=False):
        self.canvas.delete("all")
        player_y = self.canvas.winfo_height() - 200  # Adjusted padding
        if player_y < 200:
            player_y = self.canvas.winfo_height() // 2 + 50
        self.draw_hand(self.player_hand, self.canvas.winfo_width() // 2, player_y, "Player's Hand")
        if show_dealer_first_card:
            self.draw_hand([self.dealer_hand[0]], self.canvas.winfo_width() // 2, 100, "Dealer's Hand")
        else:
            self.draw_hand(self.dealer_hand, self.canvas.winfo_width() // 2, 100, "Dealer's Hand")

    def draw_hand(self, hand, x, y, label):
        self.canvas.create_text(x, y - 20, text=label, fill="white", font=("Helvetica", 16, "bold"))
        card_width = self.canvas.winfo_width() // 10
        card_height = card_width * 1.5
        spacing = card_width // 3
        total_width = len(hand) * (card_width + spacing) - spacing
        start_x = x - total_width // 2
        for i, card in enumerate(hand):
            self.canvas.create_rectangle(start_x + i * (card_width + spacing), y, start_x + i * (card_width + spacing) + card_width, y + card_height, fill="white")
            self.canvas.create_text(start_x + i * (card_width + spacing) + card_width // 2, y + card_height // 2, text=f"{card['rank']}\n{card['suit']}", font=("Helvetica", int(card_width // 3)))

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

        self.money_label.config(text=f"💰 Money: ${self.player_money}")
        if self.player_money <= 0:
            self.reset_money()
        else:
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
        self.bet_label.config(text="💵 Bet: $0")
        self.player_hand = []
        self.dealer_hand = []
        self.update_hand_labels(show_dealer_first_card=True)
        new_power_up = award_power_up()
        if new_power_up:
            self.player_power_ups.append(new_power_up)
            messagebox.showinfo("Power-up", f"Congratulations! You have earned a power-up: {new_power_up}")

    def reset_money(self):
        self.player_money = 100
        self.money_label.config(text=f"💰 Money: ${self.player_money}")
        messagebox.showinfo("Out of Money", "You ran out of money! Your money has been reset to $100.")
        self.reset_game()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackJackApp(root)
    root.mainloop()