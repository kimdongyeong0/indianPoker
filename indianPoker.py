import indianPokerUtil as util
import random

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Algorithm" modification parts where "Participants" have to modify  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Any modification is allowed, if needed add methods to make your algorithm more perfect!
# There are "c" values, which stands for card choice, and "b" values, which stands for bet choice.
# Please modify these values to strategically win the game!

# Rules are exactly same with that of "Indian Poker", except you get to choose your own card, and you are not supposed to know the card on the other hand.

# @@@@@@@@@@@@@@@@@@ RULES @@@@@@@@@@@@@@@@@@
# 1. Each players will choose a card to represent
# 2. Each players will be able to bet based on their cards.
# 3. If bets given are different, one with the lower bets have three options of action
#   3.1. One can decide to give up or not
#   3.2. One can decide to call the bet, and the card reveal will start to begin
#   3.3. One can decide to raise the bet, and the other one has to repeat #3 until they run out of the points in possession.
# 4. Bets are now matched, reveal the cards, and judge who won the current round.
# 5. Repeat the procedure until one's card run out or one's point run out.

# @@@@@@@@@@@@@@@@@@ 게임규칙 @@@@@@@@@@@@@@@@@@
# 1. 각 플레이어는 대표할 카드를 선택합니다.
# 2. 각 플레이어는 자신의 카드를 기반으로 베팅할 수 있습니다.
# 3. 베팅 금액이 다를 경우, 베팅 금액이 낮은 쪽은 세 가지 옵션 중 하나를 선택할 수 있습니다.
#   3.1. 포기할지 여부를 결정할 수 있습니다.
#   3.2. 베팅에 응하고 카드 공개가 시작됩니다.
#   3.3. 베팅을 올릴 수 있고, 상대방은 소유 포인트가 소진될 때까지 #3을 반복해야 합니다.
# 4. 베팅이 일치하면 카드를 공개하고 현재 라운드에서 승리한 플레이어를 결정합니다.
# 5. 카드 또는 포인트가 소진될 때까지 규칙을 반복합니다.

# @@@@@@@@@@@@@@@@@@ Methods @@@@@@@@@@@@@@@@@@@@
# 1. pvp: person vs person
# 2. pvai: person vs ai
# 3. aivai: ai vs ai (algorithm vs algorithm)
# 4. quit: quit

# @@@@@@@@@@@@@@@@@@ 커맨드 @@@@@@@@@@@@@@@@@@@@@@
# 1. pvp: 사람 vs 사람
# 2. pvai: 사람 vs AI
# 3. aivai: AI vs AI (알고리즘 vs 알고리즘)
# 4. quit: 종료

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Algorithm" modification parts where "Participants" have to modify  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# @@@@@@@@@@@@@@@@@@ Extra @@@@@@@@@@@@@@@@@@@@@@
# If none of these are understandable, please see "aivai" part in main methods
# CMD + F or Ctrl + F -> type mode == 'aivai' -> second one


# @TODO: class Algorithm is for you to modify in order to make the strongest algorithm ever.
class Algorithm:
    def __init__(self):
        self.deck = [i for i in range(1, 11)]
        self.deck = 2 * self.deck
        self.point = 100
        self.history = []
        self.current_card = None

    def pick(self) -> int:
        if not self.deck:
            return -1  # No cards left
        card = random.choice(self.deck)
        self.deck.remove(card)
        self.history.append(card)
        self.current_card = card
        return card

    def giveUp(self, currentBet) -> bool:
        card = self.history[-1] if self.history else -1
        if card < 4 and currentBet > 5:
            return True
        elif card < 7 and currentBet > 8:
            return True
        else:
            return False

    def raiseBet(self, currentBet) -> int:
        card = self.current_card if self.current_card else -1
        additional_bet = min(self.point, random.randint(1, 4))
        finalBet = currentBet + additional_bet
        self.point -= additional_bet
        return finalBet

    def bet(self) -> int:
        card = self.pick()
        if card == -1:
            return 0
        if card > 8:
            currentBet = random.randint(7, 13)
        elif card > 6:
            currentBet = random.randint(4, 8)
        elif card > 3:
            currentBet = random.randint(2, 5)
        else:
            currentBet = random.randint(1, 3)
        self.point -= currentBet
        return currentBet

    def update_strategy(self, result, opponent_bet):
        if result == "win":
            for i, card in enumerate(self.history):
                if card > 7:
                    self.deck.append(card)
                elif card > 4:
                    self.deck.append(card)
        elif result == "lose":
            for i, card in enumerate(self.history):
                if card < 4 and opponent_bet > 5:
                    if card in self.deck:
                        self.deck.remove(card)
                elif card < 7 and opponent_bet > 8:
                    if card in self.deck:
                        self.deck.remove(card)
        self.history = []
        self.current_card = None


if __name__ == "__main__":
    util.main()

    # Test Algorithm
    # util.test()
