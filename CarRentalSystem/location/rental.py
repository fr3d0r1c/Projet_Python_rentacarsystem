from datetime import date

from GestionFlotte.transport_base import TransportMode
from clients.customer import Customer

class Rental:
    def __init__(self, r_id: int, vehicle: TransportMode, customer: Customer, start_date: date, end_date: date):
        self.id = r_id
        self.vehicle = vehicle
        self.customer = customer
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = True

        self.total_price = self.calculate_total_price()

    def calculate_total_price(self):
        """Calcule le prix en fonction de la durée et du tarif du véhicule"""
        delta = self.end_date - self.start_date
        days = delta.days

        if days < 1:
            days = 1
            
        return days * self.vehicle.daily_rate
    
    def close_rental(self):
        """Termine la location"""
        self.is_active = False
        print(f"✅ Location #{self.id} terminée.")

    def show_details(self):
        status = "🟢 En cours" if self.is_active else "🔴 Terminée"
        return (f"[Loc #{self.id}] {self.vehicle.brand} {self.vehicle.model} "
                f"loué par {self.customer.name} ({self.start_date} -> {self.end_date}) "
                f"- Total: {self.total_price}€ - {status}")
    
    def to_dict(self):
        """
        Pour la sauvegarde, on garde uniquement les IDs du client et du véhicule.
        Cela évite de sauvegarder tout l'objet véhicule en double.
        """
        return {
            "id": self.id,
            "vehicle_id": self.vehicle.id,   # Clé étrangère
            "customer_id": self.customer.id, # Clé étrangère
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "total_price": self.total_price,
            "is_active": self.is_active
        }