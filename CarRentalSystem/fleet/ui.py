import os
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, IntPrompt, Confirm
from rich import print as rprint
from rich.columns import Columns
from rich.box import ROUNDED

# Imports de vos classes
from datetime import date
# 👇 MODIFICATION DES IMPORTS
from CarRentalSystem import fleet, storage
from fleet.vehicles import Car, Truck, Motorcycle, Hearse, GoKart, Carriage, Cart, Boat, Plane, Helicopter, Submarine, MotorizedVehicle, TowedVehicle
from fleet.animals import Horse, Donkey, Camel, Whale, Eagle, Dragon, Dolphin, TransportAnimal
from fleet.maintenance import Maintenance
from fleet.enums import MaintenanceType, VehicleStatus
from location import system

# Initialisation de la console Rich
console = Console()

# --- 💰 CONFIGURATION (Inchangée) ---
DEFAULT_RENTAL_PRICES = {
    '1': 50.0, '2': 250.0, '3': 90.0, '4': 300.0, '5': 60.0,
    '6': 35.0, '7': 25.0, '8': 80.0, '9': 120.0, '10': 40.0,
    '11': 400.0, '12': 1500.0, '13': 200.0, '14': 150.0,
    '15': 800.0, '16': 2000.0, '17': 5000.0, '18': 10000.0
}

DEFAULT_MAINT_COSTS = {
    # Basiques
    MaintenanceType.MECHANICAL_CHECK: 50.0, MaintenanceType.CLEANING: 20.0,
    MaintenanceType.HOOF_CARE: 40.0, MaintenanceType.SADDLE_MAINTENANCE: 15.0,
    MaintenanceType.TIRE_CHANGE: 120.0, MaintenanceType.OIL_CHANGE: 89.0,
    MaintenanceType.AXLE_GREASING: 30.0,
    # Spécifiques (MER / AIR / FANTASY)
    MaintenanceType.HULL_CLEANING: 500.0,    # Bateau
    MaintenanceType.SONAR_CHECK: 150.0,      # Sous-marin
    MaintenanceType.NUCLEAR_SERVICE: 5000.0, # Sous-marin
    MaintenanceType.AVIONICS_CHECK: 300.0,   # Avion
    MaintenanceType.ROTOR_INSPECTION: 200.0, # Hélico
    MaintenanceType.WING_CARE: 60.0,         # Aigle/Dragon
    MaintenanceType.SCALE_POLISHING: 100.0   # Dragon
}

DEFAULT_DURATIONS = {
    MaintenanceType.MECHANICAL_CHECK: 1.0, MaintenanceType.CLEANING: 0.5,
    MaintenanceType.HOOF_CARE: 0.5, MaintenanceType.SADDLE_MAINTENANCE: 2.0,
    MaintenanceType.TIRE_CHANGE: 0.5, MaintenanceType.OIL_CHANGE: 0.5,
    MaintenanceType.AXLE_GREASING: 1.0,
    # Spécifiques
    MaintenanceType.HULL_CLEANING: 3.0,
    MaintenanceType.SONAR_CHECK: 1.0,
    MaintenanceType.NUCLEAR_SERVICE: 15.0,
    MaintenanceType.AVIONICS_CHECK: 2.0,
    MaintenanceType.ROTOR_INSPECTION: 1.0,
    MaintenanceType.WING_CARE: 1.0,
    MaintenanceType.SCALE_POLISHING: 0.5
}

# --- 🛠️ HELPERS AMÉLIORÉS ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def ask_int(msg):
    return IntPrompt.ask(f"[bold cyan]{msg}[/]")

def ask_float(msg):
    return FloatPrompt.ask(f"[bold cyan]{msg}[/]")

def ask_float_def(msg, default):
    return FloatPrompt.ask(f"[bold cyan]{msg}[/]", default=default)

def ask_bool(msg):
    return Confirm.ask(f"[bold yellow]{msg}[/]")

def ask_text(msg):
    return Prompt.ask(f"[bold cyan]{msg}[/]")

