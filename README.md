# automates-finis-projet-Mathis-Alexis
Projet EFREI P2 : traitement d'automates finis (déterminisation, complétion, minimisation, reconnaissance de mots).

## Description

Ce programme permet de traiter des automates finis à partir de fichiers texte. Il prend en charge l'ensemble des opérations classiques sur les automates : de la lecture jusqu'à la construction du langage complémentaire, en passant par la déterminisation, la minimisation et la reconnaissance de mots.

Le programme peut traiter plusieurs automates à la suite sans avoir à être relancé.

## Fonctionnalités

- **Lecture et affichage** — chargement d'un automate depuis un fichier `.txt` et affichage de sa table de transitions
- **Détection** — vérifie si l'automate est synchrone, déterministe et/ou complet
- **Synchronisation** — suppression des transitions epsilon (ε) pour obtenir un automate synchrone
- **Standardisation** — transformation de l'automate en automate standard (un seul état initial sans transition entrante)
- **Déterminisation et complétion** — construction de l'automate déterministe et complet équivalent (AFDC)
- **Minimisation** — réduction de l'automate au nombre minimal d'états (AFDCM), avec affichage des partitions successives
- **Reconnaissance de mots** — test de plusieurs mots pour savoir s'ils sont acceptés ou non par l'automate
- **Langage complémentaire** — construction de l'automate reconnaissant le langage complémentaire

## Mathis Roca Alexis Rajabally

Projet réalisé en équipe dans le cadre du projet d'Automates Finis — EFREI P2 2025/2026.
