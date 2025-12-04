from abc import ABC, abstractmethod
from typing import List
from enums import VehicleStatus
from maintenance import Maintenance

# --- MÈRE SUPRÊME ---
class TransportMode(ABC):
    def __init__(self, t_id: int, daily_rate: float):
        self.id = t_id
        self.daily_rate = daily_rate
        self.status = VehicleStatus.AVAILABLE
        self.maintenance_log: List[Maintenance] = []

    def add_maintenance(self, maintenance: Maintenance):
        self.maintenance_log.append(maintenance)

    def to_dict(self):
        """Sauvegarde les infos de base (ID, Tarif, Status)"""

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

# --- BRANCHE MOTEUR ---
class MotorizedVehicle(TransportMode):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year):
        super().__init__(t_id, daily_rate)
        self.brand = brand
        self.model = model
        self.license_plate = license_plate
        self.year = year

    def start_engine(self):
        print(f"Moteur de {self.brand} démarré.")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "brand": self.brand,
            "model": self.model,
            "license_plate": self.license_plate,
            "year": self.year
        })
        return data

# --- BRANCHE ANIMAL ---
class TransportAnimal(TransportMode):
    def __init__(self, t_id, daily_rate, name, breed, birth_date):
        super().__init__(t_id, daily_rate)
        self.name = name
        self.breed = breed
        self.birth_date = birth_date

    # 👇 C'EST SOUVENT ICI QUE ÇA MANQUE ! 👇
    def to_dict(self):
        data = super().to_dict()
        # On ajoute le Nom et la Race au dictionnaire
        data.update({
            "name": self.name,
            "breed": self.breed
        })
        return data