# --- 📋 MENU PRINCIPAL VISUEL ---
def show_main_menu(system, storage):
    menu_text = """
[bold green]1.[/] 📋 Voir la flotte (Tableau)
[bold green]2.[/] ➕ Ajouter un élément
[bold green]3.[/] 🔧 Maintenance / Soins
[bold green]4.[/] 🐴 Atteler (Charrette/Calèche)
[bold green]5.[/] 🗑️ Supprimer un élément
[bold cyan]6.[/] 🔍 Voir Détails (Fiche)
[bold magenta]7.[/] 📊 Stats & Recherche
[bold red]8.[/] 💾 Sauvegarder et Quitter 
    """
    console.print(Panel(menu_text, title="[bold blue]GESTION DE FLOTTE[/]", subtitle="Terre • Air • Mer", expand=False))

    fleet = system.fleet

    while True:
        choice = Prompt.ask("Action Garage", choices=["1", "2", "3", "4", "5", "6", "7", "0"])

        if choice == '0': break
        elif choice == '1' : list_fleet(fleet)
        elif choice == '2' : add_menu_by_environment(fleet)
        elif choice == '3' : maintenance_menu(fleet)
        elif choice == '4' : harness_menu(fleet)
        elif choice == '5' : delete_menu(fleet)
        elif choice == '6' : show_single_vehicle_details(fleet)
        elif choice == '7' : statistics_menu(fleet)
        elif choice == '8':
            storage.save_system(system)
            console.print("[bold green]💾 Système sauvegardé ! Retour au menu principal.[/]")
            Prompt.ask("Entrée pour continuer...")
            break

def show_single_vehicle_details(fleet):
    target_id = ask_int("Entrez l'ID de l'élément à inspecter")
    obj = next((v for v in fleet if v.id == target_id), None)

    if not obj:
        console.print("[red]❌ ID introuvable.[/]")
        return
    
    table = Table(title=f"Fiche Technique : {obj.__class__.__name__}", box=ROUNDED, show_header=False)
    table.add_column("Attribut", style="cyan bold", justify="right")
    table.add_column("Valeur", style="white")

    table.add_row("ID Unique", str(obj.id))

    s_color = "green" if obj.status == VehicleStatus.AVAILABLE else "red" if obj.status == VehicleStatus.UNDER_MAINTENANCE else "yellow"
    table.add_row("Statut Actuel", f"[{s_color}]{obj.status.value}[/]")

    table.add_row("Tarif Journalier", f"{obj.daily_rate}€")

    ignored_keys = ['id', 'status', 'daily_rate', 'maintenance_log', 'animals', 'animal_ids']

    for key, value in obj.__dict__.items():
        if key not in ignored_keys:
            pretty_key = key.replace("_", " ").title()

            if isinstance(value, bool):
                pretty_value = "[green]Oui[/]" if value else "[red]Non[/]"
            else:
                pretty_value = str(value)
                
            table.add_row(pretty_key, pretty_value)

    console.print("\n")
    console.print(table)

    if isinstance(obj, TowedVehicle) and obj.animals:
        console.print(f"\n[bold u]🐴 Animaux attelés ({len(obj.animals)}) :[/]")
        for a in obj.animals:
            console.print(f" - [cyan]#{a.id}[/] {a.name} ({a.breed})")

    if obj.maintenance_log:
        console.print(f"\n[bold u]🔧 Historique Maintenance ({len(obj.maintenance_log)}) :[/]")
        m_table = Table(box=ROUNDED)
        m_table.add_column("Date", style="dim")
        m_table.add_column("Type", style="magenta")
        m_table.add_column("Coût", justify="right")
        m_table.add_column("Description")

        for m in obj.maintenance_log:
            m_table.add_row(str(m.date), m.type.value, f"{m.cost}€", m.description)

        console.print(m_table)
    else:
        console.print("\n[dim i]Aucun historique de maintenance.[/]")

    Prompt.ask("\n[bold]Appuyez sur Entrée pour revenir au menu...[/]")

