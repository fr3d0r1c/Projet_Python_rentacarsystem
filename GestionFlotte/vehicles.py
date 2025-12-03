from typing import List
from transport_base import TransportMode, MotorizedVehicle, TransportAnimal

class Car(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, door_count, has_ac):
        super().__init__(t_id, daily_rate, brand, model, license_plate)
        self.door_count = door_count
        self.has_ac = has_ac

    def show_details(self):
        clim = "Avec Clim" if self.has_ac else "Sans Clim"
        return f"[Voiture] {self.brand} {self.model} ({clim})"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "brand": self.brand,
            "model": self.model,
            "license_plate": self.license_plate,
            "door_count": self.door_count,
            "has_ac": self.has_ac
        })
        return data
    
class Carriage(TransportMode):
    def __init__(self, t_id, daily_rate, seat_count, has_roof):
        super().__init__(t_id, daily_rate)
        self.seat_count = seat_count
        self.has_roof = has_roof
        self.animals: List[TransportAnimal] = []

    def harness_animal(self, animal: TransportAnimal):
        if isinstance(animal, TransportAnimal):
            self.animals.append(animal)
            print(f"{animal.name} attelé à la calèche.")
        else:
            print("Erreur : Ce n'est pas un animal.")

    def show_details(self):
        attelage = ", ".join([a.name for a in self.animals]) if self.animals else "Personne"
        return f"[Calèche] Places: {self.seat_count} - Tirée par: {attelage}"
    
    def to_dict(self):
        data = super().to_dict()
        animals_data = [animal.to_dict() for animal in self.animals]

        data.update({
            "seat_count": self.seat_count,
            "has_roof": self.has_roof,
            "animals": animals_data # Sauvegarde les animaux liés
        })
    
class Truck(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, cargo_volume, max_weight):
        super().__init__(t_id, daily_rate, brand, model, license_plate)
        self.cargo_volume = cargo_volume
        self.max_weight = max_weight

    def show_details(self):
        return (f"[Camion] {self.brand} {self.model} - "
                f"Volume: {self.cargo_volume}m3 - Charge Max: {self.max_weight}T")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "cargo_volume": self.cargo_volume,
            "max_weight": self.max_weight
        })
        return data

class Motorcycle(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, engine_displacement, has_top_case):
        super().__init__(t_id, daily_rate, brand, model, license_plate)
        self.engine_displacement = engine_displacement
        self.has_top_case = has_top_case

    def show_details(self):
        top_case = "Avec TopCase" if self.has_top_case else "Sans TopCase"
        return (f"[Moto] {self.brand} {self.model} ({self.engine_displacement}cc) - {top_case}")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "engine_displacement": self.engine_displacement,
            "has_top_case": self.has_top_case
        })
        return data

class Hearse(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, max_coffin_length, has_refrigeration):
        super().__init__(t_id, daily_rate, brand, model, license_plate)
        self.max_coffin_length = max_coffin_length
        self.has_refrigeration = has_refrigeration

    def show_details(self):
        frigo = "Réfrigéré" if self.has_refrigeration else "Non réfrigéré"
        return (f"[Corbillard] {self.brand} {self.model} - "
                f"Long. Cercueil Max: {self.max_coffin_length}m - {frigo}")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "max_coffin_length": self.max_coffin_length,
            "has_refrigeration": self.has_refrigeration
        })
        return data

class GoKart(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, engine_type, is_indoor):
        super().__init__(t_id, daily_rate, brand, model, license_plate)
        self.engine_type = engine_type  # Ex: "2 temps", "Electrique"
        self.is_indoor = is_indoor

    def show_details(self):
        usage = "Indoor" if self.is_indoor else "Outdoor"
        return (f"[Kart] {self.brand} {self.model} - "
                f"Moteur: {self.engine_type} - Type: {usage}")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "engine_type": self.engine_type,
            "is_indoor": self.is_indoor
        })
        return data