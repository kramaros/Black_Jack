import cartes

class joueur:
    # en argument le nom du joueur, son porte feuille 
    def __init__(self,nom,BankRoll):
        self.nom=nom
        self.deck:list[cartes.carte]=[]
        self.bankroll=BankRoll
        self.mise=0
        self.assurance=0

    # choisir la mise a chaque tour 
# en entré donner le porte feuille du joueur 
# en sortie, donné la mise
    def miser(self):
            print(f"Quelle est votre mise pour ce tour {self.nom} ?")
            reponse=input("\n[1]5$ [2]10$ [3]20$ [4]50$ [5]100 [6]200\n\n")
            choix = {"1": 5, "2": 10, "3": 20, "4": 50, "5": 100,"6": 200}
            while reponse not in choix or self.bankroll<choix[reponse]:
                if reponse not in choix:
                    reponse=input("\nreponse invalide, recommencez\n\n")
                else: 
                    reponse=input("\nmise au dessus des moyens, recommencez\n\n")

            self.mise=choix[reponse]
            self.bankroll-=self.mise
            return self.mise 

    def gain(self):
        self.bankroll+=self.mise*2
        self.bankroll+=self.assurance
        self.mise=0
        self.assurance=0
        print(f"\ngain de {self.nom}")

    def perte(self):
        self.mise=0
        print(f"\nperte de {self.nom}")

    # permet de donner ou poser une carte sur un deck vide ou deja remplie 
    def donner(self,carte:cartes.carte,other:"cartes.deck"):
        if carte in self.deck:
            other.deck.append(carte)
            self.deck.remove(carte)
        else:
            raise ValueError(f"carte abscente du deck {self}") 