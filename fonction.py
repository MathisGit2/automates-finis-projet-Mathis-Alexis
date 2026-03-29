# faire les differentes fonction

# fonction pour lire l'automates
import os
import re


# AF est une structure à partir d'un dictionnaire avec comme élément :
#   alphabet : liste des symboles (récupérés lors de la lecture des transitions)
#   etats : liste des états de 0 à nombre état
#   initials : liste des états initiauux
#   finals : liste des états finaux
#   transition : liste de dictionnaire ayant en élement { depart, symbole, arrivee}

def lire_automate(choix):
    try:
        chemin = f'automates/automate{choix}.txt'
        print(chemin)

        # lecture des lignes du fichiers
        # lignes contient les lignes non vide du fichier
        with open(chemin, 'r', encoding='utf-8') as f:
            lignes = [l.strip() for l in f.readlines() if l.strip() != '']

        # Extraction des métadonnées
        nb_symboles = int(lignes[0])
        nb_etats = int(lignes[1])

        # Lignes 3 et 4 : on ignore le premier chiffre (le compte)
        initials = lignes[2].split()[1:]
        finals = lignes[3].split()[1:]

        # On initialise la structure avec un dictionnaire
        af = {
            "alphabet": [chr(ord('a') + i) for i in range(nb_symboles)],
            "etats": [str(i) for i in range(nb_etats)],
            "initials": initials,
            "finals": finals,
            "transitions": []  # Structure: { depart, symbole, arrivee }
        }

        nb_trans = int(lignes[4])
        for i in range(nb_trans):
            # Lecture des transitions à partir de la ligne 6 (index 5)
            '''
            t = lignes[5 + i]
            if len(t) >= 3:
                src = t[:-2] if t[:-2].isdigit() else None
                sym = t[-2]
                dst = t[-1] if t[-1].isdigit() else None
            '''
            t = lignes[5 + i]

            match = re.match(r"^(\d+)([a-z])(\d+)$", t)

            if not match:
                print(f"Transition invalide : {t}")
                return None

            src = match.group(1)
            sym = match.group(2)
            dst = match.group(3)

            if (sym not in af["alphabet"]) and sym != "z":
                print(f"Symbole {sym} n'appartenant pas à l'alphabet {af['alphabet']}")
                return None
            # if (src not in af["etats"]):
            if (not src.isdigit()) or (src not in af["etats"]):
                print(f"Etat départ {src} n'appartenant pas à la liste des états {af['etats']}")
                return None
            # if (dst not in af["etats"]):
            if (not dst.isdigit()) or (dst not in af["etats"]):
                print(f"Etat arrivée {dst} n'appartenant pas à la liste des états {af['etats']}")
                return None
                # af["alphabet"].add(sym) #ajout du symbole dans l'alphabet
            # On ajoute la transition sous la forme d'un dictionnaire
            af["transitions"].append({
                "depart": src,
                "symbole": sym,
                "arrivee": dst
            })
        return af
    except Exception as e:
        print(f"Erreur de lecture : {e}")
        return None


# fonction pour aficher l'automates
def afficher_automate(AF):
    etat_initials = AF["initials"]
    etat_finaux = AF["finals"]
    print(f"états initiaux(I): {etat_initials}  /  états finaux(F): {etat_finaux}")

    # Trier pour un affichage constant
    alphabet = sorted(list(AF["alphabet"]))
    etats = sorted(list(AF["etats"]))  # , key=lambda x: (int(x) if x.isdigit() else x))

    larg = max(4, len(str(len(etats) - 1)), *(len(c) for c in alphabet))
    header = 'Etat'.ljust(larg) + ' | ' + ' | '.join(c.center(larg) for c in alphabet)
    header += '|'
    print(header)
    # print('-' * (len(header) + larg))

    for etat in etats:
        cells = []
        for c in alphabet:
            # récupère les destinations, pour le couple départ (état) et symbole (c) dans les transitions de l'automate
            dest = []
            for t in AF["transitions"]:
                if t["depart"] == etat and t["symbole"] == c:
                    dest.append(t["arrivee"])
                    # dest = [t["arrivee"] for t in af["transitions"] if t["depart"] == etat and t["symbole"] == c]
            # print(f"dd : {etat} - {c} ==> {dest}")
            cells.append(','.join(map(str, sorted(dest))) if dest else '--')
        row = str(etat).ljust(larg) + ' | ' + ' | '.join(cell.center(larg) for cell in cells)
        marqueur = ''
        if etat in etat_initials:
            marqueur += ' I'
        if etat in etat_finaux:
            marqueur += ' F'
        row += '|' + marqueur.ljust(larg)
        print(row)
    # print('\nLégende : I=initial, F=final')


