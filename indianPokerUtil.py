import random

class Player:
    def __init__(self):
        self.deck = [i for i in range(1,11)]
        self.deck = 2 * self.deck
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

# sample AI from Sol Choi / (semi) Greedy algorithm / @@@@@@@@@ can be ignored @@@@@@@@@
class AI:
    def __init__(self):
        self.deck = [i for i in range(1,11)]
        self.deck = 2 * self.deck
        self.deck.sort()
        self.point = 100
        self.picked = 0
        
    # Pick cards strategically
    def pick(self):
        card = 0
        if self.point >= 70:
            rng = len(self.deck) - 6
            if rng >= 0:
                card = self.deck.pop(random.randint(0, rng))
            else:
                # print(self.deck)
                card = self.deck.pop(random.randint(0, len(self.deck)-1))
            self.picked = int(card) 
        else:
            card = self.deck.pop(self.deck.index(max(self.deck)))
            self.picked = card
        # print("Card picked:", card)
        return card
    
    # Decide giving up or not
    def giveUp(self, currentBet):
        if int(0.9 * currentBet) > self.point:
            if self.picked > 8:
                return False
            return True
        else:
            if self.picked <= 2:
                return True
            return False
    
    # Decide raise or give up
    def raiseBet(self, currentBet):
        f = random.randint(0,1)
        if f:
            final = int(1.5 * currentBet)
            if self.point >= final:
                self.point -= final
                return final
            elif currentBet > self.point:
                self.point -= currentBet
                return currentBet
            else: # Dangerous situation
                if self.picked <= 7:
                    self.point -= currentBet
                    return currentBet
                temp = self.point
                self.point = 0
                return temp
        else:
            self.point -= currentBet
            return currentBet
    
    # Bet according to the cards
    def bet(self):
        temp = self.point
        if self.point <= 10:
            self.point -= temp
            return temp
        
        if self.picked in [1,2,3]:
            self.point -= 10
            return 10
        
        elif self.picked in [4,5,6,7]:
            
            if temp <= 20:
                self.point = 0
                return temp
            
            while self.point - temp <= 0:
                temp = random.randint(2, 3) * 10
            self.point -= temp
            return temp
        
        else:
            
            if temp <= 30:
                self.point = 0
                return temp
            
            while self.point - temp <= 0:
                temp = random.randint(3, 5) * 10
            self.point -= temp
            return temp

clearBoard = '\n\n\n\n\n\n\n\n\n' * 100

