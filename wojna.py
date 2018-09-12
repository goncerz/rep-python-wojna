# Game w wojne

class Card(object) :
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["c", "d", "h", "s"]

    def __init__(self, rank, suit) :
        self.rank = rank 
        self.suit = suit

    def __str__(self) :
        rep = self.rank + self.suit
        return rep

    @property
    def value(self) :
        v = Card.RANKS.index(self.rank) + 2
        return v

class Hand(object) :
    def __init__(self) :
        self.cards = []

    def __str__(self) :
        if self.cards :
           rep = ""
           for card in self.cards :
               rep += str(card) + "\t"
        else:
            rep = "<pusta>"
        return rep

    def clear(self) :
        self.cards = []

    def add(self, card) :
        self.cards.append(card)

    def give(self, card, other_hand) :
        self.cards.remove(card)
        other_hand.add(card)

class Deck(Hand) :
    def populate(self) :
        for suit in Card.SUITS :
            for rank in Card.RANKS : 
                self.add(Card(rank, suit))
        #for rank in Card.RANKS :
        #    for suit in Card.SUITS : 
        #        self.add(Card(rank, suit))

    def shuffle(self) :
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand = 26) :
        for rounds in range(per_hand) :
            for hand in hands :
                if self.cards :
                    self.give(self.cards[0], hand)
                else :
                    print("\nBrak kart do rozdania.")

class Player(Hand) :
    def __init__(self,name) :
        super(Player, self).__init__()
        self.name = name

    def __str__(self) :
        rep = self.name + ":\n" + super(Player, self).__str__()
        return rep

    # Player przegrywa - nie ma kart
    def is_busted(self) :
        return self.cards == []

    def lose(self) :
        print(self.name, "przegrywa.")

    def win(self) :
        print(self.name, "wygrywa.")

    def bust(self) :
        print(self.name, "nie ma kart.")

class Game(object) :
    def __init__(self, names) :
        self.players = []
        for name in names :
            player = Player(name)
            self.players.append(player)

        self.heap = Hand()
        self.deck = Deck()

    def play(self) :
        n = 0
        n_chk = 100
        self.deck.populate()
        print("Talia:")
        print(self.deck)
        input("\nNacisnij dowolny klawisz.\n")
        
        self.deck.shuffle()
        print("Talia po potasowaniu:")
        print(self.deck)
        input("\nNacisnij dowolny klawisz.\n")

        self.deck.deal(self.players, per_hand = 26)

        while (not self.players[0].is_busted() ) and (not self.players[1].is_busted() ) :
            n += 1
            for player in self.players :
                print(player)
                print()

            #input("Nacisnij dowolny klawisz.\n") ###

            if self.heap.cards :
                for player in self.players :
                    player.give(player.cards[0], self.heap)

            if (not self.players[0].is_busted() ) and (not self.players[1].is_busted() ) :
                for player in self.players :
                    player.give(player.cards[0], self.heap)

            heap_size = len(self.heap.cards)

            if heap_size > 2 and self.heap.cards[heap_size-2].value == self.heap.cards[heap_size-1].value :
                print("Stos:")
                print(self.heap)
                print()
            
            if self.heap.cards[heap_size-2].value > self.heap.cards[heap_size-1].value :
                while self.heap.cards :
                    self.heap.give(self.heap.cards[0], self.players[0])
            elif self.heap.cards[heap_size-2].value < self.heap.cards[heap_size-1].value :
                while self.heap.cards :
                    self.heap.give(self.heap.cards[0], self.players[1])
            else :
                if heap_size == 2 :
                    print("Stos:")
                    print(self.heap)
                    print()

            if ( n % n_chk == 0 and n >= n_chk ) :
                print("Liczba rozdan:", n)
                choice = ""
                while choice == "" :
                    choice = input("Gramy dalej? (N-nie) ")
                if choice.lower() == "n" :
                    break

        for player in self.players :
            print()
            print(player)
        #input("\nNacisnij dowolny klawisz.\n") ###

        if (not self.players[0].is_busted() ) and self.players[1].is_busted() :
            self.players[1].bust()
            self.players[0].win()
            self.players[1].lose()
        elif self.players[0].is_busted() and (not self.players[1].is_busted() ) :
            self.players[0].bust()
            self.players[0].lose()
            self.players[1].win()
        elif (not self.players[0].is_busted() ) and (not self.players[1].is_busted() ) :
            print("\nGra przerwana. Remis.")
        else : # Playere nie maja kart
            self.players[0].bust()
            self.players[1].bust()
            print("\nRemis.")

        print("Liczba rozdan:", n)

        for player in self.players :
            player.clear()

        self.heap.clear()
        self.deck.clear()

def main() :
    print("Game W WOJNE\n")

    name1 = input("Gracz 1: ")
    while name1 == "" :
        print("Wpisz nazwe.")
        name1 = input("Player 1: ")
        
    name2 = input("Gracz 2: ")
    while name2 == "" :
        print("Wpisz nazwe.")
        name2 = input("Player 2: ")

    print()

    game = Game([name1,name2])
    choice = ""
    while choice.lower() != "n" :
        game.play()
        choice = input("\nJeszcze raz? (N-nie) ")

############################################################################################################
main()