# --- 📊 AFFICHAGE EN TABLEAU ---
def list_fleet(fleet, title_str="État de la Flotte"):
    if not fleet:
        console.print(f"[red]🚫 {title_str} : Aucun élément trouvé.[/]")
        return
    
    table = Table(title=f"📊 {title_str} ({len(fleet)} éléments)")

    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Identifiant", style="yellow") # Plaque ou Nom
    table.add_column("Description", style="white")  # Marque/Modèle ou Race
    table.add_column("Info", justify="center", style="dim") # Année ou Âge
    table.add_column("Caractéristiques Spécifiques", style="blue")
    table.add_column("Tarif", justify="right", style="green")
    table.add_column("Statut", justify="center")

    for v in fleet:
        obj_type = v.__class__.__name__
        
        # --- 1. DONNÉES GÉNÉRALES ---
        if isinstance(v, MotorizedVehicle):
            ident = v.license_plate
            desc = f"{v.brand} {v.model}"
            info = str(v.year)
        elif isinstance(v, TransportAnimal):
            ident = v.name
            desc = v.breed
            info = f"{v.age} ans"
        elif isinstance(v, TowedVehicle):
            ident = "---"
            desc = "Véhicule Tracté"
            info = "-"
        else:
            ident, desc, info = "-", "-", "-"

        details = ""

        if isinstance(v, Car):
            clim = "❄️" if v.has_ac else "🔥"
            details = f"{v.door_count} portes {clim}"
        elif isinstance(v, Truck):
            details = f"{v.cargo_volume}m³ / {v.max_weight}T"
        elif isinstance(v, Motorcycle):
            top = "📦" if v.has_top_case else ""
            details = f"{v.engine_displacement}cc {top}"
        elif isinstance(v, Hearse):
            froid = "❄️" if v.has_refrigeration else ""
            details = f"Cercueil {v.max_coffin_length}m {froid}"
        elif isinstance(v, GoKart):
            loc = "🏠" if v.is_indoor else "🌳"
            details = f"{v.engine_type} {loc}"

        elif isinstance(v, Boat):
            details = f"{v.length_meters}m / {v.power_cv}cv"
        elif isinstance(v, Submarine):
            nuc = "☢️" if v.is_nuclear else "🔋"
            details = f"Prof: -{v.max_depth}m {nuc}"

        elif isinstance(v, Plane):
            details = f"Env: {v.wingspan}m / {v.engines_count} mot."
        elif isinstance(v, Helicopter):
            details = f"{v.rotor_count} pales / Max {v.max_altitude}m"

        elif isinstance(v, Horse):
            details = f"{v.wither_height}cm"
        elif isinstance(v, Donkey):
            têtu = "😤" if v.is_stubborn else "😇"
            details = f"Charge {v.pack_capacity_kg}kg {têtu}"
        elif isinstance(v, Camel):
            details = f"{v.hump_count} bosses / {v.water_reserve}L"

        elif isinstance(v, Whale):
            chant = "🎵" if v.can_sing else "🔇"
            details = f"{v.weight_tonnes}T {chant}"
        elif isinstance(v, Dolphin):
            tricks = "🎪" if v.knows_tricks else ""
            details = f"{v.swim_speed}km/h {tricks}"

        elif isinstance(v, Eagle):
            details = f"Env: {v.wingspan_cm}cm / Alt: {v.max_altitude}m"
        elif isinstance(v, Dragon):
            details = f"Feu: {v.fire_range}m ({v.scale_color})"

        elif isinstance(v, Carriage):
            toit = "☂️" if v.has_roof else "☀️"
            nb_chevaux = len(v.animals)
            details = f"{v.seat_count}pl {toit} (Tiré par {nb_chevaux} chv)"
        elif isinstance(v, Cart):
            nb_anes = len(v.animals)
            details = f"Max {v.max_load_kg}kg (Tiré par {nb_anes} ânes)"

        s_icon, s_color = "🟢", "green"
        if v.status == VehicleStatus.RENTED:
            s_icon, s_color = "🟡", "yellow"
        elif v.status == VehicleStatus.UNDER_MAINTENANCE:
            s_icon, s_color = "🔧", "red"
        elif v.status == VehicleStatus.OUT_OF_SERVICE:
            s_icon, s_color = "💀", "grey"

        status_txt = f"[{s_color}]{s_icon} {v.status.value}[/]"

        table.add_row(
            str(v.id), 
            obj_type, 
            ident, 
            desc, 
            info, 
            details, 
            f"{v.daily_rate}€", 
            status_txt
        )
    
    console.print(table)

def visualize_menu(fleet):
    console.print(Panel("[1] ♾️  TOUT VOIR\n[2] 🚗 VÉHICULES MOTEUR\n[3] 🐎 ANIMAUX\n[4] 🚜 ATTELAGES\n[0] Retour", title="Filtres d'affichage"))
    choice = Prompt.ask("Votre choix", choices=["0", "1", "2", "3", "4"])

    if choice == '0': return

    subset = []
    titre = ""

    if choice == '1':
        subset = fleet
        titre = "Toute la Flotte"
    elif choice == '2':
        subset = [x for x in fleet if isinstance(x, MotorizedVehicle)]
        titre = "Véhicules Motorisés"
    elif choice == '3':
        subset = [x for x in fleet if isinstance(x, TransportAnimal)]
        titre = "Animaux"
    elif choice == '4':
        subset = [x for x in fleet if isinstance(x, TowedVehicle)]
        titre = "Véhicules Tractés"

    list_fleet(subset, titre)

