from typing import List
# On importe les classes parentes
from transport_base import TransportMode, MotorizedVehicle, TransportAnimal

# --- 1. VOITURE ---
class Car(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, door_count, has_ac):
        # On passe l'année (year) au parent MotorizedVehicle
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.door_count = door_count
        self.has_ac = has_ac

    def show_details(self):
        clim = "Clim" if self.has_ac else "Pas de clim"
        return f"[Voiture {self.year}] {self.brand} {self.model} ({clim})"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "door_count": self.door_count, 
            "has_ac": self.has_ac
        })
        return data

# --- 2. CAMION ---
class Truck(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, cargo_volume, max_weight):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.cargo_volume = cargo_volume
        self.max_weight = max_weight

    def show_details(self):
        return f"[Camion {self.year}] {self.brand} {self.model} ({self.max_weight}T)"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "cargo_volume": self.cargo_volume, 
            "max_weight": self.max_weight
        })
        return data

# --- 3. MOTO ---
class Motorcycle(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, engine_displacement, has_top_case):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.engine_displacement = engine_displacement
        self.has_top_case = has_top_case

    def show_details(self):
        top_case = "Avec TopCase" if self.has_top_case else "Sans TopCase"
        return f"[Moto {self.year}] {self.brand} ({self.engine_displacement}cc) - {top_case}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "engine_displacement": self.engine_displacement, 
            "has_top_case": self.has_top_case
        })
        return data

# --- 4. CORBILLARD ---
class Hearse(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, max_coffin_length, has_refrigeration):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.max_coffin_length = max_coffin_length
        self.has_refrigeration = has_refrigeration

    def show_details(self):
        frigo = "Réfrigéré" if self.has_refrigeration else "Non réfrigéré"
        return f"[Corbillard {self.year}] {self.brand} - {frigo}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "max_coffin_length": self.max_coffin_length, 
            "has_refrigeration": self.has_refrigeration
        })
        return data

# --- 5. KART ---
class GoKart(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, engine_type, is_indoor):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.engine_type = engine_type
        self.is_indoor = is_indoor

    def show_details(self):
        usage = "Indoor" if self.is_indoor else "Outdoor"
        return f"[Kart {self.year}] {self.brand} ({self.engine_type}) - {usage}"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "engine_type": self.engine_type, 
            "is_indoor": self.is_indoor
        })
        return data

# --- 6. CALÈCHE (Non motorisée) ---
class Carriage(TransportMode):
    def __init__(self, t_id, daily_rate, seat_count, has_roof):
        super().__init__(t_id, daily_rate)
        self.seat_count = seat_count
        self.has_roof = has_roof
        self.animals: List[TransportAnimal] = []

    def harness_animal(self, animal: TransportAnimal):
        self.animals.append(animal)

    def show_details(self):
        toit = "Avec toit" if self.has_roof else "Décapotable"
        attelage = ", ".join([a.name for a in self.animals]) if self.animals else "Personne"
        return f"[Calèche] {self.seat_count} places ({toit}) - Tirée par: {attelage}"

    def to_dict(self):
        data = super().to_dict()
        # On sauvegarde aussi la liste des animaux attelés (version simplifiée)
        animals_data = [a.to_dict() for a in self.animals]
        data.update({
            "seat_count": self.seat_count, 
            "has_roof": self.has_roof,
            "animals": animals_data
        })
        return data