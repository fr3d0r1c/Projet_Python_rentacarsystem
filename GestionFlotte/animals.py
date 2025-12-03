from datetime import date
from typing import Optional
from transport_base import TransportAnimal

class Horse(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, birth_date, wither_height, shoe_size):
        super().__init__(t_id, daily_rate, name, breed, birth_date)
        self.wither_height = wither_height
        self.shoe_size = shoe_size
        self.last_hoof_care: Optional[date] = None

    def check_hooves(self):
        self.last_hoof_care = date.today()
        print(f"Sabots de {self.name} vérifiés.")

    def show_details(self):
        return f"[Poney] {self.name} ({self.breed})"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "wither_height": self.wither_height,
            "shoe_size": self.shoe_size
        })
    
class Camel(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, birth_date, hump_count, water_reserve):
        super().__init__(t_id, daily_rate, name, breed, birth_date)
        self.hump_count = hump_count
        self.water_reserve = water_reserve

    def show_details(self):
        type_animal = "Dromadaire" if self.hump_count == 1 else "Chameau"
        return f"[{type_animal}] {self.name} - Bosses: {self.hump_count} - Eau: {self.water_reserve}L"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "hump_count": self.hump_count,
            "water_reserve": self.water_reserve
        })
        return data
    
class Donkey(TransportAnimal):
    def __init__(self, t_id, daily_rate, name, breed, birth_date, pack_capacity_kg, is_stubborn):
        super().__init__(t_id, daily_rate, name, breed, birth_date)
        self.pack_capacity_kg = pack_capacity_kg
        self.is_stubborn = is_stubborn

    def show_details(self):
        caractere = "Têtu" if self.is_stubborn else "Docile"
        return f"[Âne] {self.name} - Capacité: {self.pack_capacity_kg}kg - Caractère: {caractere}"
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "pack_capacity_kg": self.pack_capacity_kg,
            "is_stubborn": self.is_stubborn
        })
        return data