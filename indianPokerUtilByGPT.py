import random
import numpy as np


class Player:
    def __init__(self):
        self.deck = [i for i in range(1, 11)] * 2
        self.point = 100

    def call(self, bet, currentBet):
        additionalBet = bet - currentBet
        self.point -= additionalBet
        return bet

    def move(self, card):
        try:
            if int(card) in self.deck:
                return self.deck.pop(self.deck.index(int(card)))
        except:
            return None


class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.alpha = 0.1  # learning rate
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


class Algorithm:
    def __init__(self):
        self.deck = [i for i in range(1, 11)] * 2
        self.point = 100
        self.state_size = 100  # Example state size, modify based on actual state space
        self.action_size = 2  # For simplicity: 0 = low bet, 1 = high bet
        self.agent = QLearningAgent(self.state_size, self.action_size)

    def get_state(self):
        deck_sum = sum(self.deck)
        return deck_sum

    def pick(self) -> int:
        state = self.get_state()
        action = self.agent.act(state)
        if action == 0:
            card = self.deck.pop(random.randint(0, len(self.deck) - 1))
        else:
            card = self.deck.pop(self.deck.index(max(self.deck)))
        return card

    def giveUp(self, currentBet) -> bool:
        state = self.get_state()
        action = self.agent.act(state)
        return action == 0

    def raiseBet(self, currentBet) -> int:
        state = self.get_state()
        action = self.agent.act(state)
        if action == 0:
            return int(1.5 * currentBet)
        else:
            return currentBet

    def bet(self) -> int:
        state = self.get_state()
        action = self.agent.act(state)
        if action == 0:
            return 10
        else:
            return 20


clearBoard = "\n\n\n\n\n\n\n\n\n" * 100