def est_asynchrone(AF):
    for t in AF["transitions"]:
        if t["symbole"] == "z":
            AF["asynchrone"] = True
            print("=> L'automate est asynchrone.")
            return True

    AF["asynchrone"] = False
    print("=> L'automate est synchrone.")
    return False


def est_deterministe(AF):
    raisons = []

    # 1. État initial unique
    if len(AF["initials"]) != 1:
        raisons.append(f"Il y a {len(AF['initials'])} états initiaux (attendu : 1).")

    # 2. Doublons de (départ, symbole)
    # On utilise un dictionnaire temporaire pour compter les destinations
    # Clé : (depart, symbole) -> Valeur : liste des arrivées
    vues = {}

    for t in AF["transitions"]:
        dep, sym, arr = t["depart"], t["symbole"], t["arrivee"]
        # Vérification des doublons
        cle = (dep, sym)
        if cle not in vues:  # si la cle (dep,sym) n'extiste pas on la créé avec un tableau d'arrivée à vide
            vues[cle] = []
        vues[cle].append(arr)  # ajout à l'entrée (dep,sym) l'état d'arrivée de la transition

    for (dep, sym), destinations in vues.items():
        if len(destinations) > 1:
            raisons.append(f"L'état {dep} a plusieurs arrivées pour '{sym}' : {destinations}.")

    if not raisons:
        print("=> L'automate est déterministe.")
        return True
    else:
        print("=> L'automate n'est PAS déterministe car :")
        for r in raisons: print(f"   - {r}")
        return False


def est_complet(AF):
    # Pour la complétude, on vérifie que pour chaque état de AF["etats"] et chaque symbole de AF["alphabet"],
    # il existe au moins une transition dans la liste.
    raisons = []
    alphabet = AF["alphabet"]
    etats = AF["etats"]

    # On crée un ensemble de couples (depart, symbole) existants pour une recherche rapide
    couples_existants = {(t["depart"], t["symbole"]) for t in AF["transitions"]}

    for q in etats:
        for s in alphabet:
            if (q, s) not in couples_existants:
                raisons.append(f"L'état {q} n'a aucune transition pour le symbole '{s}'.")

    if not raisons:
        print("=> L'automate est complet.")
        return True
    else:
        print("=> L'automate n'est PAS complet car :")
        for r in raisons: print(f"   - {r}")
        return False


def fermeture_z(AF, etat):
    fermeture = {etat}
    a_traiter = [etat]

    while a_traiter:
        courant = a_traiter.pop(0)

        for t in AF["transitions"]:
            if t["depart"] == courant and t["symbole"] == "z":
                arrivee = t["arrivee"]

                if arrivee not in fermeture:
                    fermeture.add(arrivee)
                    a_traiter.append(arrivee)

    return fermeture


def synchronisation(AF):
    # On construire l'alphabet sans z
    alphabet = []
    for s in AF["alphabet"]:
        if s != "z":
            alphabet.append(s)

    # On garde les etats initiaux
    etat_initial = AF["initials"][0]

    # On regroupe les nouveaux etats qui ne vient pas d'une transition de z
    nouveaux_etats = [etat_initial]

    for t in AF["transitions"]:
        if t["symbole"] != "z":
            if t["arrivee"] not in nouveaux_etats:
                nouveaux_etats.append(t["arrivee"])

    # On détermine les nouveaux états finaux
    nouveaux_finaux = []

    for etat in nouveaux_etats:
        fz = fermeture_z(AF, etat)

        for f in AF["finals"]:
            if f in fz:
                nouveaux_finaux.append(etat)
                break

    # Supprimer les doublons dans les états finaux
    nouveaux_finaux = list(set(nouveaux_finaux))

    # Construire les nouvelles transitions sans z
    nouvelles_transitions = []

    for etat in nouveaux_etats:
        fz = fermeture_z(AF, etat)

        for sym in alphabet:
            destinations = set()

            for e in fz:
                for t in AF["transitions"]:
                    if t["depart"] == e and t["symbole"] == sym:
                        arrivee = t["arrivee"]
                        destinations.add(arrivee)

            for d in destinations:
                transition = {
                    "depart": etat,
                    "symbole": sym,
                    "arrivee": d
                }

                if transition not in nouvelles_transitions:
                    nouvelles_transitions.append(transition)

    nouveaux_etats = sorted(nouveaux_etats, key=int)
    nouveaux_finaux = sorted(nouveaux_finaux, key=int)

    nouvelles_transitions = sorted(
        nouvelles_transitions,
        key=lambda t: (int(t["depart"]), t["symbole"], int(t["arrivee"]))
    )

    # Créer le nouvel automate synchronisé
    nouveau_AF = {
        "alphabet": alphabet,
        "etats": nouveaux_etats,
        "initials": AF["initials"][:],
        "finals": nouveaux_finaux,
        "transitions": nouvelles_transitions
    }

    print("=> L'automate asynchrone a été synchronisé.")
    return nouveau_AF


