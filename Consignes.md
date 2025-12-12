# Mini Projet Python : Système de Location de Voitures insolites

## Objectif Général 

Développer une application de gestion de location de voitures basée sur les principes de la programmation orientée objet.

Cette application doit permettre à une agence de location de : 
* gérer son parc automobile,
* gérer ses clients
* effectuer et suivre les locations
* calculer le coût d'une location
* générer des rapports

## Fonctionnalités attendues

### 1. Gestion de la flotte automobile (Frédéric)

- Hiérarchie de classes : Vehicle, Car, Truck, Motorcycle, Poney, Corbillard, Tracteur, Kart
- Attributs : id, marque, modèle, catégorie, tarif, état
- Option avancée : entretien

### 2. Gestion des clients (Maxence)

- Classe Customer : id, nom, prénom, âge, permis, historique=fidélité
- Règles : âge minimum selon véhicule

### 3. Système de réservation (Rental) (Clémence)

- Données : client, véhicule, dates, coût total
- Règles : disponibilité, dates valides, pénalités

### 4. Classe centrale CarRentalSystem (Frédéric)

- Gestion : véhicules, clients, locations, recherche, rapports

## Rapport (Clémence)

- Véhicules disponibles
- Locations en cours
- Chiffre d’affaires
- Statistiques

## Livrable

- Code en modules (repo GitHub)
- UML de calsses
- README
- Tests unitaires

draw.io integration
fast api
