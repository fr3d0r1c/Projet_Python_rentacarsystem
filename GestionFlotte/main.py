from storage import StorageManager
import console_ui as ui 

def main():
    storage = StorageManager("ma_flotte.json")
    
    print("Chargement de la base de données...")
    my_fleet = storage.load_fleet()
    
    while True:
        ui.show_main_menu()
        choix = input("\nVotre choix : ")

        if choix == '1':
            ui.list_fleet(my_fleet)

        elif choix == '2':
            ui.add_vehicle_menu(my_fleet)

        elif choix == '3':
            ui.modify_vehicle_menu(my_fleet)

        elif choix == '4':
            ui.add_maintenance_menu(my_fleet)

        elif choix == '5':
            ui.delete_vehicle_menu(my_fleet)

        elif choix == '6':
            storage.save_fleet(my_fleet)
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Commande inconnue.")

if __name__ == "__main__":
    main()