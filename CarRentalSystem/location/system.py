from datetime import date
from typing import List, Optional, Type

# Imports des modules voisins
from GestionFlotte.transport_base import TransportMode
from GestionFlotte.enums import VehicleStatus
from clients.customer import Customer
from .rental import Rental

class CarRentalSystem:
    def __init__(self):
        # Les 3 listes principales (Base de données en mémoire)
        self.fleet: List[TransportMode] = []
        self.customers: List[Customer] = []
        self.rentals: List[Rental] = []

    # ==========================================
    # 1. GESTION (CRUD)
    # ==========================================
    
    def add_vehicle(self, vehicle: TransportMode):
        self.fleet.append(vehicle)
        # Pas de print ici pour ne pas polluer l'interface, on laisse l'UI gérer

    def find_vehicle(self, v_id: int) -> Optional[TransportMode]:
        return next((v for v in self.fleet if v.id == v_id), None)

    def add_customer(self, customer: Customer):
        self.customers.append(customer)

    def find_customer(self, c_id: int) -> Optional[Customer]:
        return next((c for c in self.customers if c.id == c_id), None)

    # ==========================================
    # 2. GESTION DES LOCATIONS (CORE)
    # ==========================================

    def create_rental(self, customer_id: int, vehicle_id: int, start: date, end: date) -> Optional[Rental]:
        """Crée un contrat de location si tout est valide."""
        client = self.find_customer(customer_id)
        vehicule = self.find_vehicle(vehicle_id)

        # Vérifications
        if not client:
            print("❌ Erreur : Client introuvable.")
            return None
        if not vehicule:
            print("❌ Erreur : Véhicule introuvable.")
            return None
        if vehicule.status != VehicleStatus.AVAILABLE:
            print(f"❌ Indisponible : Ce véhicule est actuellement {vehicule.status.value}.")
            return None

        # Création
        new_id = len(self.rentals) + 1
        rental = Rental(new_id, vehicule, client, start, end)
        
        # Enregistrement
        self.rentals.append(rental)
        
        # Mise à jour du statut du véhicule
        vehicule.status = VehicleStatus.RENTED
        
        print(f"✅ Location validée pour {rental.total_price}€")
        return rental

    def return_vehicle(self, rental_id: int):
        """Clôture une location."""
        rental = next((r for r in self.rentals if r.id == rental_id), None)

        if rental and rental.is_active:
            rental.close_rental()
            rental.vehicle.status = VehicleStatus.AVAILABLE

            if hasattr(rental.vehicle, 'brand'):
                nom_vehicule = f"{rental.vehicle.brand} {rental.vehicle.model}"
            elif hasattr(rental.vehicle, 'name'):
                nom_vehicule = f"{rental.vehicle.name} ({rental.vehicle.breed})"
            else:
                nom_vehicule = "Véhicule/Attelage"

            print(f"🚗 Retour confirmé pour {nom_vehicule}.")
        else:
            print("❌ Erreur : Location introuvable ou déjà terminée.")

    # ==========================================
    # 3. RECHERCHE (SEARCH)
    # ==========================================

    def search_vehicles(self, 
                        vehicle_type: Type[TransportMode] = None, 
                        available_only: bool = True, 
                        max_price: float = None) -> List[TransportMode]:
        """
        Filtre la flotte selon plusieurs critères.
        Ex: Trouver toutes les Voitures disponibles à moins de 100€.
        """
        results = []
        for v in self.fleet:
            # Critère 1 : Disponibilité
            if available_only and v.status != VehicleStatus.AVAILABLE:
                continue
            
            # Critère 2 : Type (ex: chercher que les Bateaux)
            if vehicle_type and not isinstance(v, vehicle_type):
                continue

            # Critère 3 : Prix max
            if max_price and v.daily_rate > max_price:
                continue
            
            results.append(v)
        
        return results

    # ==========================================
    # 4. RAPPORTS (REPORTS)
    # ==========================================

    def generate_active_rentals_report(self):
        """Affiche toutes les locations en cours."""
        print("\n--- 📄 RAPPORT : LOCATIONS ACTIVES ---")
        active_rentals = [r for r in self.rentals if r.is_active]
        
        if not active_rentals:
            print("Aucune location en cours.")
        else:
            for r in active_rentals:
                print(r.show_details())
        print("--------------------------------------")

    def generate_revenue_report(self):
        """Calcule le chiffre d'affaires total."""
        total_revenue = sum(r.total_price for r in self.rentals)
        print(f"\n--- 💰 RAPPORT FINANCIER ---")
        print(f"Nombre total de contrats : {len(self.rentals)}")
        print(f"Chiffre d'Affaires Total : {total_revenue}€")
        print("----------------------------")
        return total_revenue