# --- 🌍 MENU AJOUT ---
def add_menu_by_environment(fleet):
    console.print(Panel("[1] ⛰️ TERRE\n[2] 🌊 MER\n[3] ☁️ AIR\n[0] Retour", title="Choix Environnement"))
    env = Prompt.ask("Votre choix", choices=["0", "1", "2", "3"])

    if env == '0': return

    new_id = 1 if not fleet else max(v.id for v in fleet) + 1

    # ================= TERRE =================
    if env == '1':
        rprint("[bold]Types :[/] 1.Voiture 2.Camion 3.Moto 4.Corbillard 5.Kart 6.Cheval 7.Âne 8.Chameau 9.Calèche 10.Charrette")
        c = Prompt.ask("Type", choices=[str(i) for i in range(1,11)])
        rate = ask_float_def("Tarif", DEFAULT_RENTAL_PRICES.get(c, 50.0))

        if c in ['1', '2', '3', '4', '5']:
            brand = ask_text("Marque")
            model = ask_text("Modèle")

            if c == '5': # Kart
                label_id = "Numéro du Kart (ex: K-01)"
            else:
                label_id = "Plaque d'immatriculation"

            plate = ask_text(label_id)
            year = ask_int("Année")

            if c=='1': fleet.append(Car(new_id, rate, brand, model, plate, year, ask_int("Nb Portes"), ask_bool("Climatisation ?")))
            elif c=='2': fleet.append(Truck(new_id, rate, brand, model, plate, year, ask_float("Volume (m3)"), ask_float("Poids Max (T)")))
            elif c=='3': fleet.append(Motorcycle(new_id, rate, brand, model, plate, year, ask_int("Cylindrée (cc)"), ask_bool("Avec TopCase ?")))
            elif c=='4': fleet.append(Hearse(new_id, rate, brand, model, plate, year, ask_float("Long. Cercueil (m)"), ask_bool("Réfrigéré ?")))
            elif c=='5': fleet.append(GoKart(new_id, rate, brand, model, plate, year, ask_text("Type Moteur"), ask_bool("Indoor ?")))

        elif c in ['6', '7', '8']:
            name = ask_text("Nom")
            breed = ask_text("Race")
            age = ask_int("Âge")

            if c=='6': fleet.append(Horse(new_id, rate, name, breed, age, ask_int("Taille (cm)"), ask_int("Fer Av (mm)"), ask_int("Fer Arr (mm)")))
            elif c=='7': fleet.append(Donkey(new_id, rate, name, breed, age, ask_float("Capacité (kg)"), ask_bool("Têtu ?")))
            elif c=='8': fleet.append(Camel(new_id, rate, name, breed, age, ask_int("Nb Bosses"), ask_float("Réserve Eau (L)")))

        elif c in ['9', '10']:
            seats = ask_int("Nb Places")
            if c=='9': fleet.append(Carriage(new_id, rate, seats, ask_bool("Avec Toit ?")))
            elif c=='10': fleet.append(Cart(new_id, rate, seats, ask_float("Charge Max (kg)")))

    # ================= MER =================
    elif env == '2':
        rprint("[bold]Types :[/] 1.Bateau 2.Sous-Marin 3.Baleine 4.Dauphin")
        c = Prompt.ask("Type", choices=["1","2","3","4"])
        key = {'1':'11', '2':'16', '3':'13', '4':'14'}
        rate = ask_float_def("Tarif", DEFAULT_RENTAL_PRICES.get(key[c], 200.0))

        if c in ['1', '2']: # Moteurs Marins
            brand = ask_text("Chantier Naval / Marque")
            model = ask_text("Modèle / Classe")

            plate = ask_text("Nom du Vaisseau ou Numéro de Coque")
            year = ask_int("Année de mise à l'eau")

            if c=='1': fleet.append(Boat(new_id, rate, brand, model, plate, year, ask_float("Longueur (m)"), ask_float("Puissance (cv)")))
            elif c=='2': fleet.append(Submarine(new_id, rate, brand, model, plate, year, ask_float("Prof. Max (m)"), ask_bool("Nucléaire ?")))

        else: # Animaux Marins
            name = ask_text("Nom")
            breed = ask_text("Espèce")
            age = ask_int("Âge")
            if c=='3': fleet.append(Whale(new_id, rate, name, breed, age, ask_float("Poids (T)"), ask_bool("Chante ?")))
            elif c=='4': fleet.append(Dolphin(new_id, rate, name, breed, age, ask_float("Vitesse (km/h)"), ask_bool("Connaît des tours ?")))

    # ================= AIR =================
    elif env == '3':
        rprint("[bold]Types :[/] 1.Avion 2.Hélico 3.Aigle 4.Dragon")
        c = Prompt.ask("Type", choices=["1","2","3","4"])
        key = {'1':'15', '2':'12', '3':'17', '4':'18'}
        rate = ask_float_def("Tarif", DEFAULT_RENTAL_PRICES.get(key[c], 500.0))

        if c in ['1', '2']: # Moteurs Air
            brand = ask_text("Constructeur")
            model = ask_text("Modèle")

            plate = ask_text("Immatriculation (ex: F-GHIJ)")
            year = ask_int("Année")

            if c=='1': fleet.append(Plane(new_id, rate, brand, model, plate, year, ask_float("Envergure (m)"), ask_int("Nb Moteurs")))
            elif c=='2': fleet.append(Helicopter(new_id, rate, brand, model, plate, year, ask_int("Nb Pales"), ask_int("Alt. Max (m)")))
        
        else:
            name = ask_text("Nom")
            age = ask_int("Âge")
            if c=='3': fleet.append(Eagle(new_id, rate, name, ask_text("Espèce"), age, ask_int("Envergure (cm)"), ask_int("Alt. Max (m)")))
            elif c=='4': fleet.append(Dragon(new_id, rate, name, "Dragon", age, ask_float("Portée Feu (m)"), ask_text("Couleur Écailles")))

    console.print(f"[bold green]✅ Élément ajouté avec succès ! (ID: {new_id})[/]")