def completion(AF):
    # ajouter un état poubelle "P" et créer les transitions manquantes vers la poubelle
    alphabet = sorted(list(AF["alphabet"]))
    etats = AF["etats"]
    transitions = AF["transitions"]

    # On définit le nom de l'état poubelle
    p = "P"

    besoin_p = False
    nouvelles_transitions = list(transitions)  # Copie de la liste originale

    for q in etats:
        for s in alphabet:
            # VERIFICATION : existe-t-il déjà une transition pour ce (départ, symbole) ?
            existe = any(t["depart"] == q and t["symbole"] == s for t in AF["transitions"])

            if not existe:
                nouvelles_transitions.append({
                    "depart": q,
                    "symbole": s,
                    "arrivee": p
                })
                besoin_p = True

    if besoin_p:
        if p not in AF["etats"]:
            AF["etats"].append(p)
        # L'état poubelle doit boucler sur lui-même pour TOUT l'alphabet
        for s in alphabet:
            # On n'ajoute la boucle que si elle n'existe pas encore
            if not any(t["depart"] == p and t["symbole"] == s for t in nouvelles_transitions):
                nouvelles_transitions.append({
                    "depart": p, "symbole": s, "arrivee": p
                })
        print(f"INFO : L'automate a été complété avec l'état poubelle '{p}'.")
    else:
        print("INFO : L'automate était déjà complet, aucune modification nécessaire.")

    AF["transitions"] = nouvelles_transitions
    return AF


def determinisation_completion_automate(AFN):
    # tri de l'alphabet
    alphabet = sorted(list(AFN["alphabet"]))
    # Définir l'état initial composé
    # On trie pour que {1, 2} et {2, 1} donnent toujours "1.2"
    etat_init_liste = sorted(list(AFN["initials"]), key=lambda x: int(x) if x.isdigit() else x)
    nom_init = ".".join(etat_init_liste)

    if not nom_init:  # Cas rare où il n'y a pas d'état initial
        return AFN

    # Structures pour l'AFD
    etats_afd = [nom_init]
    transitions_afd = []
    finals_afd = []

    # File d'attente pour explorer les nouveaux états composés
    file_attente = [nom_init]
    visites = set()

    while file_attente:
        courant_nom = file_attente.pop(0)
        if courant_nom in visites:
            continue
        visites.add(courant_nom)

        # Si l'état courant contient un état final de l'AFN, il est final dans l'AFD
        composants = courant_nom.split(".")
        if any(c in AFN["finals"] for c in composants):
            if courant_nom not in finals_afd:
                finals_afd.append(courant_nom)

        for sym in alphabet:
            # Trouver tous les états atteignables depuis tous les composants
            prochains = set()
            for c in composants:
                # On cherche dans les transitions de l'AFN (liste de tuples)
                for t in AFN["transitions"]:
                    if t["depart"] == c and t["symbole"] == sym:
                        prochains.add(t["arrivee"])

            # Si on a des destinations, on crée l'état composé
            if prochains:
                liste_prochains = sorted(list(prochains), key=lambda x: int(x) if x.isdigit() else x)
                nom_prochain = ".".join(liste_prochains)
                # Ajouter la transition à l'AFD
                transitions_afd.append({"depart": courant_nom, "symbole": sym, "arrivee": nom_prochain})
                # Si cet état est nouveau, on l'ajoutera à la file
                if nom_prochain not in visites:
                    file_attente.append(nom_prochain)
                    if nom_prochain not in etats_afd:
                        etats_afd.append(nom_prochain)

    # Construire l'objet AFD
    AFD = {
        "alphabet": alphabet,
        "etats": etats_afd,
        "initials": [nom_init],
        "finals": finals_afd,
        "transitions": transitions_afd
    }
    # construction de l'AFDC par complétion des transitions manquantes
    AFDC = completion(AFD)

    return AFDC


