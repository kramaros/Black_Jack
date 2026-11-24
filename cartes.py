import random
import sys

#sys.tracebacklimit = 0

class carte:
    # valeur prend la valeur de la carte (as à Roi)
    # figure prend le nom de la figure en str
    # symbole prend le symbole de la carte (♠, ♥, ♦, ♣)
    def __init__(self,valeur:str, figure:str, symbole:str):
        self.valeur=valeur
        self.figure=figure
        self.symbole=symbole
        self.ID=f"{self.valeur}{self.symbole}"
        self.etat="affiché"
        self.affichage=f"""
  ____      
 |{self.valeur}   |
 | {self.symbole}  |
 |   {self.valeur}|
  ‾‾‾‾ """ if self.valeur!="10" else f"""
  ____      
 |10  |
 | {self.symbole}  |
 |  10|
  ‾‾‾‾
""" 

        
        self.cachée=f"""
  ____      
 |####|
 |####|
 |####|
  ‾‾‾‾
"""
    def __str__(self):
        if self.etat=="affiché":
            return self.affichage
        else:
            return self.cachée

    def __repr__(self):
        return f"{self.valeur} de {self.figure}"

    def retourner(self):
        if self.etat=="affiché":
            self.etat="caché"
        else:
            self.etat="affiché"

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
            raise ValueError("Nombre de carte par jeux inexacte")
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

    # permet de donner ou poser une carte sur un deck vide ou deja remplie 
    def donner(self,carte:carte,other:deck):
        if carte in self.deck:
            other.deck.append(carte)
            self.deck.remove(carte)
        else:
            raise ValueError(f"carte abscente du deck {self}") 

