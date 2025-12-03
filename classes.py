from datetime import datetime

# --- MOCKS (A supprimer) ---
class VehicleMock:
    def __init__(self, brand, model, daily_rate):
        self.brand = brand
        self.model = model
        self.daily_rate = daily_rate
        self.is_available = True

    def set_availability(self, status):
        self.is_available = status

class CustomerMock:
    def __init__(self, name):
        self.name = name

# --- RENTAL ---
class Rental:
    def __init__(self, customer, vehicle, start_date_str, end_date_str):
        self.customer = customer
        self.vehicle = vehicle
        self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        self.actual_return_date = None
        self.total_cost = 0.0
        self.penalty = 0.0
        self.is_active = False
        self._validate_rental()

    def _validate_rental(self):
        # ... (le reste du code de la méthode) ...
        pass 

    # ... (Copie ici toutes les autres méthodes : confirm_rental, return_vehicle, etc.)