def obtenir_index_classe(etat, partition):
    # Retourne l'indice de la classe contenant l'état donné
    for i, classe in enumerate(partition):
        if etat in classe:
            return i
    return -1


def afficher_transitions_classes(partition, alphabet, transitions_afdc, etape):
    # Affiche les transitions exprimées en termes de classes (consigne projet)
    print(f"\nTransitions à l'étape P{etape} :")
    for i, classe in enumerate(partition):
        representant = classe[0]
        for sym in alphabet:
            # On cherche la destination dans l'AFDC original
            dest = next(t["arrivee"] for t in transitions_afdc if t["depart"] == representant and t["symbole"] == sym)
            index_dest = obtenir_index_classe(dest, partition)
            print(f"  Classe {i} --({sym})--> Classe {index_dest}")


def sont_equivalents(e1, e2, alphabet, partition, transitions_afdc):
    # Vérifie si deux états e1 et e2 sont équivalents (vont vers les mêmes classes)
    for sym in alphabet:
        dest1 = next(t["arrivee"] for t in transitions_afdc if t["depart"] == e1 and t["symbole"] == sym)
        dest2 = next(t["arrivee"] for t in transitions_afdc if t["depart"] == e2 and t["symbole"] == sym)

        if obtenir_index_classe(dest1, partition) != obtenir_index_classe(dest2, partition):
            return False
    return True


def minimiser_automate(AFDC):
    print("\nPHASE DE MINIMISATION :")

    alphabet = sorted(AFDC["alphabet"])
    etats = sorted(AFDC["etats"])

    # P0 : Séparation terminaux / non-terminaux
    finals = sorted(AFDC["finals"])
    non_finals = sorted([e for e in etats if e not in finals])
    partition = [p for p in [non_finals, finals] if p]

    iteration = 0
    while True:
        print(f"\nPartition P{iteration} : {partition}")
        # Appeler l'affichage des transitions par classes
        afficher_transitions_classes(partition, alphabet, AFDC["transitions"], iteration)

        nouvelle_partition = []
        for classe in partition:
            if not classe: continue
            classes_eclatees = []

            for etat in classe:
                trouve = False
                for sous_classe in classes_eclatees:
                    if sont_equivalents(etat, sous_classe[0], alphabet, partition, AFDC["transitions"]):
                        sous_classe.append(etat)
                        trouve = True
                        break
                if not trouve:
                    classes_eclatees.append([etat])

            nouvelle_partition.extend(classes_eclatees)

        nouvelle_partition.sort()

        # Vérification de la stabilité
        if nouvelle_partition == partition:
            print(f"\nStabilité atteinte à P{iteration}.")
            break

        partition = nouvelle_partition
        iteration += 1

    # Vérification si déjà minimal
    if len(partition) == len(etats):
        print("\n=> INFO : L'automate était déjà minimal (aucune fusion possible).")
        return AFDC

    # Construction de l'AFDCM
    AFDCM = {
        "alphabet": alphabet,
        "etats": [".".join(c) for c in partition],
        "initials": [],
        "finals": [],
        "transitions": [],
        "correspondance": {}
    }

    for c in partition:
        nom = ".".join(c)
        AFDCM["correspondance"][nom] = c

        if any(e in AFDC["initials"] for e in c):
            AFDCM["initials"].append(nom)
        if any(e in AFDC["finals"] for e in c):
            AFDCM["finals"].append(nom)

        rep = c[0]
        for sym in alphabet:
            d_orig = next(t["arrivee"] for t in AFDC["transitions"] if t["depart"] == rep and t["symbole"] == sym)
            d_nom = ".".join(next(cp for cp in partition if d_orig in cp))
            AFDCM["transitions"].append({"depart": nom, "symbole": sym, "arrivee": d_nom})

    # Affichage final
    print("\nTABLE DE CORRESPONDANCE :")
    for k, v in AFDCM["correspondance"].items():
        print(f"  Nouvel état '{k}' regroupe les anciens : {v}")

    print("\nSTRUCTURE FINALE (AFDCM) :")
    # Utilisation de ta fonction existante pour l'affichage propre
    from fonction import afficher_automate
    # Si la fonction n'est pas dans le même fichier ou déjà importée :
    try:
        afficher_automate(AFDCM)
    except:
        # Fallback si afficher_automate n'est pas accessible ici
        for t in AFDCM["transitions"]:
            print(f"  {t['depart']} --({t['symbole']})--> {t['arrivee']}")

    return AFDCM


