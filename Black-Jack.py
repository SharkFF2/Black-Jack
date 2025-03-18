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

def display_hand(player, hand):
    print(f"{player}'s hand: " + ', '.join([f"{card['rank']} of {card['suit']}" for card in hand]) +
          f" (Total: {calculate_hand(hand)})")

def blackjack():
    print("Welcome to Blackjack!")
    player_money = 100  # Initial money for the player
    max_money = player_money  # Track the maximum money the player had

    while True:
        if player_money <= 0:
            print("You are out of money! Game over.")
            while True:
                buy_chips = input("Do you want to buy more chips? (yes/no): ").lower()
                if buy_chips in ['yes', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
            if buy_chips == 'yes':
                max_buyable_chips = max_money // 2
                print(f"You can buy up to ${max_buyable_chips} worth of chips.")
                while True:
                    try:
                        additional_chips = int(input(f"Enter the amount of chips to buy (max ${max_buyable_chips}): "))
                        if additional_chips > max_buyable_chips:
                            print(f"You can't buy more than ${max_buyable_chips} worth of chips.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                player_money += additional_chips
            else:
                break

        print(f"\nYou have ${player_money}.")
        while True:
            try:
                bet = int(input("Place your bet: "))
                if bet > player_money:
                    print("You don't have enough money to place that bet.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        if len(deck) < 10:
            print("Reshuffling the deck...")
            deck.extend(create_deck())

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        display_hand("Player", player_hand)
        print(f"Dealer's first card: {dealer_hand[0]['rank']} of {dealer_hand[0]['suit']}")

        while True:
            action = input("Choose an action: [H]it, [S]tand, [D]ouble, [P]Split (WIP): ").lower()

            if action == 'h':
                player_hand.append(deck.pop())
                display_hand("Player", player_hand)

                if calculate_hand(player_hand) > 21:
                    print("Player busts! Dealer wins.")
                    player_money -= bet
                    break
            elif action == 's':
                break
            elif action == 'd':
                if bet * 2 > player_money:
                    print("You don't have enough money to double down.")
                    continue
                player_money -= bet  # Deduct the original bet first
                bet *= 2
                player_hand.append(deck.pop())
                display_hand("Player", player_hand)

                if calculate_hand(player_hand) > 21:
                    print("Player busts! Dealer wins.")
                    player_money -= bet
                break
            elif action == 'p':
                print("Split is not implemented yet.")
            else:
                print("Invalid input. Please enter 'h', 's', 'd', or 'p'.")

        if calculate_hand(player_hand) <= 21:
            # Dealer's turn
            display_hand("Dealer", dealer_hand)
            while calculate_hand(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                display_hand("Dealer", dealer_hand)

            # Determine the winner
            player_score = calculate_hand(player_hand)
            dealer_score = calculate_hand(dealer_hand)

            if dealer_score > 21 or player_score > dealer_score:
                print("Player wins!")
                player_money += bet
            elif player_score == dealer_score:
                print("Push! (tie)")
            else:
                print("Dealer wins!")
                player_money -= bet

        # Update the maximum money the player had
        if player_money > max_money:
            max_money = player_money

blackjack()

# Ask the player if they want to play again
while True:
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again == 'yes':
        blackjack()
    elif play_again == 'no':
        print("Thanks for playing! Goodbye.")
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'.") 

    def advanced_dealer_strategy(dealer_hand):
        while True:
            dealer_score = calculate_hand(dealer_hand)
            if dealer_score < 17:
                dealer_hand.append(deck.pop())
                display_hand("Dealer", dealer_hand)
                time.sleep(1)  # Adding delay to make it feel more realistic
            elif dealer_score == 17 and any(card['rank'] == 'A' for card in dealer_hand):
                dealer_hand.append(deck.pop())
                display_hand("Dealer", dealer_hand)
                time.sleep(1)  # Adding delay to make it feel more realistic
            else:
                break

    # Replace the dealer's turn logic in the blackjack function with the advanced dealer strategy
    def blackjack():
        print("Welcome to Blackjack!")
        player_money = 100  # Initial money for the player
        max_money = player_money  # Track the maximum money the player had

        while True:
            if player_money <= 0:
                print("You are out of money! Game over.")
                while True:
                    buy_chips = input("Do you want to buy more chips? (yes/no): ").lower()
                    if buy_chips in ['yes', 'no']:
                        break
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                if buy_chips == 'yes':
                    max_buyable_chips = max_money // 2
                    print(f"You can buy up to ${max_buyable_chips} worth of chips.")
                    while True:
                        try:
                            additional_chips = int(input(f"Enter the amount of chips to buy (max ${max_buyable_chips}): "))
                            if additional_chips > max_buyable_chips:
                                print(f"You can't buy more than ${max_buyable_chips} worth of chips.")
                                continue
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    player_money += additional_chips
                else:
                    break

            print(f"\nYou have ${player_money}.")
            while True:
                try:
                    bet = int(input("Place your bet: "))
                    if bet > player_money:
                        print("You don't have enough money to place that bet.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            if len(deck) < 10:
                print("Reshuffling the deck...")
                deck.extend(create_deck())

            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            display_hand("Player", player_hand)
            print(f"Dealer's first card: {dealer_hand[0]['rank']} of {dealer_hand[0]['suit']}")

            while True:
                action = input("Choose an action: [H]it, [S]tand, [D]ouble, [P]Split (WIP): ").lower()

                if action == 'h':
                    player_hand.append(deck.pop())
                    display_hand("Player", player_hand)

                    if calculate_hand(player_hand) > 21:
                        print("Player busts! Dealer wins.")
                        player_money -= bet
                        break
                elif action == 's':
                    break
                elif action == 'd':
                    if bet * 2 > player_money:
                        print("You don't have enough money to double down.")
                        continue
                    player_money -= bet  # Deduct the original bet first
                    bet *= 2
                    player_hand.append(deck.pop())
                    display_hand("Player", player_hand)

                    if calculate_hand(player_hand) > 21:
                        print("Player busts! Dealer wins.")
                        player_money -= bet
                    break
                elif action == 'p':
                    print("Split is not implemented yet.")
                else:
                    print("Invalid input. Please enter 'h', 's', 'd', or 'p'.")

            if calculate_hand(player_hand) <= 21:
                # Dealer's turn using advanced strategy
                display_hand("Dealer", dealer_hand)
                advanced_dealer_strategy(dealer_hand)

                # Determine the winner
                player_score = calculate_hand(player_hand)
                dealer_score = calculate_hand(dealer_hand)

                if dealer_score > 21 or player_score > dealer_score:
                    print("Player wins!")
                    player_money += bet
                elif player_score == dealer_score:
                    print("Push! (tie)")
                else:
                    print("Dealer wins!")
                    player_money -= bet

            # Update the maximum money the player had
            if player_money > max_money:
                max_money = player_money

    blackjack()

    # Ask the player if they want to play again
    while True:
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == 'yes':
            blackjack()
        elif play_again == 'no':
            print("Thanks for playing! Goodbye.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")