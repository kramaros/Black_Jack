import cartes

# création des joueurs et du croupier
# en sortie on donne le croupier et une liste de tuple des joueurs et de leur deck ainsi que de la table 
def initialisation():
    # ordree du jeux
    ordre=["table"]
    ordre_deck=[]

    # création du deck de la banque
    croupier=cartes.deck(6,52)
    croupier.create() # création du croupier
    croupier.shuffle()

    #création du deck de la table
    table=cartes.deck(0,0)
    ordre_deck.append(table)

    nb_joueur=int(input("""
    Bienvenue au Black Jack

    Combien de joueur ? """))

    for i in range(nb_joueur):
        name:str=input(f"\nnom du joueur {i+1} ?")
        x=cartes.deck(0,0)
        ordre.insert(-1,name)
        ordre_deck.insert(-1,x)

    ordre_final=list(zip(ordre,ordre_deck))

    return croupier, ordre_final

# un tour de table jusqu'a la perte ou la victoire du croupier
# on prend en argument les sorties de initialisation 
def tour(croupier, ordre):

    distribution=1  # rajouter +=1 a la fin du pemier tour de distribution 
    for k in range(2):
        for i in ordre:
            if i[0]=="table":
                print(f"cartes pausées sur la table")
                croupier.donner(croupier.deck[0],i[1])
                liste_carte=[]
                if distribution==2:
                    i[1].deck[1].retourner()  # retourner face caché la 2ème carte
                for k in i[1].deck:
                    liste_carte.append(k)    
                print(*liste_carte)

            else:
                print(f"carte donnée à {i[0]}")
                croupier.donner(croupier.deck[0],i[1])
                liste_carte=[]
                for k in i[1].deck:
                    liste_carte.append(k)
                print(*liste_carte) # affichier de facon horizontale les cartes avec *
        distribution+=1

def main():
    croupier, ordre=initialisation()
    tour(croupier,ordre)
    
if __name__=="__main__":
    main()