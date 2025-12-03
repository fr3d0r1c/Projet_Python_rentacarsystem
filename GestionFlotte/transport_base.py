from abc import ABC, abstractmethod
from typing import List
from enums import VehicleStatus
from maintenance import Maintenance

class TransportMode(ABC):
    def __init__(self, t_id: int, daily_rate: float):
        self.id = t_id
        self.daily_rate = daily_rate
        self.status = VehicleStatus.AVAILABLE
        self.maintenance_log: List[Maintenance] = []

    def add_maintenance(self, maintenance: Maintenance):
        self.maintenance_log.append(maintenance)
        print(f"Entretien ajouté au véhicule #{self.id}")

    @abstractmethod
    def show_details(self):
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "daily_rate": self.daily_rate,
            "status": self.status.value,
        }

class MotorizedVehicle(TransportMode):
    def __init__(self, t_id, daily_rate, brand, model, license_plate):
        super().__init__(t_id, daily_rate)
        self.brand = brand
        self.model = model
        self.license_plate = license_plate

    def start_engine(self):
        if self.status == VehicleStatus.AVAILABLE:
            print(f"Le moteur de la {self.brand} démarre.")
        else :
            print(f"Impossible : Véhicule {self.status.value}")

    def refuel(self):
        print("Le plein est fait.")

class TransportAnimal(TransportMode):
    def __init__(self, t_id, daily_rate, name, breed, birth_date):
        super().__init__(t_id, daily_rate)
        self.name = name
        self.breed = breed
        self.birth_date = birth_date

    def feed(self):
        print(f"{self.name} a été nourri.")

    def heal(self):
        self.status = VehicleStatus.UNDER_MAINTENANCE
        print(f"{self.name} reçoit des soins.")