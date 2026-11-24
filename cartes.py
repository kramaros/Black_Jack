import random

class carte:
    # valeur prend la valeur de la carte (as à Roi)
    # figure prend le nom de la figure en str
    # symbole prend le symbole de la carte (♠, ♥, ♦, ♣)
    def __init__(self,valeur:str, figure:str, symbole:str):
        self.valeur=valeur
        self.figure=figure
        self.symbole=symbole
        self.affichage=f"""
  ____      
 |{self.valeur}   |
 | {self.symbole}  |
 |___{self.valeur}|
"""
    def __str__(self):
        return self.affichage

    def __repr__(self):
        return f"{self.valeur} de {self.figure}"

class deck:
    
    # nb_jeux prends le nombre de jeux demandé pour le deck 
    # nb_de_carte_par_jeux prend le nombre de carte dans un deck
    # pour la création du deck d'un joueur, laisser les 2 valeurs vides
    def __init__(self,nb_jeux, nb_carte_par_jeux):
        self.nb_jeux:int=nb_jeux
        self.nb_cartejeux:int=nb_carte_par_jeux
        self.symboles:list[str]=["♠", "♥", "♦", "♣"]
        self.figures:list[str]=["pique","coeur","carreau","trèfle"]
        self.valeurs:list[str]=["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
        self.deck:list[carte]=[]
    
    # création du deck de base du jeux souhaité
    def create(self):
        # test de possibilité de création du jeux:
        if not self.nb_cartejeux%4==0:
            raise "Nombre de carte par jeux inexacte"
        else:
            for i in range(self.nb_jeux):
                for fig,symb in zip(self.figures,self.symboles): #zip rend un tuple des valeurs associé 
                    for j in range(int(self.nb_cartejeux/4)): # nb de carte par symboles
                        x=carte(self.valeurs[j],fig,symb)
                        self.deck.append(x)
        return self.deck

    # à redefinir en fonction du jeux souhaité dans l'héritage de la class
    def __str__(self): 
        return str(self.deck)

    # pour mélanger le deck 
    def shuffle(self):
        random.shuffle(self.deck)


