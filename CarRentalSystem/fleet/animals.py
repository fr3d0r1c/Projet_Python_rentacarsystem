from .transport_base import TransportAnimal

# --- TERRE ---
class Horse(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, wither_height, shoe_size_front, shoe_size_rear):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.wither_height = wither_height
        self.shoe_size_front = shoe_size_front; self.shoe_size_rear = shoe_size_rear
    @property
    def category(self): return "Poney" if self.wither_height < 140 else "Cheval"
    
    def show_details(self): 
        return f"[{self.category}] {self.name} ({self.age} ans) - {self.wither_height}cm, Fers: {self.shoe_size_front}/{self.shoe_size_rear}mm"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "wither_height": self.wither_height, "shoe_size_front": self.shoe_size_front, "shoe_size_rear": self.shoe_size_rear}); return d

class Donkey(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, pack_capacity_kg, is_stubborn):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.pack_capacity_kg = pack_capacity_kg; self.is_stubborn = is_stubborn
    
    def show_details(self): 
        caractere = "Têtu" if self.is_stubborn else "Docile"
        return f"[Âne] {self.name} ({self.age} ans) - Charge {self.pack_capacity_kg}kg, {caractere}"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "pack_capacity_kg": self.pack_capacity_kg, "is_stubborn": self.is_stubborn}); return d

class Camel(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, hump_count, water_reserve):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.hump_count = hump_count; self.water_reserve = water_reserve
    
    def show_details(self): 
        return f"[Chameau] {self.name} ({self.age} ans) - {self.hump_count} bosses, {self.water_reserve}L eau"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "hump_count": self.hump_count, "water_reserve": self.water_reserve}); return d

# --- MER ---
class Whale(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, weight_tonnes, can_sing):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.weight_tonnes = weight_tonnes; self.can_sing = can_sing
    
    def show_details(self): 
        chant = "Chanteuse" if self.can_sing else "Silencieuse"
        return f"[Baleine] {self.name} ({self.age} ans) - {self.weight_tonnes}T, {chant}"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "weight_tonnes": self.weight_tonnes, "can_sing": self.can_sing}); return d

class Dolphin(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, swim_speed, knows_tricks):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.swim_speed = swim_speed; self.knows_tricks = knows_tricks
    
    def show_details(self): 
        trick = "Savant" if self.knows_tricks else "Sauvage"
        return f"[Dauphin] {self.name} ({self.age} ans) - {self.swim_speed}km/h, {trick}"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "swim_speed": self.swim_speed, "knows_tricks": self.knows_tricks}); return d

# --- AIR ---
class Eagle(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, wingspan_cm, max_altitude):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.wingspan_cm = wingspan_cm; self.max_altitude = max_altitude
    
    def show_details(self): 
        return f"[Aigle] {self.name} ({self.age} ans) - Env. {self.wingspan_cm}cm, Alt. {self.max_altitude}m"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "wingspan_cm": self.wingspan_cm, "max_altitude": self.max_altitude}); return d

class Dragon(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, fire_range, scale_color):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age; self.fire_range = fire_range; self.scale_color = scale_color
    
    def show_details(self): 
        return f"[Dragon] {self.name} ({self.age} ans) - {self.scale_color}, Feu {self.fire_range}m"
    
    def to_dict(self): d=super().to_dict(); d.update({"age": self.age, "fire_range": self.fire_range, "scale_color": self.scale_color}); return d