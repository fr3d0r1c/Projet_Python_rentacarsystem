from abc import ABC, abstractmethod
from typing import List
from .enums import VehicleStatus
from .maintenance import Maintenance

class TransportMode(ABC):
    def __init__(self, t_id: int, daily_rate: float):
        self.id = t_id
        self.daily_rate = daily_rate
        self.status = VehicleStatus.AVAILABLE
        self.maintenance_log: List[Maintenance] = []

    @property
    def is_available(self):
        return self.status == VehicleStatus.AVAILABLE

    def add_maintenance(self, maintenance: Maintenance):
        self.maintenance_log.append(maintenance)

    def to_dict(self):
        m_logs = [m.to_dict() for m in self.maintenance_log]
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "daily_rate": self.daily_rate,
            "status": self.status.value,
            "maintenance_log": m_logs
        }

    @abstractmethod
    def show_details(self):
        pass

class MotorizedVehicle(TransportMode):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year):
        super().__init__(t_id, daily_rate)
        self.brand = brand
        self.model = model
        self.license_plate = license_plate
        self.year = year

    def to_dict(self):
        data = super().to_dict()
        data.update({"brand": self.brand, "model": self.model, "license_plate": self.license_plate, "year": self.year})
        return data

class TransportAnimal(TransportMode):
    def __init__(self, t_id, daily_rate, name, breed, birth_date):
        super().__init__(t_id, daily_rate)
        self.name = name
        self.breed = breed
        self.birth_date = birth_date # Gardé pour compatibilité, mais on utilise 'age' dans les enfants

    def to_dict(self):
        data = super().to_dict()
        data.update({"name": self.name, "breed": self.breed})
        return data

class TowedVehicle(TransportMode):
    def __init__(self, t_id, daily_rate, seat_count):
        super().__init__(t_id, daily_rate)
        self.seat_count = seat_count
        self.animals = [] 

    def harness_animal(self, animal):
        self.animals.append(animal)
        print(f"✅ {animal.name} a été attelé.")

    def to_dict(self):
        data = super().to_dict()
        # On sauvegarde les IDs pour reconstruire le lien plus tard
        data.update({
            "seat_count": self.seat_count,
            "animal_ids": [a.id for a in self.animals]
        })
        return data