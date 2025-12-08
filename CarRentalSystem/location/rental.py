from datetime import date, timedelta, datetime
from GestionFlotte.transport_base import TransportMode, MotorizedVehicle, TransportAnimal
from clients.customer import Customer

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
        # reste du code
        pass 