from datetime import date
from enums import MaintenanceType

class Maintenance:
    def __init__(self, m_id: int, date_m: date, m_type: MaintenanceType, cost: float, description: str):
        self.id = m_id
        self.date = date_m
        self.type = m_type # Doit être une valeur de l'Enum MaintenanceType
        self.cost = cost
        self.description = description

    def validate(self):
        """Affiche une confirmation visuelle de l'entretien."""
        print(f"✅ Maintenance #{self.id} ({self.type.value}) validée le {self.date} pour {self.cost}€.")

    def to_dict(self):
        """Transforme l'objet en dictionnaire pour la sauvegarde JSON."""
        return {
            "id": self.id,
            "date": str(self.date), # On convertit la date en texte (YYYY-MM-DD)
            "type": self.type.value, # On garde le texte de l'enum (ex: "Vidange")
            "cost": self.cost,
            "description": self.description
        }

    def __str__(self):
        """Permet un affichage propre si on fait print(maintenance)"""
        return f"[{self.date}] {self.type.value} - {self.description} ({self.cost}€)"