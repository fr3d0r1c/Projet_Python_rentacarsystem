import unittest
from datetime import date

from single_file_delivery import (
    CarRentalSystem, Customer, Rental, Car, Dragon, 
    VehicleStatus, MaintenanceType
)

class TestCarRental(unittest.TestCase):

    def setUp(self):
        self.system = CarRentalSystem()

        self.client = Customer(1, "Toto", "B-123", "toto@mail.com", "0600", "toto", "pass")
        self.voiture = Car(1, 50.0, "Peugeot", "208", "AA-123-BB", 2020, 5, True)
        self.dragon = Dragon(2, 500.0, "Smaug", "Rouge", 150, 100.0, "Doré")

        self.system.add_customer(self.client)
        self.system.add_vehicle(self.voiture)
        self.system.add_vehicle(self.dragon)

    def test_creation_client(self):
        self.assertEqual(self.client.name, "Toto")
        self.assertEqual(self.client.driver_license, "B-123")

    def test_creation_vehicule(self):
        self.assertEqual(self.voiture.brand, "Peugeot")
        self.assertTrue(self.voiture.has_ac)
        self.assertEqual(self.dragon.scale_color, "Doré")

    def test_calcul_prix_simple(self):
        rental = Rental(self.client, self.voiture, "2024-01-01", "2024-01-06")
        cout = rental.calculate_cost()
        self.assertEqual(cout, 250.0)

    def test_validation_date_invalide(self):
        with self.assertRaises(ValueError):
            Rental(self.client, self.voiture, "2024-01-10", "2024-01-01")

    def test_disponibilite_vehicule(self):
        rental = Rental(self.client, self.voiture, "2024-01-01", "2024-01-05")

        self.assertFalse(self.voiture.status == VehicleStatus.AVAILABLE)

        with self.assertRaises(ValueError):
            Rental(self.client, self.voiture, "2024-01-02", "2024-01-03")

    def test_retour_normal(self):
        rental = Rental(self.client, self.voiture, "2024-01-01", "2024-01-03") # 2 jours prévus
        prix_final = rental.close_rental("2024-01-03")

        self.assertEqual(prix_final, 100.0)
        self.assertEqual(rental.penalty, 0.0)

        self.assertEqual(self.voiture.status, VehicleStatus.AVAILABLE)

    def test_retour_retard(self):
        rental = Rental(self.client, self.voiture, "2024-01-01", "2024-01-03")

        prix_final = rental.close_rental("2024-01-05")

        self.assertEqual(rental.penalty, 10.0)
        self.assertEqual(prix_final, 210.0)

if __name__ == '__main__':
    print("🚗 Démarrage des tests unitaires Rent-A-Dream...")
    unittest.main()