import random
import math

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']

ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

# CLASSES

class Card:  # Creates all the cards

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " +self.suit

class Deck:  # creates a deck of cards

    def __init__(self):
        self.deck = []  # haven't created a deck yet
        for suit in suits:
            for rank in ranks:
              # adding card to deck
                self.deck.append(Card(suit, rank))

    def shuffle(self):  # shuffle all the cards in the deck
        random.shuffle(self.deck)

    def deal(self):  # pick out a card from the deck
        single_card = self.deck.pop()
        return single_card

class Hand:   # show all the cards that the dealer and player have

    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card):  # add a card to the player's or dealer's hand
        self.cards.append(card)
      
class Poker(object):

  def __init__(self):
    # create all the objects we'll need
    # make the decks
    self.deck = Deck()
    self.playerHand = Hand()
    self.compHand = Hand()
    self.table = Hand()
    # set the amount of chips
    self.playerChips = 10000
    self.compChips = 10000
    self.tableChips = 0
    # use later to determine who the winner of each round is by seeing who has the best hand
    self.playerScore = 0
    self.compScore = 0
    # turn will alternate between 0-1 for big/ little blind
    self.turn = 0
    # self.checkTie1 = False

    # checking the betting with the bot
    self.BETVAR = False
    self.BETAMOUNT = 0

  # the main playing loop
  def play(self):
      self.deck.shuffle()
      self.cardRanks = []
      self.cardSuits = []
      self.count = 0
      playing = True
      # adding cards to player and comp hands
      self.playerHand.add_card(self.deck.deal())
      self.playerHand.add_card(self.deck.deal())
    
      self.compHand.add_card(self.deck.deal())
      self.compHand.add_card(self.deck.deal())

      # make the big/little blind
      if self.turn == 0:
        self.playerChips -= 200
        self.compChips -=100
        self.tableChips += 300
        print("\nThe player is the big blinds and bets 200 chips, and the computer as little blind bets 100 chips")
        self.turn = 1
      elif self.turn == 1:
        self.playerChips -= 100
        self.compChips -=200
        self.tableChips += 300
        print("\nThe player is the little blind and bets 100 chips, and the computer is the big blind and bets 200 chips")
        self.turn = 0
      
      # after created hands we need to make the table
    
      self.table.add_card(self.deck.deal())
      self.table.add_card(self.deck.deal())
      self.table.add_card(self.deck.deal())
      self.showCards()

      # self.pokerbot()
      while playing:
        
        print()
        # main loop for the betting part of the table
        try:
          chipBet =  int(input("What would you like to do? \n1.Fold \n2.Check \n3.Raise \n4.See the amount of chips on the table "))
        except:
          print("not an option")
          continue
    
        if chipBet <1 or chipBet > 5:
          print("error not an option")
          
        else:
          # needs to be reset
          self.BETVAR = False
          self.BETAMOUNT = 0

          if chipBet == 1:
            self.folded(self.playerHand)
          elif chipBet == 2:
            # print("you check, and so does the comp")
            print("you check")
          elif chipBet == 3:
            try:
              self.raiseAmount = int(input("how much would u like to bet"))
            except:
              print("not an option")
              continue
            
            
            if self.raiseAmount >self.playerChips:
              print("you do not have that many chips")
              continue
            else:
              print("you bet", self.raiseAmount, "amount of chips")
              self.tableChips += self.raiseAmount
              self.playerChips -= self.raiseAmount
              self.BETVAR = True
              self.BETAMOUNT += self.raiseAmount


               # #####
              # print("comp also bets same amount")
              self.tableChips +=self.raiseAmount
              self.compChips -=self.raiseAmount
              ######
              
          elif chipBet == 4:
            print("the amount of chips currently on the tabe is", self.tableChips)
            # we need continue to block the self.count +=1, and by blocking that the game doesn't continue
            continue    
          self.pokerbot()
          self.count +=1
          if self.count == 3:
            print("\nYour hand is", *self.playerHand.cards, sep = "\n")
            print("\nThe computer hand is", *self.compHand.cards, sep = "\n")
            print("\nThe winner is")   
          self.showCards()

  def convert(self):
    # convert to numbers from letters
    self.newList = []
    for i in self.cardRanks:
      if i == "Two":
        self.newList.append(2)
      if i == "Three":
        self.newList.append(3)
      if i == "Four":
        self.newList.append(4)
      if i == "Five":
        self.newList.append(5)
      if i == "Six":
        self.newList.append(6)
      if i == "Seven":
        self.newList.append(7)
      if i == "Eight":
        self.newList.append(8)
      if i == "Nine":
        self.newList.append(9)
      if i == "Ten":
        self.newList.append(10)
      if i == "Jack":
        self.newList.append(11)
      if i == "Queen":
        self.newList.append(12)
      if i == "King":
        self.newList.append(13)
      if i == "Ace":
        self.newList.append(14)
      # if self.checkTie1 == True:
        
      #   return self.newList

  def royalFlush(self,person):
    self.RFdict = []
    self.suits = []
    for i in person.cards:
      if i == "Ace":
        self.RFdict.append(i.rank)
        self.suits.append(i.suit)
      elif i == "Ten":
        self.RFdict.append(i.rank)
        self.suits.append(i.suit)
      elif i == "Jack":
        self.RFdict.append(i.rank)
        self.suits.append(i.suit)
      elif i == "Queen":
        self.RFdict.append(i.rank)
        self.suits.append(i.suit)
      elif i == "King":
        self.RFdict.append(i.rank)
        self.suits.append(i.suit)
        # by sorting the array we assure that if the player does have a royal flush we can determine the exact order of the cards
    self.RFdict.sort()
    try:
      if self.RFdict[0] == "Ace" and self.RFdict[1] == "Jack" and self.RFdict[2] == "King" and self.RFdict[3] == "Queen" and self.RFdict[4] == "Ten":
        if len(set(self.suits)) == 1:
          return False
        else:
          return True
    except:
      return True
    
  def straightFlush(self):
    if self.straight() == False and self.flush() == False:
      return False
    else:
      return True
    
  def fourKind(self):
    self.dic = {}
    
    for i in self.cardRanks:
      if i not in self.dic:
        self.dic[i] = 1
      else:
        self.dic[i] +=1
    for i in self.dic:
      if self.dic[i] == 4:
        return False
    return True
    
  def fullHouse(self):
    self.three = False
    self.two = False
    self.dic = {}

    for i in self.cardRanks:
      if i not in self.dic:
        self.dic[i] = 1
      else:
        self.dic[i] +=1

    for i in self.dic:
      if self.dic[i] == 3:
        self.three = True
      elif self.dic[i] == 2:
        self.two = True

    if self.three and self.two:
      return False
    return True

  def flush(self):
    self.dic = {}

    for i in self.cardSuits:
      if i not in self.dic:
        self.dic[i] = 1
      else:
        self.dic[i] +=1

    for i in self.dic:
      if self.dic[i] >= 5:
        return False

    return True

  def straight(self):
    self.convert()
    self.newList1 = []
    self.diff = 1
    # remove dups
    for i in self.newList:
      if i not in self.newList1:
        self.newList1.append(i)
    self.newList1.sort()

    if len(self.newList1) < 5:
      return True
    else:
      
      for i in range(len(self.newList1) - 4) :
        if self.newList1[i] + 1 == self.newList1[i + 1] :
          if self.newList1[i +1] + 1 == self.newList1[i + 2]:
            if self.newList1[i + 2] + 1== self.newList1[i+3]:
              if self.newList1[i + 3] + 1 == self.newList1[i + 4]:
                return False
    return True

  def threeKind(self):
    self.dic = {}

    for i in self.cardRanks:
      if i not in self.dic:
        self.dic[i] = 1
      else:
        self.dic[i] +=1

    for i in self.dic:
      if self.dic[i] == 3:
        return False
    return True

  def twoPair(self):
    self.count1 = 0
    self.dic = {}

    for i in self.cardRanks:
      if i not in self.dic:
        self.dic[i] = 1
      else:
        self.dic[i] +=1
    for i in self.dic:
      if self.dic[i] >= 2:
        self.count1 +=1

    if self.count1 >= 2:
      return False
    return True

  def pair(self):
    self.dic = {}

    for i in self.cardRanks:
      if i not in self.dic:
        self.dic[i] = 1
      else:
        self.dic[i] +=1
    for i in self.dic:
      if self.dic[i] == 2:
        return False 
    return True

  def highCard(self):
    self.convert()
    self.newList.sort()
    if self.newList[-1] == 11:
      return "Jack"
    elif self.newList[-1] == 12:
      return "Queen"
    elif self.newList[-1] == 13:
      return "King"
    elif self.newList[-1] == 14:
      return "Ace"
    else:
      return self.newList[-1]

  def showCards(self):
    print("\n")
    if self.count == 0:
      print("YOUR HAND IS",*self.playerHand.cards,sep = "\n")
      print("\n")
      print("The Table is...",*self.table.cards, sep = '\n')
      print("\n")
    elif self.count == 1:
      
      self.table.add_card(self.deck.deal())
      print("YOUR HAND IS",*self.playerHand.cards,sep = "\n")

      print("\n")
      print("The Table is...",*self.table.cards, sep = '\n')
      print("\n")
    elif self.count == 2:
      
      self.table.add_card(self.deck.deal())
      print("YOUR HAND IS",*self.playerHand.cards,sep = "\n")

      print("\n")
      print("The Table is...",*self.table.cards, sep = '\n')
      print("\n")
      # game is over now time to see who wins
    else:
      self.half = 0
      self.showOnce = 0
      print(self.checkWinner(self.playerHand))
      print(self.checkWinner(self.compHand))
      if self.playerScore > self.compScore:
        print("player wins")
        self.playerChips += self.tableChips
      elif self.playerScore == self.compScore:
            print("tie")
            self.half = self.tableChips // 2
            self.playerChips += self.half
            self.compChips += self.half
          
      else:
        print("comp wins")
        self.compChips += self.tableChips
      if self.playerChips <= 0 :
        print("comp has won...")
        quit()
      elif self.compChips <= 0:
        print("YOU HAVE WON...")
        quit()
      self.restart()
      
  def checkWinner(self,person):
      self.cardRanks = []
      self.cardSuits = []
    
      for i in person.cards:
        self.cardRanks.append(i.rank)
        self.cardSuits.append(i.suit)
      for i in self.table.cards:
        self.cardRanks.append(i.rank)
        self.cardSuits.append(i.suit)
        # checking for tie will break out here after appending the cards
      # if self.checkTie1 == True:
      #   return
        
      
      # we will keep checking the hands from the best to the worst until one returns False, which will be there best Hand
      if self.royalFlush(person):
        if self.straightFlush():
          if self.fourKind():
            if self.fullHouse():
              if self.flush():
                if self.straight():
                  if self.threeKind():
                    if self.twoPair():
                      if self.pair():
                        
                        if person==self.playerHand:
                          self.playerScore = 1
                        else:
                          self.compScore = 1
                        return("high card of " , self.highCard())
                      else:
                        if person == self.playerHand:
                          self.playerScore = 2
                        else:
                          self.compScore = 2
                        return("pair")
                        
                    else:
                      
                      if person == self.playerHand:
                        self.playerScore = 3
                      else:
                        self.compScore = 3
                      return("2 pair")
                      
                  else:
                    
                    if person == self.playerHand:
                      self.playerScore = 4
                    else:
                      self.compScore = 4
                    return("3 of a kind")
                else:

                  if person == self.playerHand:
                    self.playerScore = 5
                  else:
                    self.compScore = 5
                  return("straight")
              else:
               
               if person == self.playerHand:
                  self.playerScore = 6
               else:
                  self.compScore = 6
               return("flush")
            else:
              
              if person == self.playerHand:
                self.playerScore = 7
              else:
                self.compScore = 7
              return("full house")
          else:
           
            if person == self.playerHand:
              self.playerScore = 8
            else:
              self.compScore = 8
            return("4 of a kind")
        else:
         
          if person == self.playerHand:
            self.playerScore = 9
          else:
            self.compScore = 9
          return("straight flush")
      else:
        if person == self.playerHand:
          self.playerScore = 10
        else:
          self.compScore = 10
        return("royal flush")
     
  def folded(self,player):
    if player == self.playerHand:
      self.compChips += self.tableChips
    else:
      self.playerChips +=self.tableChips
    self.restart()


  def restart(self):
    print("you have" , self.playerChips, " many chips and the computer has" , self.compChips, "chips remaining")
    self.deck = Deck()
    self.playerHand = Hand()
    self.compHand = Hand()
    self.table = Hand()
    self.tableChips = 0
    self.compScore = 0
    self.playerScore = 0
    # self.count = 0
    print("\n\n\n")
    self.play()
  def compAmazingHand(self):
    # if comp's hand is 4 of a kind or royale flush
    self.BETAMOUNT = self.compChips
    print("THE COMP GOES ALL IN")
    self.compBET = 0
    self.compChips -= self.compBET
    self.tableChips += self.compBET
    self.inputBEST = input("1.call \n.Fold")
    if self.inputBEST == "1":
      if self.playerChips < self.compBET:
        print("you don't have enough chips and i ran out of time making this so you lose... sorry")
        self.compChips += self.tableChips
        self.folded(self.playerHand)
      else:
        # the player can bet now time to check if he bet before
        if self.BETVAR == False:
          print("you bet", self.compBET, "amount")
          self.playerChips -= self.compBET
          self.tableChips +=self.compBET
        else:
          print("you bet", self.compBET - self.BETAMOUNT, "amount")
          self.playerChips -= (self.compBET - self.BETAMOUNT)
          self.tableChips +=(self.compBET - self.BETAMOUNT)
        if self.count == 1:
          self.table.add_card(self.deck.deal())
          self.table.add_card(self.deck.deal())
          self.showCards()
        elif self.count == 2:
          self.table.add_card(self.deck.deal())
          self.showCards()
        elif self.count == 3:
          self.showCards()

    if self.inputBEST == "2":
      self.compChips += self.tableChips
      
      self.folded(self.playerHand)
      

  def compSecondBestHand(self):
    # if comps score is 2 or better but worse than 9
       # using the floor operation to make sure we can't bet a decimal amount of chips
    self.lowerbound = math.floor(self.compChips * (1/4))
    self.upperbound = math.floor(self.compChips * (1/2))
    self.compBET = 0
    self.compBET = random.randint(self.lowerbound,self.upperbound)
    # if the rand value is less than what the comp picked, make it equal to that
    if self.compBET < self.BETAMOUNT:
        self.compBET = self.BETAMOUNT 
    if self.compChips < self.BETAMOUNT:
        # wanted to do something else but ran out of time
        print("the comp folds")
        self.playerChips += self.tableChips
        self.folded(self.compHand)
      
    self.tableChips += self.compBET
    self.compScore -= self.compBET
    if self.compBET == self.BETAMOUNT:
        print("comp bets the same amount as you")
        # self.tableChips += self.compBET
        # return to break out of function cause there's no use to go on after
        return
    # self.tableChips += self.compBET
    
    print("the comp bets", self.compBET, "amount")
    self.secondBest = input("1.call \n2.fold")
      
    if self.secondBest == "1":
        
          if self.playerChips < self.compBET:
            print("you don't have enough chips and i ran out of time making this so you lose... sorry ps side pots are way too hard anways...")
            self.compChips += self.tableChips
            self.folded(self.playerHand)
          else:
            if self.BETVAR == False:
              print("you bet", self.compBET, "amount")
              self.playerChips -= self.compBET
              self.tableChips +=self.compBET
            else:
              print("you bet", self.compBET - self.BETAMOUNT, "amount")
              self.playerChips -= self.compBET - self.BETAMOUNT
              self.tableChips +=self.compBET - self.BETAMOUNT
    elif self.secondBest == "2":
        self.compChips += self.tableChips
        self.folded(self.playerHand)
        
  def compWorstHand(self):
    # comp score < 3
    if self.BETVAR == False:
      # the player didnt bet, so we keep playing
      print("the bot also check")
      return
    else:
      if self.count == 1:
        self.amount =   1/5
      else:
        self.amount = 1/10

      if self.BETAMOUNT > math.floor(self.amount * self.compChips):
        # the comp folds
        print("the comp folds")
        self.folded(self.compHand)
      else:
        print("the comp bets", math.floor(self.amount * self.compChips), "amount of chips")
        self.compChips -= math.floor(self.amount * self.compChips)
        self.tableChips += math.floor(self.amount * self.compChips)
      
      
  def pokerbot(self):
    self.checkWinner(self.compHand)
    if self.count == 0:
      self.compSecondBestHand()
    else:
      if self.compScore >= 9:
        self.compAmazingHand()
      elif self.compScore >= 2:
        self.compSecondBestHand()
      else:
        self.compWorstHand()
    
def main():
  poker = Poker()
  poker.play()

main()
