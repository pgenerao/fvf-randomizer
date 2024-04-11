import os
import random
import yaml

MAX_HAND_COST = 50
MIN_HAND_SIZE = 25

PROBABILITY_OF_ADDING_ONE_MORE_CARD = .66

with open("cards.yaml") as stream:
    try:
        # Import cards w/ costs data from yaml file.
        cards_details = yaml.safe_load(stream)[0]["cards"]

        # Create deck and hand variables.
        deck = list(cards_details.keys())
        hand = []

        valid_hand = False
        
        # Try out different hands by randomly choosing cards.
        while(not valid_hand):
            deck_copy = deck.copy()
            
            hand_candidate = []
            hand_candidate_cost = 0

            # Run trial (pull random cards and see if it forms a valid hand)
            while(len(deck_copy) > 0):
                # Draw a card from the deck
                new_card = random.choice(deck_copy)
                deck_copy.remove(new_card)

                new_card_cost = cards_details[new_card]["cost"]

                # Check if the new card can fit into the hand

                # Case 1: We don't have enough cards => Take this card.
                if new_card_cost + hand_candidate_cost <= MAX_HAND_COST and len(hand_candidate) < MIN_HAND_SIZE:
                    hand_candidate.append(new_card)
                    hand_candidate_cost += new_card_cost
                
                # Case 2: We have enough cards => Take this card with a probability p. If we don't take this card, stop
                #         drawing cards.
                elif new_card_cost + hand_candidate_cost <= MAX_HAND_COST and len(hand_candidate) >= MIN_HAND_SIZE:
                    if random.random() <= PROBABILITY_OF_ADDING_ONE_MORE_CARD:
                        hand_candidate.append(new_card)
                        hand_candidate_cost += new_card_cost
                    else:
                        break
            
            # Check to see if the hand we have is valid.
            if(len(hand_candidate) >= MIN_HAND_SIZE and hand_candidate_cost <= MAX_HAND_COST):
                hand = hand_candidate
                valid_hand = True
        
        # Sort hand by type and then cost.
        hand.sort(key=lambda card: -cards_details[card]["cost"])
        hand.sort(key=lambda card: cards_details[card]["type"])

        # Print resulting hand.
        total_cost = 0

        # Print every card and tally up the cost.
        for card in hand:
            card_cost = cards_details[card]["cost"]
            card_type = cards_details[card]["type"]

            print(f"{card_type}\t\t{card} ({card_cost})")

            total_cost += card_cost

        # Print the total cost of the hand and the size of the hand
        term_size = os.get_terminal_size()
        print('-' * term_size.columns)  # Print line

        print(f"Total Cost: {total_cost}")
        print(f"Hand Size: {len(hand)}")

        print('-' * term_size.columns)  # Print line

    except yaml.YAMLError as e:
        print(e)