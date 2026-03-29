import fonction
from fonction import (
    lire_automate, non_standard, standardisation, lire_lignes, lire_mot,
    reconnaitre_mot, determinisation_completion_automate, minimiser_automate,
    obtenir_index_classe, afficher_transitions_classes, sont_equivalents,
    automate_complementaire
)

# Liste de tous les numéros d'automates acceptés (de 01 à 44)
CHOIX_VALIDES = [f"{i:02d}" for i in range(1, 45)]


def choisir_automate():
    # On répète la question tant que l'utilisateur ne donne pas un numéro valide
    while True:
        choix = input("\nQuel automate voulez-vous utiliser ? (01 à 44, ou 'quitter') : ").strip()
        if choix.lower() == 'quitter':
            return None
        if choix in CHOIX_VALIDES:
            print(f"Automate {choix} sélectionné.")
            return choix
        print("Numéro invalide. Entrez un nombre entre 01 et 44.")


def traiter_automate(choix):
    # Fonction principale qui enchaîne toutes les étapes de traitement


    # Étape 1 : chargement de l'automate depuis le fichier et affichage

    af = lire_automate(choix)
    if af is None:
        print("\nImpossible de lire l'automate. Traitement annulé.")
        return

    print("\n=== AUTOMATE INITIAL ===")
    fonction.afficher_automate(af)

    # Étape 2 : si l'automate contient des transitions epsilon (z),
    # on propose à l'utilisateur de le synchroniser
    if fonction.est_asynchrone(af):
        rep = input("Voulez-vous synchroniser l'automate ? (oui/non) : ").strip().lower()
        if rep == "oui":
            print("\nSynchronisation en cours :")
            af = fonction.synchronisation(af)
            print("\n=== AUTOMATE SYNCHRONISE ===")
            fonction.afficher_automate(af)
        else:
            # Sans synchronisation on ne peut pas aller plus loin
            print("\nTraitement impossible sur un automate asynchrone non synchronisé. Arrêt.")
            return


    # Étape 3 : on vérifie si l'automate est déterministe et/ou complet

    print("\n--- Analyse de l'automate ---")
    det = fonction.est_deterministe(af)
    comp = fonction.est_complet(af)


    # Étape 4 : standardisation à la demande de l'utilisateur

    lignes = lire_lignes(choix)
    rep = input("\nVoulez-vous standardiser l'automate ? (oui/non) : ").strip().lower()
    if rep == "oui":
        if non_standard(choix, lignes):
            # On demande une confirmation avant de modifier
            rep2 = input(f"L'automate {choix} n'est pas standard. Lancer la standardisation ? (oui/non) : ").strip().lower()
            if rep2 == "oui":
                resultat = standardisation(choix, lignes)
                print(f"\nFichier standardisé enregistré : {resultat}")
        else:
            print(f"\nL'automate {choix} est déjà standard, aucune modification nécessaire.")


    # Étape 5 : déterminisation et complétion
    # On suit le pseudo-code du sujet à la lettre

    AFDC = af  # valeur par défaut si l'utilisateur refuse

    rep = input("\nVoulez-vous déterminiser et compléter l'automate ? (oui/non) : ").strip().lower()
    if rep == "oui":
        print("\nConstruction de l'AFDC :")
        if det:
            if comp:
                # Déjà déterministe et complet : rien à faire
                AFDC = af
                print("=> L'automate est déjà déterministe et complet.")
            else:
                # Déterministe mais pas complet : on ajoute juste l'état poubelle
                AFDC = fonction.completion(af)
        else:
            # Non déterministe : déterminisation + complétion complètes
            AFDC = fonction.determinisation_completion_automate(af)

        print("\n=== AUTOMATE DETERMINISTE ET COMPLET (AFDC) ===")
        fonction.afficher_automate(AFDC)
    else:
        # Si l'utilisateur refuse mais que l'automate n'est pas AFDC,
        # on le calcule quand même en arrière-plan pour les étapes suivantes
        if not (det and comp):
            print("\nATTENTION : l'automate n'est pas déterministe et complet.")
            print("Calcul de l'AFDC en arrière-plan pour pouvoir continuer ...")
            if det:
                AFDC = fonction.completion(af)
            else:
                AFDC = fonction.determinisation_completion_automate(af)
            print("\n=== AFDC (calculé automatiquement) ===")
            fonction.afficher_automate(AFDC)


    # Étape 6 : minimisation de l'AFDC

    AFDCM = AFDC  # on part de l'AFDC par défaut

    rep = input("\nVoulez-vous minimiser l'automate ? (oui/non) : ").strip().lower()
    if rep == "oui":
        # La minimisation n'est applicable que sur un automate déterministe et complet
        if fonction.est_deterministe(AFDC) and fonction.est_complet(AFDC):
            AFDCM = fonction.minimiser_automate(AFDC)
        else:
            print("\nLa minimisation nécessite un automate déterministe et complet.")


    # Étape 7 : test de reconnaissance de mots
    #On boucle jusqu'à ce que l'utilisateur tape "fin"

    print("\n--- Test de mots (entrez 'fin' pour quitter cette section) ---")
    automate_recog = AFDCM  # on utilise l'automate le plus réduit disponible
    mot = input("Entrez un mot à tester : ").strip()
    while lire_mot(mot) == 0:  # lire_mot retourne 0 si le mot n'est pas "fin"
        if reconnaitre_mot(mot, automate_recog):
            print("=> Ce mot est ACCEPTÉ par l'automate.")
        else:
            print("=> Ce mot est REJETÉ par l'automate.")
        mot = input("Mot suivant (ou 'fin' pour arrêter) : ").strip()


    # Étape 8 : construction de l'automate du langage complémentaire

    rep = input("\nVoulez-vous obtenir l'automate du langage complémentaire ? (oui/non) : ").strip().lower()
    if rep == "oui":
        # On indique clairement depuis quel automate le complémentaire est construit
        source_label = "AFDCM" if AFDCM is not AFDC else "AFDC"
        AComp = automate_complementaire(AFDCM, source=source_label)
        print(f"\n=== AUTOMATE COMPLEMENTAIRE (construit depuis {source_label}) ===")
        fonction.afficher_automate(AComp)


def main():
    print("\n=====================================================")
    print("   Bienvenue dans le programme d'automates finis")
    print("=====================================================")

    # On tourne en boucle pour permettre de traiter plusieurs automates
    # sans avoir à relancer le programme
    while True:
        choix = choisir_automate()
        if choix is None:
            # L'utilisateur a tapé "quitter"
            print("\nFin du programme. À bientôt !")
            break

        traiter_automate(choix)

        # On demande si l'utilisateur veut continuer avec un autre automate
        continuer = input("\nTraiter un autre automate ? (oui/non) : ").strip().lower()
        if continuer != "oui":
            print("\nFin du programme. À bientôt !")
            break


if __name__ == "__main__":
    main()