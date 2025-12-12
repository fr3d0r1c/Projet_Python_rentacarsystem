from .transport_base import MotorizedVehicle, TowedVehicle
from .animals import Horse, Donkey

# --- TERRE ---
class Car(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, door_count, has_ac):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.door_count = door_count; self.has_ac = has_ac
    
    def show_details(self): 
        clim = "Clim" if self.has_ac else "Pas de clim"
        return f"[Voiture {self.year}] {self.brand} {self.model} - {self.door_count} portes, {clim}"
    
    def to_dict(self): d=super().to_dict(); d.update({"door_count": self.door_count, "has_ac": self.has_ac}); return d

class Truck(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, cargo_volume, max_weight):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.cargo_volume = cargo_volume; self.max_weight = max_weight
    
    def show_details(self): 
        return f"[Camion {self.year}] {self.brand} {self.model} - {self.cargo_volume}m³, {self.max_weight}T"
    
    def to_dict(self): d=super().to_dict(); d.update({"cargo_volume": self.cargo_volume, "max_weight": self.max_weight}); return d

class Motorcycle(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, engine_displacement, has_top_case):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.engine_displacement = engine_displacement; self.has_top_case = has_top_case
    
    def show_details(self): 
        top = "Avec TopCase" if self.has_top_case else "Sans TopCase"
        return f"[Moto {self.year}] {self.brand} {self.model} - {self.engine_displacement}cc, {top}"
    
    def to_dict(self): d=super().to_dict(); d.update({"engine_displacement": self.engine_displacement, "has_top_case": self.has_top_case}); return d

class Hearse(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, max_coffin_length, has_refrigeration):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.max_coffin_length = max_coffin_length; self.has_refrigeration = has_refrigeration
    
    def show_details(self): 
        frigo = "Réfrigéré" if self.has_refrigeration else "Non réfrigéré"
        return f"[Corbillard {self.year}] {self.brand} {self.model} - Cercueil max {self.max_coffin_length}m, {frigo}"
    
    def to_dict(self): d=super().to_dict(); d.update({"max_coffin_length": self.max_coffin_length, "has_refrigeration": self.has_refrigeration}); return d

class GoKart(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, engine_type, is_indoor):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.engine_type = engine_type; self.is_indoor = is_indoor
    
    def show_details(self): 
        loc = "Indoor" if self.is_indoor else "Outdoor"
        return f"[Kart {self.year}] {self.brand} {self.model} - {self.engine_type}, {loc}"
    
    def to_dict(self): d=super().to_dict(); d.update({"engine_type": self.engine_type, "is_indoor": self.is_indoor}); return d

# --- MER ---
class Boat(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, length_meters, power_cv):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.length_meters = length_meters; self.power_cv = power_cv
    
    def show_details(self): 
        return f"[Bateau {self.year}] {self.brand} {self.model} - {self.length_meters}m, {self.power_cv}cv"
    
    def to_dict(self): d=super().to_dict(); d.update({"length_meters": self.length_meters, "power_cv": self.power_cv}); return d

class Submarine(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, max_depth, is_nuclear):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.max_depth = max_depth; self.is_nuclear = is_nuclear
    
    def show_details(self): 
        moteur = "Nucléaire" if self.is_nuclear else "Diesel/Élec"
        return f"[Sous-Marin {self.year}] {self.brand} {self.model} - Prof. -{self.max_depth}m, {moteur}"
    
    def to_dict(self): d=super().to_dict(); d.update({"max_depth": self.max_depth, "is_nuclear": self.is_nuclear}); return d

# --- AIR ---
class Plane(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, wingspan, engines_count):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.wingspan = wingspan; self.engines_count = engines_count
    
    def show_details(self): 
        return f"[Avion {self.year}] {self.brand} {self.model} - Env. {self.wingspan}m, {self.engines_count} moteurs"
    
    def to_dict(self): d=super().to_dict(); d.update({"wingspan": self.wingspan, "engines_count": self.engines_count}); return d

class Helicopter(MotorizedVehicle):
    def __init__(self, t_id, daily_rate, brand, model, license_plate, year, rotor_count, max_altitude):
        super().__init__(t_id, daily_rate, brand, model, license_plate, year)
        self.rotor_count = rotor_count; self.max_altitude = max_altitude
    
    def show_details(self): 
        return f"[Hélico {self.year}] {self.brand} {self.model} - {self.rotor_count} pales, Alt. max {self.max_altitude}m"
    
    def to_dict(self): d=super().to_dict(); d.update({"rotor_count": self.rotor_count, "max_altitude": self.max_altitude}); return d

# --- ATTELAGES ---
class Carriage(TowedVehicle):
    def __init__(self, t_id, daily_rate, seat_count, has_roof):
        super().__init__(t_id, daily_rate, seat_count)
        self.has_roof = has_roof
    def harness_animal(self, animal):
        if isinstance(animal, Horse) and animal.wither_height >= 140: super().harness_animal(animal)
        else: print("❌ Seul un Cheval (>140cm) peut tirer une Calèche.")
    def show_details(self):
        toit = "Avec toit" if self.has_roof else "Décapotable"
        att = f" avec {len(self.animals)} chevaux" if self.animals else " (vide)"
        return f"[Calèche] {self.seat_count} places, {toit} {att}"
    def to_dict(self): d=super().to_dict(); d.update({"has_roof": self.has_roof}); return d

class Cart(TowedVehicle):
    def __init__(self, t_id, daily_rate, seat_count, max_load_kg):
        super().__init__(t_id, daily_rate, seat_count)
        self.max_load_kg = max_load_kg
    def harness_animal(self, animal):
        if isinstance(animal, Donkey): super().harness_animal(animal)
        else: print("❌ Seul un Âne peut tirer une Charrette.")
    def show_details(self):
        att = f" avec {len(self.animals)} ânes" if self.animals else " (vide)"
        return f"[Charrette] {self.max_load_kg}kg max {att}"
    def to_dict(self): d=super().to_dict(); d.update({"max_load_kg": self.max_load_kg}); return d