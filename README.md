# Projet de session INM5151

## Description

Dans le cadre du cours **Projet d'analyse et de modélisation (INM5151)** pour **le programme de baccalauréat en informatique et génie logiciel** de l'UQAM.


Le projet se base sur des éléments spéculatifs en raison de sa nature académique. 

Economeuble est une plateforme permettant aux utilisateurs d'acheter ou de vendre des meubles neufs ou usagés de nature antique ou artisanale.


## Auteurs

CHAN, JOANNE - CHAJ03539105 

EL-HENI, ELA - ELHE24579402 

LIMANE, MOUAD - LIMM15019000 

YOUNES, JULIEN - YOUJ19059900 

ZIDANI, DJAMEL - ZIDD29019507

## Plateformes supportées

Ce prototype a été créée et téstée sous la plateforme macOS.

## Installation

Le microframework utilisé est Flask pour Python basé sur le moteur de templates Jinja2, ce dernier sert à simplifier l'utilisation des requetes HTTP.

Pour executer l'application il faut d'abord installer Flask ainsi que toutes les [librairies nécessaires](requirments.txt) à l'aide de la commande :

`pip3 install <librairie>`

Ensuite, lancer la commande :

`python3 run.py`

## Fonctionnalités réalisées :

- Création d'un compte
- Connexion
- Modification des informations personnelles
- Deconnexion
- Ajout d'un article
- Modification d'un article
- Suppression d'un article
- Affichage du profil d'un vendeur
- Affichage d'un article
- Ajout d'un article au panier
- Récupération d'un mot de passe

## Base de données

La base données utilisée : SQLite

Librairie : SQLAlchemy

[Une base de données](./economeuble/database.db) est disponible dans le projet.


Pour en créer une autre :

`eport FLASK_APP = manage.py`


`flask shell()`


`db.create_all()`


`exit()`

## Technologies utilisées

Dans le front-end :
- HTML5
- CSS 3
- Bootstrap
- JavaScript

Dans le back-end
- Python 3.8.1
- Flask 1.1.1
- SQLite
- Jinja 2

## Références 

- https://github.com/jacquesberger/exemplesINF5190
- https://github.com/elaelheni/Projet-de-session-INF5190
- https://codyhouse.co/demo/faq-template/index.html
- https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css
- https://use.fontawesome.com/releases/v5.0.13/js/solid.js
- https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js
- https://code.jquery.com/jquery-3.3.1.slim.min.js
- https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js
- https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js

## Sources des images:

- https://www.google.com/

