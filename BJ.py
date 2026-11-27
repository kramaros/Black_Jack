import cartes
from joueur import joueur

# dictionnaire ordonant la valeur des cartes
Valeur_cartes={
    "A":(1,11),
    "K":10,
    "Q":10,
    "J":10,
    "10":10,
    "9":9,
    "8":8,
    "7":7,
    "6":6,
    "5":5,
    "4":4,
    "3":3,
    "2":2

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
    reponse=input("""
                                88                          
                                ""                          
                                                            
 ,adPPYba, ,adPPYYba, ,adPPYba, 88 8b,dPPYba,   ,adPPYba,   
a8"     "" ""     `Y8 I8[    "" 88 88P'   `"8a a8"     "8a  
8b         ,adPPPPP88  `"Y8ba,  88 88       88 8b       d8  
"8a,   ,aa 88,    ,88 aa    ]8I 88 88       88 "8a,   ,a8"  
 `"Ybbd8"' `"8bbdP"Y8 `"YbbdP"' 88 88       88  `"YbbdP"'   
                                                            
 


    Bienvenue au Black Jack

    Combien de joueur ? """)

    while True:
        try:
            nb_joueur = int(reponse)

            if nb_joueur > 0:
                break

        except ValueError:
            pass
        reponse = input("Donnez un nombre valable : ")

    for i in range(nb_joueur):
        name:str=input(f"\nnom du joueur {i+1} ?")
        
        print(f"\nQuel montant pour votre Bankroll ?")
        reponse=input("\n[1]100$ [2]200$ [3]500$ [4]1000$ [5]5000$\n\n")
        choix = {"1": 100, "2": 200, "3": 500, "4": 1000, "5": 5000}

        while reponse not in choix:
            reponse=input("\nchoix invalide, recommencez\n\n")
        
        argent=choix[reponse]
        
        x=joueur(name,argent)
        ordre.insert(-1,x)



    return croupier, table, ordre


# fonction permettant d'obtenir la valeur d'un deck
# mettre le deck souhaité en entrée
# la valeur du deck est donné en sortie
def valeur_deck(deck:cartes.deck):
    ValeurDuDeck=0
    liste_As=deck.deck.copy()
    for i in deck.deck:
        if i.valeur != "A":
            ValeurDuDeck+= Valeur_cartes[i.valeur]
            liste_As.remove(i)
    # AS        
    for i in liste_As:
        ValeurDuDeck += Valeur_cartes[i.valeur][0]

    if liste_As and ValeurDuDeck + 10 <= 21:
        ValeurDuDeck += 10

    return ValeurDuDeck

# afficher le deck horizontalemlent avec comme argument le deck proposé
def afficher_deck(deck):
    if type(deck)==joueur:
        print(f"\n Deck de {deck.nom} :\n")
        if len(deck.poche)>1:
            print(f"\nDeck n° {deck.poche.index(deck.deck)+1}\n")
            print(f"\nMise du deck: {deck.mise}\n")
        print(f"\nBankroll: {deck.bankroll}")
        print(f"\nMise totale: {sum(deck.liste_mises)}")

    cartes_affichees = [
        str(carte).strip("\n").splitlines()
        for carte in deck.deck
    ]

    for ligne in zip(*cartes_affichees):
        print("   ".join(ligne))

# fonction permettant de distribuer les cartes au black jack
# donner en argument l'ordre du jeux, le deck du croupier, et le deck de la table
def distribution(ordre, croupier, table):
    for k in range(2):
        for i in ordre:
            if i=="table":
                print(f"cartes pausées sur la table")
                croupier.donner(croupier.deck[0],table)
                if k==1:
                    table.deck[1].retourner()  # retourner face caché la 2ème carte  
                afficher_deck(table)

            else:
                print(f"carte donnée à {i.nom}")
                croupier.donner(croupier.deck[0],i) # affichier de facon horizontale les cartes avec *
                afficher_deck(i)


# retourne true si les 2 premieres cartes font 21                
def Black_Jack(deck):
    return len(deck.deck)==2 and valeur_deck(deck)==21

#fonction de l'assurance si le croupier commence avec un As
# donner en argument le deck de la table et le tuple du joueur
# return True si Black Jack du croupier
def assurance(table,ordre):
    for i in ordre: 
        if i=="table":
            continue
        if table.deck[0].valeur=="A":
            print(f"""Voulez vous prendre une assurance {i.nom} ?""")
            
            reponse=input(" Oui(O)/Non(n)\n\n")
            while reponse not in ("O","n"):
                print("reponse incorrecte ")
                reponse=input(" Oui(O)/Non(n)\n\n")

            if reponse=="O":
                if i.bankroll<i.mise/2:
                    print("Bankroll non suffisante pour une assurance")
                    continue
                assurance=i.mise / 2
                i.assurance+=assurance
                i.bankroll-=assurance
                print(f"{i.nom} s'assure de {assurance} $")

            elif reponse=="n":
                print(f"{i.nom} ne s'assure pas")




    if Black_Jack(table):

        print("\nBLACK JACK DU CROUPIER !!!\n")

        table.deck[1].retourner()
        afficher_deck(table)

        for i in ordre:

            if type(i) == joueur:

                # Gestion de l'assurance
                if i.assurance > 0:
                    i.bankroll += i.assurance * 3
                    print(f"\nAssurance gagnée par {i.nom}")

                i.assurance = 0

                # Gestion de la mise principale
                if Black_Jack(i):
                    i.gain(0, 1)

                else:
                    i.perte(0)

        return True

    else:

        for i in ordre:

            if type(i) == joueur:

                if i.assurance > 0:
                    print(f"\nAssurance perdue par {i.nom}")

                i.assurance = 0

        return False

# possibiliter de doubler la mise et seulement tirer une carte    
# donner en argument le deck croupier et le joueur 
# en sortie False si double mise impossible
# True si elle est possible            
def double_mise(croupier:cartes.deck,joueur:joueur,p): # modifier pour doubler unquement la mise de la main 
    if joueur.bankroll<joueur.mise:
        print("bankroll insuffisant pour doubler")
        return False
    
    print(f"\n{joueur.nom} fait une double mise !")
    joueur.bankroll-=joueur.mise
    joueur.mise+=joueur.mise
    joueur.liste_mises[p]=joueur.mise

    croupier.donner(croupier.deck[0],joueur)
    afficher_deck(joueur)
    return True

# retourne True si possibilité de split sinon False
# fonction non implémenté dans la classe car valeurs des cartes défini dans dictionnaire externe 
def possibiliter_split(joueur:joueur):
    return (
    len(joueur.deck)==2 
    and 
    Valeur_cartes[joueur.deck[0].valeur]==Valeur_cartes[joueur.deck[1].valeur]
    )
            

# action du joueur: tirer rester doubler split
# attention !! double apres split possible 
# split un as permet uniquement de prendre une carte par as
# pas de black jack apres un split
# apres un split d'as impossible de doubler la mise
def action(croupier:cartes.deck,joueur:joueur):

    p=0
    while p < len(joueur.poche): # boucle pour chaque main d'un joueur
        
        joueur.changer_deck(p)

        while valeur_deck(joueur) < 21:


            if len(joueur.deck) == 1:

                as_split = joueur.deck[0].valeur == "A"

                croupier.donner(croupier.deck[0], joueur)
                afficher_deck(joueur)

                if as_split:
                    break

                if valeur_deck(joueur) >= 21:
                    break

            choix=["[1] Tirer","[2] Rester"]
            choix_valides=["1", "2"]

            if len(joueur.deck)==2:
                choix.append("[3] Doubler Mise")
                choix_valides.append("3")

                if possibiliter_split(joueur):
                    choix.append("[4] Split")
                    choix_valides.append("4")

            réponse=input("\n"+" ".join(choix)+"\n")
            while réponse not in (choix_valides):
                print("\nChoix invalide, recommencez\n")
                réponse=input("\n"+" ".join(choix)+"\n")
            
            if réponse == "1":
                croupier.donner(croupier.deck[0], joueur)
                afficher_deck(joueur)

            if réponse=="2":
                print(f"\n {joueur.nom} reste")
                break

            if réponse=="3":
                if not double_mise(croupier,joueur,p):
                    continue
                break
            
            if réponse=="4": # faire en sorte de pouvoir tourner de main sr un tour / limiter a 4 mains X / rajouter une mise similaire sur mise total et a chaque élimination de main supprimer la partie de la mise


                if len(joueur.poche)>=4:
                    print("nombre de jeux maximal à 4 déja atteint")
                    continue
                
                if joueur.bankroll<joueur.mise: # bloquer si pas assez d'argent pour split
                    print("pas assez d'argent dans la Bankroll pour split")
                    continue

                joueur.split()

                for i in range(len(joueur.poche)):
                    joueur.changer_deck(i)
                    print(f"{joueur.nom} : deck n° {i+1}")
                    afficher_deck(joueur)

                joueur.changer_deck(p)
    

        if valeur_deck(joueur)>21:
            print(f"dépassement de 21 pour cette main")
            joueur.perte(p)
        p+=1
        

    return
    
# tours des joueurs avant le croupier 
# mettre en argument le deck de la banque et celui des joueurs
def tour_joueur(croupier,joueur:joueur):
    print(f"\ntour de {joueur.nom}")
    # vérifier black jack
    if Black_Jack(joueur):
        print("\nBLACK JACK !!!\n\n")
        joueur.gain(0,2.5)
        
        return

    afficher_deck(joueur)

    action(croupier,joueur)

# la banque tire à 16, reste à 17
# donner en argument le deck du crouîer ainsi que celui de la table
# en sortie, True si 
def tour_croupier(croupier,table):
    print(f"\ntour de la banque")

    while valeur_deck(table)<=16:
        croupier.donner(croupier.deck[0],table)
        print("\nTable\n")
        afficher_deck(table)
    # true si croupier encore en jeux 
    if (17<=valeur_deck(table)<=21):
        return True
    # False si crouier perd
    if valeur_deck(table)>21:
        print("\n le croupier a un total supérieur à 21")
        return False

# fonction permettant de donner les gains ou les pertes
# donner en entré le deck des joueurs et de la table
def vérification(joueur:joueur,table):
    # selection de joueur encore en jeux !!! ainsi que de leurs différentes mains 


    for p in range(len(joueur.poche)):
        if joueur.liste_mises[p]==0:
            continue

        joueur.changer_deck(p)


        if valeur_deck(joueur) > 21:
            joueur.perte(p)

        elif valeur_deck(table) > 21:
            joueur.gain(p)

        elif valeur_deck(joueur) < valeur_deck(table):
            joueur.perte(p)

        elif valeur_deck(joueur) > valeur_deck(table):
            joueur.gain(p)

        else:
            joueur.gain(p, 1)

        

# fonction qui supprime les joueurs avec un solde nul
# rend le joueur pour le mettre dans une liste poubelle
def éliminations(joueur:joueur,ordre):
    if joueur.bankroll<5: # mise minimale de 5
        print(f"\n {joueur.nom} est éliminé(e)")
        ordre.remove(joueur)
        return joueur

# un tour de table jusqu'a la perte ou la victoire du croupier
# on prend en argument les sorties de initialisation 
# ajouter un système de timer pour laisser le temps a chaque echange de carte d'etre visualisé
def tour(croupier, table, ordre):
    print("\n\ndébut du tour\n\n")
    # mise des joueurs pour le tour
    for i in ordre:
        if i !="table":
            mise=i.miser()
            print(f"\n {i.nom} mise {mise}$")

    # premiers tour de distributions
    distribution(ordre,croupier,table)

    # demande des assurances si premiere carte est un As
    if assurance(table,ordre):
        return 

    # tour des joueurs
    for i in ordre:
        if type(i)==joueur:
            tour_joueur(croupier,i)

    # retournement final du croupier
    print("\n\ncartes pausées sur la table : ") 
    afficher_deck(table)   
    print("\n* retournement de la carte face visible\n")
    table.deck[1].retourner()
    afficher_deck(table)


    tour_croupier(croupier, table)

    for i in ordre:
        if type(i) == joueur:
            vérification(i, table)


# choix de continuer de jouer ou non
# donner en argument la liste des joueurs ayant perdu pour un future tableau des scores
# donner en argument la liste ordre
# rend en argument la liste poubelle
def choix(poubelle, ordre):
    réponse = input("\n\n[1]continuer [2]quitter\n\n")

    while réponse not in ("1", "2"):
        réponse = input("\nChoix invalide, recommencez\n")

    if réponse == "2":
        for i in ordre.copy():
            if type(i) == joueur:
                poubelle.append(i)
                ordre.remove(i)

    return poubelle

def affichage_score(score:list[joueur]):
    score.sort(key=lambda s: s.bankroll, reverse=True ) # ordonner par la bankroll des joueurs
    k=1
    for i in score:
        print(f"{k}. {i.nom} : {i.bankroll} $\n")
        k+=1

# fonction pour vider les decks a la fin d'un tour     
# probleme pouvant être rencontré : si jamais le croupier n'a plus de carte ?
# si deck vide du croupier, rajouter la defausse mélangé dans son deck a nouveau
def vider_deck(ordre,défausse,table): # rajouter aussi les autres mains !!
    for i in ordre:
        if type(i) == joueur:
            for p in i.poche:
                défausse.deck.extend(p)
            i.poche.clear()
            i.deck.clear()
            i.liste_mises.clear()
            i.mise=0
            i.assurance=0

    défausse.deck.extend(table.deck)
    table.deck.clear()

# s'il reste moins de 52 cartes, shuffle la défausse et la rajouter au croupier
def vider_défausse(défausse, croupier):
    défausse.shuffle()
    croupier.deck.extend(défausse.deck)
    défausse.deck=[]

def main():
    score = []
    défausse = cartes.deck(0, 0)

    croupier, table, ordre = initialisation()

    while len(ordre) > 1:

        # Renouvellement du sabot
        if len(croupier.deck) <= 52:
            vider_défausse(défausse, croupier)

        # Déroulement du tour
        tour(croupier, table, ordre)

        # Récupération des cartes
        vider_deck(ordre, défausse, table)

        # Vérification du nombre de cartes
        assert len(croupier.deck) + len(défausse.deck) == 312

        # Élimination des joueurs
        for i in ordre.copy():
            if type(i) == joueur:
                déchet = éliminations(i, ordre)

                if déchet is not None:
                    score.append(déchet)

        # Choix de continuer
        if len(ordre) > 1:
            score = choix(score, ordre)

    print("\n\nfin de partie\n\n")
    print("SCORES:\n\n")
    affichage_score(score)
    
if __name__=="__main__":
    main() 