def lire_lignes(choix):
    chemin = f'Automates/automate{choix}.txt'
    with open(chemin, 'r', encoding='utf-8') as fichier:
        lignes = [l.strip() for l in fichier if l.strip() != '']
        return lignes


def non_standard(choix, lignes):
    etats_initiaux = lignes[2].split()[1:]

    # Vérifier s'il y a plus d'un état initial
    if len(etats_initiaux) != 1:
        print(f"L'automate {choix} n'est pas standard : il comporte plusieurs états initiaux")
        return True

    etat_initial = etats_initiaux[0]
    transitions = lignes[5:]

    # Vérifier les transitions vers l'état initial
    for t in transitions:
        t = t.strip()

        arrivee = None
        for j, c in enumerate(t):
            if c.isalpha():
                arrivee = t[j + 1:]
                break

        if arrivee == etat_initial:
            print(f"L'automate {choix} n'est pas standard : il comporte des transitions vers l'état initial")
            return True

    return False


def standardisation(choix, lignes):
    # Vérifier si l'automate est déjà standard
    if not non_standard(choix, lignes):
        print(f"L'automate {choix} est déjà standard")
        return lignes

    etats_initiaux = lignes[2].split()[1:]
    etats_finaux = lignes[3].split()[1:]
    transitions = lignes[5:]
    nb_etats = int(lignes[1].strip())

    nouvel_etat = nb_etats
    nouvelles_transitions = []

    for t in transitions:
        depart = ''
        symbole = ''
        arrivee = ''

        for j, c in enumerate(t):
            if c.isalpha():
                depart = t[:j]
                symbole = c
                arrivee = t[j + 1:]
                break

        if depart in etats_initiaux:
            nouvelles_transitions.append(f"{nouvel_etat}{symbole}{arrivee}")

    # Ajouter les transitions
    # On crée une nouvelle liste pour toutes les transitions avec un retour à la ligne
    toutes_transitions = []

    # Ajouter les transitions existantes
    for t in transitions + nouvelles_transitions:
        toutes_transitions.append(t + "\n")

    # Mettre à jour les lignes
    lignes[1] = "\n" + f"{nb_etats + 1}\n"
    lignes[2] = f"1 {nouvel_etat}\n"

    # Mettre à jour les états finaux si l'état initial de base était final
    for i in etats_initiaux:
        if i in etats_finaux:
            etats_finaux.append(str(nouvel_etat))
            break
    lignes[3] = f"{len(etats_finaux)} {' '.join(etats_finaux)}\n"

    lignes[4] = str(len(lignes[5:])) + "\n"

    lignes[5:] = toutes_transitions

    # Écriture dans le fichier
    nom_fichier = f"Automates/automatestandard{choix}.txt"
    with open(nom_fichier, "w") as f:
        f.writelines(lignes)

    print(f"Le fichier {nom_fichier} a été créé avec l'automate standardisé")
    return nom_fichier


# Reconnaissance de mots

def lire_mot(mot):
    print("le mot est : ", mot)
    if mot == "fin":
        return 1
    else:
        return 0


def reconnaitre_mot(mot, af):
    """Retourne True si mot est accepté par l'automate af, sinon False."""
    if af is None or mot is None:
        return False

    # Cas du mot vide : accepter si un état initial est final
    if mot == "":
        return any(initial in af["finals"] for initial in af["initials"])

    current_states = set(af["initials"])
    for c in mot:
        if c not in af["alphabet"]:
            return False

        next_states = set()
        for t in af["transitions"]:
            if t["depart"] in current_states and t["symbole"] == c:
                next_states.add(t["arrivee"])

        current_states = next_states
        if not current_states:
            return False

    return any(state in af["finals"] for state in current_states)

def automate_complementaire(A, source="AFDC"):
    # Construction de l'automate du langage complémentaire
    # On échange simplement les états finaux et non-finaux
    print(f"\n=> Construction de l'automate complémentaire à partir de l'{source}.")

    # Les états finaux du complémentaire sont les NON-finaux de A
    nouveaux_finals = [e for e in A["etats"] if e not in A["finals"]]

    AComp = {
        "alphabet": list(A["alphabet"]),
        "etats": list(A["etats"]),
        "initials": list(A["initials"]),
        "finals": nouveaux_finals,
        "transitions": [dict(t) for t in A["transitions"]]
    }

    print("=> Automate complémentaire construit (échange états finaux <-> non-finaux).")
    return AComp