# --- MAINTENANCE ---
def maintenance_menu(fleet):
    list_fleet(fleet) # Affiche le tableau pour choisir l'ID

    tid = ask_int("ID de l'élément à entretenir")
    obj = next((v for v in fleet if v.id == tid), None)
    
    if not obj:
        console.print("[red]❌ ID introuvable.[/]")
        return
    
    console.print(f"[bold]Sélection :[/] {obj.show_details()}")
    
    options = [MaintenanceType.CLEANING]

    if isinstance(obj, TransportAnimal):
        if isinstance(obj, (Horse, Donkey, Camel)):
            options.extend([MaintenanceType.HOOF_CARE, MaintenanceType.SADDLE_MAINTENANCE])
        
        elif isinstance(obj, (Eagle, Dragon)):
            options.append(MaintenanceType.WING_CARE)
            if isinstance(obj, Dragon):
                options.append(MaintenanceType.SCALE_POLISHING)

        elif isinstance(obj, (Whale, Dolphin)):
            options.append(MaintenanceType.HOOF_CARE)

    elif isinstance(obj, MotorizedVehicle):
        options.extend([MaintenanceType.MECHANICAL_CHECK, MaintenanceType.OIL_CHANGE])
        if isinstance(obj, (Car, Truck, Motorcycle, Hearse, GoKart)):
            options.append(MaintenanceType.TIRE_CHANGE)

        elif isinstance(obj, (Boat, Submarine)):
            options.append(MaintenanceType.HULL_CLEANING)

            if isinstance(obj, Submarine):
                options.extend([MaintenanceType.SONAR_CHECK, MaintenanceType.NUCLEAR_SERVICE])

        elif isinstance(obj, (Plane, Helicopter)):
            options.append(MaintenanceType.AVIONICS_CHECK)
            if isinstance(obj, Helicopter):
                options.append(MaintenanceType.ROTOR_INSPECTION)

    elif isinstance(obj, TowedVehicle):
        options.extend([MaintenanceType.AXLE_GREASING, MaintenanceType.TIRE_CHANGE])

    rprint("\n[bold u]Interventions possibles pour ce type :[/]")

    choices_str = []
    for i, t in enumerate(options):
        cost = DEFAULT_MAINT_COSTS.get(t, 0)
        rprint(f"  [cyan bold]{i+1}.[/] {t.value} [dim](~{cost}€)[/]")
        choices_str.append(str(i+1))
    
    c_idx = Prompt.ask("Votre choix", choices=choices_str)
    selected_type = options[int(c_idx) - 1]

    def_cost = DEFAULT_MAINT_COSTS.get(selected_type, 50.0)
    def_time = DEFAULT_DURATIONS.get(selected_type, 1.0)

    cost = ask_float_def("Coût final", def_cost)
    console.print(f"[dim]Durée estimée : {def_time} jour(s)[/]")

    new_m = Maintenance(len(obj.maintenance_log)+1, date.today(), selected_type, cost, "Entretien", def_time)
    obj.add_maintenance(new_m)

    if ask_bool("Mettre en statut 'En Maintenance' ?"):
        obj.status = VehicleStatus.UNDER_MAINTENANCE

    console.print("[bold green]✅ Maintenance enregistrée avec succès ![/]")

