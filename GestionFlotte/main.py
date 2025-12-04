from storage import StorageManager
import console_ui as ui 

def main():
    storage = StorageManager("ma_flotte.json")
    my_fleet = storage.load_fleet()
    
    while True:
        ui.show_main_menu()
        choix = input("\nVotre choix : ")

        if choix == '1': ui.list_fleet(my_fleet)
        elif choix == '2': ui.add_main_menu(my_fleet)
        elif choix == '3': ui.maintenance_menu(my_fleet)
        elif choix == '4': ui.harness_menu(my_fleet)
        elif choix == '5': ui.delete_menu(my_fleet)
        elif choix == '6':
            storage.save_fleet(my_fleet)
            print("👋 Au revoir !")
            break
        else: print("❌ ?")

if __name__ == "__main__":
    main()