def main():
    print("Starting Indian Poker Game! \n\nPlease Choose the mode of the game!")

    while True:
        mode = input("Given Options are: pvp, pvai, aivai, quit: ").lower()
        while mode not in ["pvp", "pvai", "aivai", "quit"]:
            mode = input("Wrong choice, please choose between pvp, pvai, aivai, quit: ")

        if mode == "pvp":
            print("\n\n @@@ Starting PvP mode... @@@")
            p1 = Player()
            p2 = Player()

            for i in range(20):
                c1 = input(
                    "Player1's turn to choose card, which card do you wish to pick? (1-10): "
                )
                f1 = p1.move(c1)
                while c1 not in [str(i) for i in range(1, 11)] or f1 is None:
                    if f1 is None:
                        c1 = input(
                            "The Card you are trying to pull does not exist, please choose again, (1-10): "
                        )
                        f1 = p1.move(c1)
                        continue
                    c1 = input(
                        "You have chosen the wrong card, please choose the right card, (1-10): "
                    )

                print(clearBoard + "Player1 has successfully chosen the card")

                c2 = input(
                    "Player2's turn to choose card, which card do you wish to pick? (1-10): "
                )
                f2 = p2.move(c2)
                while c2 not in [str(i) for i in range(1, 11)] or f2 is None:
                    if f2 is None:
                        c2 = input(
                            "The Card you are trying to pull does not exist, please choose again, (1-10): "
                        )
                        f2 = p2.move(c2)
                        continue
                    c2 = input(
                        "You have chosen the wrong card, please choose the right card, (1-10): "
                    )

                print(clearBoard + "Player2 has successfully chosen the card")

                print(
                    "It is now time to bet. Please bet accordingly with strategies.\nOnce the amounts of the bets are equivalent, final judgement will be beginning."
                )
                b1 = int(input("Player1's turn to bet: "))
                while b1 > p1.point:
                    b1 = int(
                        input(
                            "You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(
                                p1.point
                            )
                        )
                    )
                p1.point -= b1

                b2 = int(input("Player2's turn to bet: "))
                while b2 > p2.point:
                    b2 = int(
                        input(
                            "You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(
                                p2.point
                            )
                        )
                    )
                p2.point -= b2

                while b1 != b2:
                    print(
                        "\n\nAmounts of the betting are different, starting raise and call session.\nHighest Bet: {}".format(
                            max(b1, b2)
                        )
                    )
                    if b1 < b2:
                        print(
                            "\nPlayer1's bet is lower than that of Player2. Player1, would you like to bet more?"
                        )
                        d1 = input(
                            "No means that you are giving up. You will automatically lose. (Y / N): "
                        ).upper()
                        while d1 != "Y" and d1 != "N":
                            d1 = input("Wrong choice, Please try again: ").upper()
                        if d1 == "Y":
                            cob1 = input("Call or Bet? (c / b): ").lower()
                            if cob1 == "c":
                                b1 = p1.call(b2, b1)
                            else:
                                p1.point += b1
                                b1 = int(input("Player1's turn to bet: "))
                                while b1 > p1.point:
                                    b1 = int(
                                        input(
                                            "You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(
                                                p1.point
                                            )
                                        )
                                    )
                                p1.point -= b1
                        else:
                            print("Player1 gave up.")
                            f1 = -1
                            break
                    else:
                        print(
                            "\nPlayer2's bet is lower than that of Player1. Player2, would you like to bet more?"
                        )
                        d2 = input(
                            "No means that you are giving up. You will automatically lose. (Y / N): "
                        ).upper()
                        while d2 != "Y" and d2 != "N":
                            d2 = input("Wrong choice, Please try again: ").upper()
                        if d2 == "Y":
                            cob2 = input("Call or Bet? (c / b): ").lower()
                            if cob2 == "c":
                                b2 = p2.call(b1, b2)
                            else:
                                p2.point += b2
                                b2 = int(input("Player2's turn to bet: "))
                                while b2 > p2.point:
                                    b2 = int(
                                        input(
                                            "You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(
                                                p2.point
                                            )
                                        )
                                    )
                                p2.point -= b2
                        else:
                            print("Player2 gave up.")
                            f2 = -1
                            break

                print("\n\n")
                if f1 > f2:
                    print("Player1 wins!")
                    p1.point += b1 + b2
                elif f1 < f2:
                    print("Player2 wins!")
                    p2.point += b1 + b2
                else:
                    print("Draw...")
                    p1.point += b1
                    p2.point += b2

                print("\nYour cards were: Player1: {}, Player2: {}".format(f1, f2))

                if p1.point == 0:
                    print(
                        "Player1 has lost all his / her points!\nPlayer2 has won the game!!!\n\n"
                    )
                    break
                elif p2.point == 0:
                    print(
                        "Player2 has lost all his / her points!\nPlayer1 has won the game!!!\n\n"
                    )
                    break

                print(
                    "\nCurrent Point: Player1: {}, Player2: {}".format(
                        p1.point, p2.point
                    )
                )

            if p1.point > p2.point:
                print("@@@@@@@ Player1 won!! @@@@@@@")
            elif p1.point < p2.point:
                print("@@@@@@@ Player2 won!! @@@@@@@")
            else:
                print("@@@@@@@ Draw!! @@@@@@@")

        elif mode == "pvai":
            p1 = Player()
            p2 = Algorithm()
            print("Starting PvAI mode...")
            for i in range(20):
                c1 = input(
                    "Player1's turn to choose card, which card do you wish to pick? (1-10): "
                )
                f1 = p1.move(c1)
                while c1 not in [str(i) for i in range(1, 11)] or f1 is None:
                    if f1 is None:
                        c1 = input(
                            "The Card you are trying to pull does not exist, please choose again, (1-10): "
                        )
                        f1 = p1.move(c1)
                        continue
                    c1 = input(
                        "You have chosen the wrong card, please choose the right card, (1-10): "
                    )

                print(clearBoard + "Player1 has successfully chosen the card")

                c2 = p2.pick()
                f2 = int(c2)

                print(
                    "It is now time to bet. Please bet accordingly with strategies.\nOnce the amounts of the bets are equivalent, final judgement will be beginning."
                )
                b1 = int(input("Player1's turn to bet: "))
                while b1 > p1.point:
                    b1 = int(
                        input(
                            "You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(
                                p1.point
                            )
                        )
                    )
                p1.point -= b1

                print("AI will choose its betting...")
                b2 = p2.bet()

                while b1 != b2:
                    print(
                        "\n\nAmounts of the betting are different, starting raise and call session.\nHighest Bet: {}".format(
                            max(b1, b2)
                        )
                    )
                    if b1 < b2:
                        print(
                            "\nPlayer1's bet is lower than that of Player2. Player1, would you like to bet more?"
                        )
                        d1 = input(
                            "No means that you are giving up. You will automatically lose. (Y / N): "
                        ).upper()
                        while d1 != "Y" and d1 != "N":
                            d1 = input("Wrong choice, Please try again: ").upper()
                        if d1 == "Y":
                            cob1 = input("Call or Bet? (c / b): ").lower()
                            if cob1 == "c":
                                b1 = p1.call(b2, b1)
                            else:
                                p1.point += b1
                                b1 = int(input("Player1's turn to bet: "))
                                while b1 > p1.point:
                                    b1 = int(
                                        input(
                                            "You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(
                                                p1.point
                                            )
                                        )
                                    )
                                p1.point -= b1
                        else:
                            print("Player1 gave up.")
                            f1 = -1
                            break
                    else:
                        if not p2.giveUp(b1):
                            p2.point += b2
                            b2 = p2.raiseBet(b1)
                        else:
                            print("AI has given up.")
                            f2 = -1
                            break

                print("\n\n")
                if f1 > f2:
                    print("Player1 wins!")
                    p1.point += b1 + b2
                elif f1 < f2:
                    print("AI wins!")
                    p2.point += b1 + b2
                else:
                    print("Draw...")
                    p1.point += b1
                    p2.point += b2

                print("\nYour cards were: Player1: {}, AI: {}".format(f1, f2))

                if p1.point <= 0:
                    print(
                        "Player1 has lost all his / her points!\nAI has won the game!!!\n\n"
                    )
                    break
                elif p2.point <= 0:
                    print(
                        "AI has lost all his / her points!\nPlayer has won the game!!!\n\n"
                    )
                    break

                print("\nCurrent Point: Player1: {}, AI: {}".format(p1.point, p2.point))

        elif mode == "aivai":
            p1 = Algorithm()
            p2 = Algorithm()
            print("Starting AIvAI mode...")
            for i in range(20):
                f1 = int(p1.pick())
                f2 = int(p2.pick())

                b1 = int(p1.bet())
                b2 = int(p2.bet())
                while b1 != b2:
                    if b1 < b2:
                        if not p1.giveUp(b2):
                            p1.point += b1
                            b1 = p1.raiseBet(b2)
                        else:
                            print("AI1 has given up.")
                            f1 = -1
                            break
                    else:
                        if not p2.giveUp(b1):
                            p2.point += b2
                            b2 = p2.raiseBet(b1)
                        else:
                            print("AI2 has given up.")
                            f2 = -1
                            break

                print("\n\n")
                if f1 > f2:
                    print("AI1 wins!")
                    p1.point += b1 + b2
                elif f1 < f2:
                    print("AI2 wins!")
                    p2.point += b1 + b2
                else:
                    print("Draw...")
                    p1.point += b1
                    p2.point += b2

                print("\nYour cards were: AI1: {}, AI2: {}\n".format(f1, f2))

                if p1.point <= 0:
                    print(
                        "AI1 has lost all his / her points!\nAI2 has won the game!!!\n\n"
                    )
                    break
                elif p2.point <= 0:
                    print(
                        "AI2 has lost all his / her points!\nAI1 has won the game!!!\n\n"
                    )
                    break

                print("\nCurrent Point: AI1: {}, AI2: {}\n".format(p1.point, p2.point))

            if p1.point > p2.point:
                print("Finally, AI1 has won the game!!!\n\n")
            elif p2.point > p1.point:
                print("Finally, AI2 has won the game!!!\n\n")
            print("Final Point: AI1: {}, AI2: {}\n".format(p1.point, p2.point))

        elif mode.lower() == "quit":
            print("\nThank you for playing the game! Come again!")
            break


if __name__ == "__main__":
    main()