# --- ATTELAGE ---
def harness_menu(fleet):
    list_fleet(fleet)
    vid = ask_int("ID Véhicule Tracté")
    v = next((x for x in fleet if x.id == vid), None)
    
    if not isinstance(v, TowedVehicle):
        console.print("[red]❌ Ce n'est pas une calèche ou charrette.[/]")
        return
    
    aid = ask_int("ID Animal")
    a = next((x for x in fleet if x.id == aid), None)
    
    # Capture du print de harness_animal pour le styliser si besoin, 
    # mais ici on laisse la méthode de classe gérer le print
    console.rule("[bold]Résultat Attelage[/]")
    v.harness_animal(a)
    console.rule()

# --- SUPPRESSION ---
def delete_menu(fleet):
    list_fleet(fleet)
    tid = ask_int("ID à supprimer")
    found = next((v for v in fleet if v.id == tid), None)
    
    if found:
        rprint(f"[bold red]❓ Supprimer : {found.show_details()} ?[/]")
        if Confirm.ask("Confirmer"):
            fleet.remove(found)
            console.print("[bold red]🗑️ Élément supprimé.[/]")
    else:
        console.print("[red]❌ Introuvable.[/]")

# --- 📊 MENU STATISTIQUES & RECHERCHE ---
from rich.progress import track
from time import sleep

def statistics_menu(fleet):
    while True:
        console.print(Panel("[1] 📈 Rapport Global\n[2] 🔍 Recherche Avancée\n[0] Retour", title="Intelligence Artificielle (ou presque)"))
        choice = Prompt.ask("Votre choix", choices=["0", "1", "2"])
        
        if choice == '0': break

        # --- 1. RAPPORT GLOBAL ---
        if choice == '1':
            total = len(fleet)
            if total == 0:
                console.print("[red]Flotte vide.[/]")
                continue

            # Calculs
            nb_maint = sum(1 for v in fleet if v.status == VehicleStatus.UNDER_MAINTENANCE)
            nb_rented = sum(1 for v in fleet if v.status == VehicleStatus.RENTED)
            nb_avail = sum(1 for v in fleet if v.status == VehicleStatus.AVAILABLE)
            
            # Affichage "Fun" avec Rich
            console.rule("[bold blue]RAPPORT DE FLOTTE[/]")
            console.print(f"Total Véhicules : [bold cyan]{total}[/]")
            console.print(f"💰 Revenu Potentiel/Jour : [bold green]{sum(v.daily_rate for v in fleet)}€[/]")
            
            # Barres visuelles
            pct_maint = (nb_maint / total) * 100
            pct_dispo = (nb_avail / total) * 100
            
            rprint(f"\n[red]En Maintenance : {nb_maint}[/] ({pct_maint:.1f}%)")
            console.print("█" * int(pct_maint/5), style="red")
            
            rprint(f"\n[green]Disponibles    : {nb_avail}[/] ({pct_dispo:.1f}%)")
            console.print("█" * int(pct_dispo/5), style="green")
            console.print("\n")

        # --- 2. RECHERCHE AVANCÉE ---
        elif choice == '2':
            console.rule("[bold yellow]RECHERCHE INTELIGENTE[/]")
            max_p = ask_float("Budget Max par jour (€)")
            
            # Simulation de recherche (pour l'effet wow)
            for _ in track(range(10), description="Analyse de la base de données..."):
                sleep(0.05)

            # Filtrage
            results = [v for v in fleet if v.daily_rate <= max_p and v.status == VehicleStatus.AVAILABLE]
            
            if results:
                # On réutilise votre super fonction d'affichage
                list_fleet(results, f"Véhicules dispo à moins de {max_p}€")
            else:
                console.print(f"[red]Aucun véhicule trouvé pour ce budget.[/]")