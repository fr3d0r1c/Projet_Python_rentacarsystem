from datetime import date, timedelta
from GestionFlotte.transport_base import TransportMode, MotorizedVehicle, TransportAnimal
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
        delta = self.end_date - self.start_date
        days = delta.days
        if days < 1: days = 1
        return days * self.vehicle.daily_rate
    
    def close_rental(self):
        self.is_active = False
        print(f"✅ Location #{self.id} terminée.")

    def show_details(self):
        status = "🟢 En cours" if self.is_active else "🔴 Terminée"

        if isinstance(self.vehicle, MotorizedVehicle):
            veh_info = f"{self.vehicle.brand} {self.vehicle.model}"

        elif isinstance(self.vehicle, TransportAnimal):
            veh_info = f"{self.vehicle.name} ({self.vehicle.breed})"

        else:
            veh_info = f"{self.vehicle.__class__.__name__} ({self.vehicle.seat_count} pl.)"

        return (f"[Loc #{self.id}] {veh_info} "
                f"loué par {self.customer.name} ({self.start_date} -> {self.end_date}) "
                f"- Total: {self.total_price}€ - {status}")
    
    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle.id,
            "customer_id": self.customer.id,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            "total_price": self.total_price,
            "is_active": self.is_active
        }