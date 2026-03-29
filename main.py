import fonction
from fonction import lire_automate, non_standard, standardisation, lire_lignes, lire_mot, reconnaitre_mot, \
    determinisation_completion_automate, minimiser_automate, obtenir_index_classe, afficher_transitions_classes, \
    sont_equivalents


def main():
    flag = 0
    print("\nBienvenue dans le programme d'automate !")
    while flag == 0:
        choix = input("Veuillez choisir un automate (entre 01 et 44): ")
        if choix in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                     '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                     '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                     '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                     '41', '42', '43', '44']:
            print(f"Vous avez choisi l'automate {choix}.")
            flag = 1
        else:

            print("\nChoix invalide. Veuillez choisir un nombre entre 01 et 44.")
    # dmd quelle automate at-elle choisie et faire les differentes fonctions
    af = lire_automate(choix)
    # si automate en erreur on sort du programme
    if (af == None):
        print("\nAutomate non lisible")
        return
    fonction.afficher_automate(af)
    flag = 0
    if fonction.est_asynchrone(af):
        while flag == 0:
            synchroniser = input("Voulez-vous synchroniser l'automate ? (oui/non) ")
            if synchroniser == "oui":
                print("\nCalcul de l'automate synchrone")
                af = fonction.synchronisation(af)
                fonction.afficher_automate(af)
                flag = 1
            if synchroniser == "non":
                print("\nNous ne pouvons pas faire d'autre manipulation sur l'automate choisi")

    if fonction.est_deterministe(af):
        if fonction.est_complet(af):
            print("")

    AFDC = af
    determiniser_completer = input("Voulez-vous determiniser et completer l'automate ? (oui/non) ")
    if determiniser_completer.lower() == "oui":
        if determiniser_completer == "oui":

            print("\nCalcul AFDC")
            if fonction.est_deterministe(af):
                if fonction.est_complet(af):
                    AFDC = af
                else:
                    AFDC = fonction.completion(af)

            else:
                AFDC = fonction.determinisation_completion_automate(af)

    fonction.afficher_automate(af)
    af = AFDC

    minimisei_automate = input("\nVoulez-vous minimiser l'automate ? (oui/non) ")
    if minimisei_automate.lower() == "oui":
        if fonction.est_deterministe(af) and fonction.est_complet(af):
            afdcm = fonction.minimiser_automate(AFDC)

            af = afdcm
        else:
            print("\nL'automate doit être déterministe et complet pour être minimisé.")

    '''
    print("Calcul AFDC")

    fonction.determiniser_completer_automate(af)

    if fonction.est_deterministe(af):
        if fonction.est_complet(af):
            AFDC = af
        else:
            AFDC = fonction.completion(af)
    else:
        AFDC = fonction.determiniser_completer_automate(af)

    fonction.afficher_automate_deterministe_complet(AFDC)
    '''

    lignes = lire_lignes(choix)
    standardiser = input("\nVoulez-vous standardiser l'automate ? (oui/non) ")
    if standardiser.lower() == "oui":
        if non_standard(choix, lignes):
            # Demander à l'utilisateur s'il veut standardiser
            reponse = input(f"Voulez-vous standardiser l'automate {choix} ? (oui/non) : ").strip().lower()
            if reponse == "oui":
                SFA = standardisation(choix, lignes)

                print(f"L'automate {choix} a été standardisé.")
                # Si tu veux, tu peux afficher le nouvel automate

                print("\nNouvel automate standardisé :")
                print("".join(SFA))
            else:

                print(f"L'automate {choix} reste non-standard.")
        else:

            print(f"L'automate {choix} est déjà standard.")

    mot = input("\nEntrer un mot : ")
    while not lire_mot(mot):
        if reconnaitre_mot(mot, af):
            print("\nMot reconnu.")
        else:
            print("\nMot non reconnu.")
        mot = input("\nEntrer un nouveau mot ou finir en écrivant fin : ")


#    fonction.est_un_automate_deterministe(af)
#    fonction.est_un_automate_complet(af)
#    af_complet = fonction.completion(af)
#    fonction.afficher_automate(af_complet)


if __name__ == "__main__":
    main()
