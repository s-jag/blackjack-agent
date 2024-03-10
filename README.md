# blackjack-agent
Blackjack Agent


## Strategy 1: Perfect Basic Strategy

**Description**: This strategy involves making decisions based solely on the player's hand and the dealer's up card, following a set of predefined rules that aim to minimize the house edge without any card counting.

**Decisions**:
- **Hard Totals**: The strategy dictates specific actions (hit, stand, double down, or split) based on the total value of the hand and the dealer's up card.
- **Soft Totals**: Decisions for hands containing an Ace valued as 11, considering the flexibility of the Ace's value.
- **Splits**: Guidelines for splitting pairs, which may vary depending on the pair and the dealer's up card.
- **Doubling Down**: Identifies opportunities to double the initial bet, based on the player's hand and the dealer's visible card.

#### Hard Totals:
- **8 or less**: Always hit.
- **9**: Double down if the dealer has 3 through 6, otherwise hit.
- **10**: Double down if the dealer has 2 through 9, otherwise hit.
- **11**: Double down if the dealer has 2 through 10, hit if the dealer has an Ace.
- **12**: Stand if the dealer has 4 through 6, otherwise hit.
- **13-16**: Stand if the dealer has 2 through 6, otherwise hit.
- **17-21**: Always stand.

#### Soft Totals:
- **A,2 or A,3**: Double down if the dealer has 5 or 6, otherwise hit.
- **A,4 or A,5**: Double down if the dealer has 4 through 6, otherwise hit.
- **A,6**: Double down if the dealer has 3 through 6, otherwise hit.
- **A,7**: Stand if the dealer has 2, 7, or 8. Double down if the dealer has 3 through 6, otherwise hit.
- **A,8 or A,9**: Always stand.
- **A,10**: Always stand (this is a blackjack and automatically wins unless the dealer also has a blackjack).

#### Splits:
- **2's and 3's**: Split if the dealer has 2 through 7, otherwise hit.
- **4's**: Never split.
- **5's**: Treat as a total of 10 and double down if the dealer has 2 through 9, otherwise hit.
- **6's**: Split if the dealer has 2 through 6, otherwise hit.
- **7's**: Split if the dealer has 2 through 7, otherwise hit.
- **8's**: Always split.
- **9's**: Split if the dealer has 2 through 6, 8, or 9. Stand if the dealer has 7, 10, or Ace.
- **10's (Jacks, Queens, Kings)**: Never split.
- **Aces**: Always split.

#### Doubling Down:
- Highlighted within the Hard and Soft totals sections. The general principle is to double down to maximize winnings when the player has a strong hand and the dealer has a hand likely to lead to a bust.




## Strategy 2: Perfect Basic Strategy with 3 Classes (-1, 0, +1)

**Description**: This strategy enhances the Perfect Basic Strategy by incorporating a simple card counting system. It divides cards into three classes (-1, 0, +1) based on their values, keeping a running count and adjusting decisions using the true count (the running count divided by the number of decks remaining).

**Decisions**:
- **Running Count**: Keep a tally of the cards played, adding or subtracting based on their assigned class (-1, 0, +1).
- **True Count Calculation**: Divide the running count by the number of decks remaining to adjust the strategy for deck penetration.
- **Bet Sizing**: Adjust the bet size based on the true count, with higher bets placed when the count is favorable.
- **Strategy Adjustments**: Make strategic deviations from the Perfect Basic Strategy based on the true count, such as taking insurance, altering play for certain hands, or changing split and double down decisions.

## Strategy 3: Complete Card Counting

**Description**: This advanced strategy involves keeping a precise count of all cards seen, using more complex systems that can track aces, tens, and other cards separately. This approach aims to provide a comprehensive advantage over the house by making highly informed decisions on betting, playing, and insurance.

**Decisions**:
- **Card Counting System**: Implement a detailed card counting system (e.g., Hi-Lo, KO, Omega II) that assigns different values to different cards.
- **Ace Tracking**: Pay special attention to the flow of Aces, adjusting betting and playing decisions based on the likelihood of receiving a natural blackjack.
- **Betting Strategy**: Adjust the size of bets more precisely based on the count, with potential for aggressive changes when the count is highly favorable.
- **Play Variations**: Make nuanced adjustments to playing decisions, potentially including changes to hit/stand decisions, doubling strategies, and splitting rules based on the count.
- **Insurance Decisions**: Make informed decisions about taking insurance against the dealer's Ace, based on the count and the adjusted odds of the dealer having a blackjack.




