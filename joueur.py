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
        while True:
            print(f"Quelle est votre mise pour ce tour {self.nom} ?")
            reponse=input("\n[1]5$ [2]10$ [3]20$ [4]50$ [5]100 [6]200")
            choix = {"1": 5, "2": 10, "3": 20, "4": 50, "5": 100,"6": 200}
            mise=choix[reponse]
            if self.bankrool<mise:
                print("mise au dessus des moyens")
            else:
                return self.mise 
