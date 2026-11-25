import cartes
from joueur import joueur

#fonction de l'assurance si le croupier commence avec un As
# donner en argument le deck de la table et le tuple duimport cartes

# dictionnaire ordonant la valeur des cartes
Valeur_cartes={
    "A":(1,11),
    "K":int(10),
    "Q":int(10),
    "J":int(10),
    "10":int(10),
    "9":int(9),
    "8":int(8),
    "7":int(7),
    "6":int(6),
    "5":int(5),
    "4":int(4),
    "3":int(3),
    "2":int(2)

}

# création des joueurs et du croupier
# en sortie on donne le croupier et une liste de tuple des joueurs et de leur deck ainsi que de la table 
def initialisation():
    # ordree du jeux
    ordre=["table"]

    # création du deck de la banque
    croupier=cartes.deck(6,52)
    croupier.create() # création du croupier
    croupier.shuffle()

    #création du deck de la table
    table=cartes.deck(0,0)

    nb_joueur=int(input("""
                                88                          
                                ""                          
                                                            
 ,adPPYba, ,adPPYYba, ,adPPYba, 88 8b,dPPYba,   ,adPPYba,   
a8"     "" ""     `Y8 I8[    "" 88 88P'   `"8a a8"     "8a  
8b         ,adPPPPP88  `"Y8ba,  88 88       88 8b       d8  
"8a,   ,aa 88,    ,88 aa    ]8I 88 88       88 "8a,   ,a8"  
 `"Ybbd8"' `"8bbdP"Y8 `"YbbdP"' 88 88       88  `"YbbdP"'   
                                                            
 


    Bienvenue au Black Jack

    Combien de joueur ? """))

    for i in range(nb_joueur):
        name:str=input(f"\nnom du joueur {i+1} ?")
        print(f"\nQuel montant pour votre Bankroll ?")
        reponse=input("\n[1]100$ [2]200$ [3]500$ [4]1000$ [5]5000$\n")
        choix = {"1": 100, "2": 200, "3": 500, "4": 1000, "5": 5000}
        argent=choix[reponse]
        x=joueur(name,argent)
        ordre.insert(-1,x)



    return croupier, table, ordre


# fonction permettant d'obtenir la valeur d'un deck
def valeur_deck(deck:cartes.deck):
    ValeurDuDeck=0
    for i in deck.deck:
        if i.valeur != "A":
            ValeurDuDeck+= Valeur_cartes[i.valeur]
        else:
            if ValeurDuDeck + Valeur_cartes[i.valeur][1] >21:
                ValeurDuDeck+=Valeur_cartes[i.valeur][0]
            else:
                ValeurDuDeck+=Valeur_cartes[i.valeur][1]
    return ValeurDuDeck


#fonction de l'assurance si le croupier commence avec un As
# donner en argument le deck de la table et le tuple du joueur
def assurance(table,ordre):
    for i in ordre: 
        if i=="table":
            continue
        if table.deck[0].valeur=="A":
            print(f"""Voulez vous prendre une assurance {i.name} ?""")

            reponse=input(" Oui(O)/Non(n)")
            if reponse=="O":
                assurance=int(i.mise / 2)
                i.assurance+=assurance
                i.BankRoll-=assurance
                print(f"{i.name} s'assure de {assurance} $")
    if Valeur_cartes[table.deck[1].valeur]==10:
        #rendre mise et assurance 
        pass


# un tour de table jusqu'a la perte ou la victoire du croupier
# on prend en argument les sorties de initialisation 
# ajouter un système de timer pour laisser le temps a chaque echange de carte d'etre visualisé
def tour(croupier, table, ordre):
    # mise pour le tour
    for i in ordre:
        if i !="table":
            mise=i.miser()
            print(f"\n {i.nom} mise {mise}$")

    # premiers tour de distributions
    distribution=1  # rajouter +=1 a la fin du pemier tour de distribution 
    for k in range(2):
        for i in ordre:
            if i=="table":
                print(f"cartes pausées sur la table")
                croupier.donner(croupier.deck[0],table)
                liste_carte=[]
                if distribution==2:
                    table.deck[1].retourner()  # retourner face caché la 2ème carte
                for k in table.deck:
                    liste_carte.append(k)    
                print(*liste_carte)

            else:
                print(f"carte donnée à {i.nom}")
                croupier.donner(croupier.deck[0],i)
                liste_carte=[]
                for k in i.deck:
                    liste_carte.append(k)
                print(*liste_carte) # affichier de facon horizontale les cartes avec *
        distribution+=1

    for i in ordre: 
        
        if i=="table":
            liste_carte=[]
            for k in table.deck:
                liste_carte.append(k)
            print(*liste_carte)
            print("* retournement de la carte face visible")
            table.deck[1].retourner()
            print(table.deck[1])





def main():
    croupier, table, ordre=initialisation()
    tour(croupier,table, ordre)

    
if __name__=="__main__":
    main() 