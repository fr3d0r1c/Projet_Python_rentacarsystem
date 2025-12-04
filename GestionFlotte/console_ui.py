from datetime import date
from vehicles import *
from animals import *
from maintenance import Maintenance
from enums import MaintenanceType, VehicleStatus
from transport_base import MotorizedVehicle, TransportAnimal, TowedVehicle

# PRIX
DEFAULT_RENTAL_PRICES = {
    '1':50.0, '2':35.0, '3':250.0, '4':90.0, '5':300.0, '6':60.0, 
    '7':120.0, '8':25.0, '9':80.0, '10':40.0,'11':400.0, '12':1500.0, 
    '13':200.0, '14':150.0, '15':800.0, '16':2000.0, '17':5000.0, '18':100.0
}
# HELPERS
def ask_int(m):
    while True: 
        try: return int(input(m))
        except: print("❌ Entier svp")

def ask_float(m): 
    while True: 
        try: return float(input(m))
        except: print("❌ Float svp")

def ask_float_def(m,d):
    v=input(f"{m} (Entrée={d}): "); 
    return float(v) if v.strip() else d
def ask_bool(m): 
    return input(f"{m} (o/n): ").lower().startswith('o')

# MENUS
def show_main_menu():
    print("\n--- Gestion de Flote ---")
    print("1.📋 Voir 2.➕ Ajouter 3.🔧 Entretien 4.🐴 Atteler 5.🗑️ Supprimer 6.💾 Fin")

def list_fleet(fleet):
    if not fleet: print("Vide.")
    else:
        for v in fleet: print(f"[{v.id}] {v.show_details()} | {v.status.value}")

def add_main_menu(fleet):
    print("\n1.⛰️ Terre 2.🌊 Mer 3.☁️ Air"); c=input("Env: ")
    nid = 1 if not fleet else max(v.id for v in fleet)+1
    
    if c=='1':
        print("1.Voiture 2.Camion 3.Moto 4.Corbillard 5.Kart 6.Cheval 7.Âne 8.Chameau 9.Calèche 10.Charrette")
        t=input("Type: ")
        rate=ask_float_def("Tarif", DEFAULT_RENTAL_PRICES.get(t,50.0))
        if t=='1': fleet.append(Car(nid,rate,input("Marque: "),input("Modèle: "),input("Plaque: "),ask_int("Année: "),5,True))
        elif t=='6': fleet.append(Horse(nid,rate,input("Nom: "),"Std",5,160,100,100))
        elif t=='7': fleet.append(Donkey(nid,rate,input("Nom: "),"Std",5,50,True))
        elif t=='9': fleet.append(Carriage(nid,rate,4,True))
        elif t=='10': fleet.append(Cart(nid,rate,1,200))
        # (Ajoutez les autres types terrestres si besoin, j'ai abrégé pour la lisibilité)
    elif c=='2':
        print("1.Bateau 2.Sous-Marin 3.Baleine 4.Dauphin"); t=input("Type: ")
        rate=ask_float_def("Tarif", 200.0)
        if t=='1': fleet.append(Boat(nid,rate,input("Marque: "),"Mod","BAT",2020,10,200))
        elif t=='2': fleet.append(Submarine(nid,rate,"Nautilus","Nuc","SUB",2020,500,True))
        elif t=='3': fleet.append(Whale(nid,rate,input("Nom: "),"Bleue",10,100,True))
        elif t=='4': fleet.append(Dolphin(nid,rate,input("Nom: "),"Flipper",5,40,True))
    elif c=='3':
        print("1.Avion 2.Hélico 3.Aigle 4.Dragon"); t=input("Type: ")
        rate=ask_float_def("Tarif", 500.0)
        if t=='1': fleet.append(Plane(nid,rate,"Boeing","747","AIR",2010,60,4))
        elif t=='2': fleet.append(Helicopter(nid,rate,"Airbus","H160","HEL",2022,5,3000))
        elif t=='3': fleet.append(Eagle(nid,rate,input("Nom: "),"Royal",5,200,2000))
        elif t=='4': fleet.append(Dragon(nid,rate,input("Nom: "),"Rouge",200,50,"Rouge"))
    print("✅ Fait.")

def maintenance_menu(fleet):
    tid=ask_int("ID: "); obj=next((v for v in fleet if v.id==tid),None)
    if not obj: return
    print("1.Méca 2.Nettoyage 3.Sabots"); c=input("Type: ")
    typ = MaintenanceType.MECHANICAL_CHECK if c=='1' else MaintenanceType.HOOF_CARE if c=='3' else MaintenanceType.CLEANING
    obj.add_maintenance(Maintenance(len(obj.maintenance_log)+1,date.today(),typ,50.0,"Entretien",1.0))
    if ask_bool("Indispo?"): obj.status=VehicleStatus.UNDER_MAINTENANCE
    print("✅ Fait.")

def harness_menu(fleet):
    vid=ask_int("ID Charrette/Calèche: "); v=next((x for x in fleet if x.id==vid),None)
    if not isinstance(v, TowedVehicle): return print("❌ Erreur Véhicule")
    aid=ask_int("ID Animal: "); a=next((x for x in fleet if x.id==aid),None)
    v.harness_animal(a)

def delete_menu(fleet):
    tid=ask_int("ID: "); f=next((v for v in fleet if v.id==tid),None)
    if f: fleet.remove(f); print("🗑️ Fait.")