def main():
    print("Starting Indian Poker Game! \n\nPlease Choose the mode of the game!")
    
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Game Starts @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    while True:
        mode = input("Given Options are: pvp, pvai, aivai, quit: ").lower()
        while mode not in ['pvp', 'pvai', 'aivai', 'quit']:
            mode = input("Wrong choice, please choose between pvp, pvai, aivai, quit: ")
        
        if mode == 'pvp':
            print("\n\n @@@ Starting PvP mode... @@@")
            p1 = Player()
            p2 = Player()
            
            for i in range(20):
                # @@@@@@@@ Card choosing phase @@@@@@@@@@
                c1 = input("Player1's turn to choose card, which card do you wish to pick? (1-10): ")
                f1 = p1.move(c1)
                while c1 not in [str(i) for i in range(1, 11)] or f1 == None:
                    if f1 == None:
                        c1 = input("The Card you are trying to pull does not exist, please choose again, (1-10): ")
                        f1 = p1.move(c1)
                        continue
                    c1 = input("You have chosen the wrong card, please choose the right card, (1-10): ")
                
                print(clearBoard + "Player1 has successfully chosen the card")
                
                c2 = input("Player2's turn to choose card, which card do you wish to pick? (1-10): ")
                f2 = p2.move(c2)
                while c2 not in [str(i) for i in range(1, 11)] or f2 == None:
                    if f2 == None:
                        c2 = input("The Card you are trying to pull does not exist, please choose again, (1-10): ")
                        f2 = p2.move(c2)
                        continue
                    c2 = input("You have chosen the wrong card, please choose the right card, (1-10): ")
                
                print(clearBoard + "Player2 has successfully chosen the card")
            
                # @@@@@@@@@ Betting phase @@@@@@@@@
                print("It is now time to bet. Please bet accordingly with strategies.\nOnce the amounts of the bets are equivalent, final judgement will be beginning.")
                b1 = int(input("Player1's turn to bet: "))
                while b1 > p1.point:
                    b1 = int(input("You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(p1.point)))
                p1.point -= b1
                
                b2 = int(input("Player2's turn to bet: "))
                while b2 > p2.point:
                    b2 = int(input("You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(p2.point)))
                p2.point -= b2
                    
                while b1 != b2:
                    print("\n\nAmounts of the betting are different, starting raise and call session.\nHighest Bet: {}".format(b1 if b1 > b2 else b2))
                    if b1 < b2:
                        print("\nPlayer1's bet is lower than that of Player2. Player1, would you like to bet more?")
                        d1 = input("No means that you are giving up. You will automatically lose. (Y / N): ").upper()
                        while d1 != "Y" and d1 != "N":
                            d1 = input("Wrong choice, Please try again: ").upper()
                        if d1 == "Y":
                            cob1 = input("Call or Bet? (c / b): ").lower()
                            if cob1 == 'c':
                                # p1.point += b1
                                b1 = p1.call(b2, b1)
                            else:
                                p1.point += b1
                                b1 = int(input("Player1's turn to bet: "))
                                while b1 > p1.point:
                                    b1 = int(input("You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(p1.point)))
                                p1.point -= b1
                        else:
                            print("Player1 gave up.")
                            f1 = -1
                            break
                    else:
                        print("\nPlayer2's bet is lower than that of Player1. Player2, would you like to bet more?")
                        d2 = input("No means that you are giving up. You will automatically lose. (Y / N): ").upper()
                        while d2 != "Y" and d2 != "N":
                            d2 = input("Wrong choice, Please try again: ").upper()
                        if d2 == "Y":
                            cob2 = input("Call or Bet? (c / b): ").lower()
                            if cob2 == 'c':
                                # p2.point += b2
                                b2 = p2.call(b1, b2)
                            else:
                                p2.point += b2
                                b2 = int(input("Player2's turn to bet: "))
                                while b2 > p2.point:
                                    b2 = int(input("You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(p2.point)))
                                p2.point -= b2
                        else:
                            print("Player2 gave up.")
                            f2 = -1
                            break
                
                # @@@@@@@@@@@ Judgement phase @@@@@@@@@@@
                print('\n\n')
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
                    print("Player1 has lost all his / her points!\nPlayer2 has won the game!!!\n\n")
                    break
                elif p2.point == 0:
                    print("Player2 has lost all his / her points!\nPlayer1 has won the game!!!\n\n")
                    break
                
                print("\nCurrent Point: Player1: {}, Player2: {}".format(p1.point, p2.point))
                    
            if p1.point > p2.point:
                print("@@@@@@@ Player1 won!! @@@@@@@")
            elif p1.point < p2.point:
                print("@@@@@@@ Player2 won!! @@@@@@@")
            else:
                print("@@@@@@@ Draw!! @@@@@@@")
                
        elif mode == 'pvai':
            p1 = Player()
            p2 = AI()
            print("Starting PvAI mode...")
            for i in range(20):
                # @@@@@@@@ Card choosing phase @@@@@@@@@@
                c1 = input("Player1's turn to choose card, which card do you wish to pick? (1-10): ")
                f1 = p1.move(c1)
                while c1 not in [str(i) for i in range(1, 11)] or f1 == None:
                    if f1 == None:
                        c1 = input("The Card you are trying to pull does not exist, please choose again, (1-10): ")
                        f1 = p1.move(c1)
                        continue
                    c1 = input("You have chosen the wrong card, please choose the right card, (1-10): ")
                
                print(clearBoard + "Player1 has successfully chosen the card")
                
                c2 = p2.pick()
                f2 = int(c2)
                
                # @@@@@@@@@ Betting phase @@@@@@@@@
                print("It is now time to bet. Please bet accordingly with strategies.\nOnce the amounts of the bets are equivalent, final judgement will be beginning.")
                b1 = int(input("Player1's turn to bet: "))
                while b1 > p1.point:
                    b1 = int(input("You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(p1.point)))
                p1.point -= b1
                
                print("AI will choose its betting...")
                b2 = p2.bet()
                
                while b1 != b2:
                    print("\n\nAmounts of the betting are different, starting raise and call session.\nHighest Bet: {}".format(b1 if b1 > b2 else b2))
                    if b1 < b2:
                        print("\nPlayer1's bet is lower than that of Player2. Player1, would you like to bet more?")
                        d1 = input("No means that you are giving up. You will automatically lose. (Y / N): ").upper()
                        while d1 != "Y" and d1 != "N":
                            d1 = input("Wrong choice, Please try again: ").upper()
                        if d1 == "Y":
                            cob1 = input("Call or Bet? (c / b): ").lower()
                            if cob1 == 'c':
                                b1 = p1.call(b2, b1)
                            else:
                                p1.point += b1
                                b1 = int(input("Player1's turn to bet: "))
                                while b1 > p1.point:
                                    b1 = int(input("You cannot bet more than what you have. Please bet again, (Your current point: {}): ".format(p1.point)))
                                p1.point -= b1
                        else:
                            print("Player1 gave up.")
                            f1 = -1
                            break
                    else: # ai has bet lower.
                        if not p2.giveUp(b1):
                            p2.point += b2
                            b2 = p2.raiseBet(b1)
                        else:
                            print("AI has given up.")
                            f2 = -1
                            break
                
                # @@@@@@@@@@@ Judgement phase @@@@@@@@@@@
                print('\n\n')
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
                    print("Player1 has lost all his / her points!\nAI has won the game!!!\n\n")
                    break
                elif p2.point <= 0:
                    print("AI has lost all his / her points!\nPlayer has won the game!!!\n\n")
                    break
                
                print("\nCurrent Point: Player1: {}, AI: {}".format(p1.point, p2.point))

        elif mode == 'aivai':
            # Define Players
            p1 = AI()
            p2 = AI()
            print("Starting AIvAI mode...")
            for i in range(20):
                # Pick cards from the deck
                f1 = int(p1.pick())
                f2 = int(p2.pick())

                # Initialize bet amount
                b1 = int(p1.bet())
                b2 = int(p2.bet())
                while b1 != b2:
                    if b1 < b2:
                        # Will Player1 give up according to bet given by Player2?
                        if not p1.giveUp(b2):
                            p1.point += b1
                            # Reset the bet.
                            b1 = p1.raiseBet(b2)
                        else:
                            print("AI1 has given up.")
                            f1 = -1
                            break
                    else:
                        # Will Player2 give up according to bet given by Player1?
                        if not p2.giveUp(b1):
                            p2.point += b2
                            # Reset the bet.
                            b2 = p2.raiseBet(b1)
                        else:
                            print("AI2 has given up.")
                            f2 = -1
                            break

                # @@@@@@@@@@@ Judgement phase @@@@@@@@@@@
                print('\n\n')
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
                    print("AI1 has lost all his / her points!\nAI2 has won the game!!!\n\n")
                    break
                elif p2.point <= 0:
                    print("AI2 has lost all his / her points!\nAI1 has won the game!!!\n\n")
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