from datetime import date
from transport_base import TransportAnimal

class Horse(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, age, wither_height, shoe_size_front, shoe_size_rear):
        super().__init__(t_id, daily_rate, name, breed, None)
        self.age = age
        self.wither_height = wither_height
        self.shoe_size_front = shoe_size_front
        self.shoe_size_rear = shoe_size_rear

    @property
    def category(self):
        if self.wither_height < 140:
            return "Poney"
        else:
            return "Cheval"
        
    def show_details(self):
        return (f"[{self.category}] {self.name} ({self.age} ans) - "
                f"Taille: {self.wither_height}cm - "
                f"Fers: Av.{self.shoe_size_front}mm / Arr.{self.shoe_size_rear}mm")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "age": self.age,
            "wither_height": self.wither_height,
            "shoe_size_front": self.shoe_size_front,
            "shoe_size_rear": self.shoe_size_rear
        })
        return data

class Donkey(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, birth_date, pack_capacity_kg, is_stubborn):
        super().__init__(t_id, daily_rate, name, breed, birth_date)
        self.pack_capacity_kg = pack_capacity_kg
        self.is_stubborn = is_stubborn

    def show_details(self):
        caractere = "Têtu" if self.is_stubborn else "Docile"
        return f"[Âne] {self.name} ({caractere})"

    def to_dict(self):
        data = super().to_dict()
        data.update({"pack_capacity_kg": self.pack_capacity_kg, "is_stubborn": self.is_stubborn})
        return data

class Camel(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, birth_date, hump_count, water_reserve):
        super().__init__(t_id, daily_rate, name, breed, birth_date)
        self.hump_count = hump_count
        self.water_reserve = water_reserve

    def show_details(self):
        return f"[Chameau] {self.name} ({self.hump_count} bosses)"

    def to_dict(self):
        data = super().to_dict()
        data.update({"hump_count": self.hump_count, "water_reserve": self.water_reserve})
        return data