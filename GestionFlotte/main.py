from storage import StorageManager
import console_ui as ui 

def main():
    storage = StorageManager("ma_flotte.json")
    my_fleet = storage.load_fleet()
    
    while True:
        ui.show_main_menu()
        choix = input("\nVotre choix : ")

        if choix == '1':
            ui.list_fleet(my_fleet)
        
        elif choix == '2':
            ui.add_motor_menu(my_fleet)  # Nouveau menu Voitures
            
        elif choix == '3':
            ui.add_animal_menu(my_fleet) # Nouveau menu Animaux

        elif choix == '4':
            ui.add_towed_menu(my_fleet)  # Nouveau menu Attelages

        elif choix == '5':
            # Maintenance Mécanique
            ui.maintenance_process(my_fleet, 'motor')
            
        elif choix == '6':
            # Maintenance Vétérinaire
            ui.maintenance_process(my_fleet, 'animal')

        elif choix == '7':
            ui.harness_animal_menu(my_fleet)

        elif choix == '8':
            ui.delete_vehicle_menu(my_fleet)

        elif choix == '9':
            storage.save_fleet(my_fleet)
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Commande inconnue.")

if __name__ == "__main__":
    main()