import cartes
# revoir la gestion des mises 
class joueur:
    # en argument le nom du joueur, son porte feuille 
    def __init__(self,nom,BankRoll):
        self.nom=nom
        self.deck:list[cartes.carte]=[]
        self.poche:list[list[cartes.carte]]=[]
        self.bankroll=BankRoll
        self.mise=0
        self.liste_mises:list[int]=[]
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

            # initialisation des listes
            self.poche = [self.deck]
            self.liste_mises= [self.mise]
            return self.mise 

    # definir le gain d'une main
    # donner en argument le numero de la main
    def gain(self,p,multiplicateur=2):
        self.bankroll += self.liste_mises[p] * multiplicateur
        self.mise=0
        self.liste_mises[p]=0

        if multiplicateur == 1:
            print(f"\négalité pour {self.nom}")
        else:
            print(f"\ngain de {self.nom}")

    # définie une perte d'une main 
    # donenr en argument la main
    def perte(self,p):
        self.mise=0
        self.liste_mises[p]=0

        if len(self.poche)>1:
            print(f"\nperte de la main n° {p+1} de {self.nom}")
        else:
            print(f"\nperte de {self.nom}")

    # permet de donner ou poser une carte sur un deck vide ou deja remplie 
    def donner(self,carte:cartes.carte,other:"cartes.deck"):
        if carte in self.deck:
            other.deck.append(carte)
            self.deck.remove(carte)
        else:
            raise ValueError(f"carte abscente du deck {self}") 
        
    # faire en sorte que self.deck garde toujours un deck et garder la liste de deck tout les decks dans sa poche 
    # fonction qui divise la main actuelle en 2 mains conservées dans poche
    # ajouter la mise a chaque deck
    # self.deck est ensuite remplacé par la premiere main 
    def split(self):
        liste1=[]
        liste2=[]

        if len(self.deck)!=2:
            print("split non possible")
            return 

        liste1.append(self.deck[0])
        liste2.append(self.deck[1])

        self.liste_mises.insert(self.poche.index(self.deck)+1,self.mise) # ajouter la meme mise sur chaque deck  
        self.bankroll-=self.mise
        


        self.poche[self.poche.index(self.deck)] = liste1
        self.poche.insert(self.poche.index(liste1)+1, liste2)

        self.changer_deck(self.poche.index(liste1))

    # changer le deck en main par celui dans la poche 
    # donner en argument le numéro de la main a switch 
    def changer_deck(self,deck):
        self.deck=self.poche[deck]
        self.changer_mise(deck)

    # meme fonctionnement que changer deck
    def changer_mise(self,mise):
        self.mise=self.liste_mises[mise]
