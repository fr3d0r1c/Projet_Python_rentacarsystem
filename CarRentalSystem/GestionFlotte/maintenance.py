from datetime import date, timedelta
from .enums import MaintenanceType

class Maintenance:
    def __init__(self, m_id: int, date_m: date, m_type: MaintenanceType, cost: float, description: str, duration: float):
        self.id = m_id
        self.date = date_m
        self.type = m_type
        self.cost = cost
        self.description = description
        self.duration = duration # Durée en jours

    @property
    def end_date(self):
        days_int = int(self.duration) if self.duration >= 1 else 1
        return self.date + timedelta(days=days_int)

    def validate(self):
        print(f"✅ Maintenance #{self.id} ({self.type.value}) - Durée : {self.duration}j")

    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date),
            "type": self.type.value,
            "cost": self.cost,
            "description": self.description,
            "duration": self.duration
        }