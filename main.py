#!/usr/bin/python3

# --------------------------------------------------
# Main file & importations
# --------------------------------------------------

from classes import Rental, VehicleMock, CustomerMock 

def main():
    try:
        print("--- Démarrage du système ---")
        
        # Création des objets
        client = CustomerMock("Thomas Anderson")
        voiture = VehicleMock("Tesla", "Model S", 100)

        # Utilisation de ta classe Rental
        location = Rental(client, voiture, "2024-05-01", "2024-05-05")
        location.confirm_rental()

        # Retour
        location.return_vehicle("2024-05-06") # Un jour de retard
        
        # Facture
        print(location.generate_invoice())

    except Exception as e:
        print(f"Erreur : {e}")

# Cette ligne dit : "Si on lance ce fichier directement, exécute la fonction main()"
if __name__ == "__main__":
    main()
