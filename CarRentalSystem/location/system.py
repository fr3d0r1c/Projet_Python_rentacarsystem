from datetime import date
from typing import List, Optional

# On importe nos briques
from GestionFlotte.transport_base import TransportMode
from GestionFlotte.enums import VehicleStatus
from clients.customer import Customer
from .rental import Rental


class CarRentalSystem:
    def __init__(self):
        # Les 3 listes principales de votre base de données en mémoire
        self.fleet: List[TransportMode] = []
        self.customers: List[Customer] = []
        self.rentals: List[Rental] = []

    # --- GESTION DE LA FLOTTE ---
    def add_vehicle(self, vehicle: TransportMode):
        self.fleet.append(vehicle)
        print(f"Véhicule ajouté : {vehicle.brand} {vehicle.model} (ID: {vehicle.id})")

    def find_vehicle(self, v_id: int) -> Optional[TransportMode]:
        """Cherche un véhicule par son ID"""
        for v in self.fleet:
            if v.id == v_id:
                return v
        return None

    # --- GESTION DES CLIENTS ---
    def add_customer(self, customer: Customer):
        self.customers.append(customer)
        print(f"Client enregistré : {customer.name} (ID: {customer.id})")

    def find_customer(self, c_id: int) -> Optional[Customer]:
        """Cherche un client par son ID"""
        for c in self.customers:
            if c.id == c_id:
                return c
        return None

    # --- CŒUR DU MÉTIER : LA LOCATION ---
    def rent_vehicle(self, customer_id: int, vehicle_id: int, start: date, end: date):
        """
        Tente de créer une location.
        Vérifie si le véhicule existe, s'il est disponible, et si le client existe.
        """
        # 1. On récupère les objets
        client = self.find_customer(customer_id)
        vehicule = self.find_vehicle(vehicle_id)

        # 2. Vérifications de sécurité
        if not client:
            print("❌ Erreur : Client introuvable.")
            return None
        
        if not vehicule:
            print("❌ Erreur : Véhicule introuvable.")
            return None

        if vehicule.status != VehicleStatus.AVAILABLE:
            print(f"❌ Erreur : Le véhicule {vehicule.brand} n'est pas disponible (Statut : {vehicule.status.value}).")
            return None

        # 3. Création du contrat
        # On génère un ID unique pour la location (taille de la liste + 1)
        rental_id = len(self.rentals) + 1
        new_rental = Rental(rental_id, vehicule, client, start, end)
        
        # 4. Enregistrement et Mise à jour du statut
        self.rentals.append(new_rental)
        vehicule.status = VehicleStatus.RENTED
        
        print(f"✅ Location validée ! {client.name} part avec la {vehicule.brand} pour {new_rental.total_price}€.")
        return new_rental

    def return_vehicle(self, rental_id: int):
        """Clôture une location et rend le véhicule disponible"""
        # On cherche la location
        target_rental = None
        for r in self.rentals:
            if r.id == rental_id:
                target_rental = r
                break
        
        if target_rental and target_rental.is_active:
            target_rental.close_rental()
            # IMPORTANT : On libère le véhicule
            target_rental.vehicle.status = VehicleStatus.AVAILABLE
            print(f"🚗 Véhicule {target_rental.vehicle.brand} retourné et disponible.")
        else:
            print("❌ Erreur : Location introuvable ou déjà clôturée.")