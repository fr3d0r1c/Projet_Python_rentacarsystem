import sys
import os
from datetime import date, timedelta

current_dir = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.join(current_dir, "CarRentalSystem")
if project_folder not in sys.path:
    sys.path.append(project_folder)

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from rich import print as rprint

# --- IMPORTS DES MODULES ---
from location.system import CarRentalSystem
from clients.customer import Customer
from storage import StorageManager
import console_ui as fleet_ui

console = Console()

def main():
    system = CarRentalSystem()
    
    storage = StorageManager("ma_flotte.json")
    system.fleet = storage.load_fleet() 
    
    while True:
        console.clear()
        show_global_menu()
        choice = Prompt.ask("Votre choix ", choices=["1", "2", "3", "4", "5", "0"])

        if choice == "1":
            while True:
                print("\n")
                console.rule("[bold cyan]GARAGE & ÉCURIE[/]")
                fleet_ui.show_main_menu() # Affiche votre menu existant
                
                sub_choice = Prompt.ask("Action Garage (0 pour Retour Menu Principal)")
                
                if sub_choice == '0': break
                elif sub_choice == '1': fleet_ui.list_fleet(system.fleet) # Ou visualize_menu
                elif sub_choice == '2': fleet_ui.add_menu_by_environment(system.fleet)
                elif sub_choice == '3': fleet_ui.maintenance_menu(system.fleet)
                elif sub_choice == '4': fleet_ui.harness_menu(system.fleet)
                elif sub_choice == '5': fleet_ui.delete_menu(system.fleet)
                elif sub_choice == '6': 
                    storage.save_fleet(system.fleet)
                    Prompt.ask("Sauvegardé. Appuyez sur Entrée...")
                else:
                    fleet_ui.statistics_menu(system.fleet)

        # ---------------------------------------------------------
        # 2. GESTION DES CLIENTS (Nouveau)
        # ---------------------------------------------------------
        elif choice == "2":
            manage_customers(system)

        # ---------------------------------------------------------
        # 3. GESTION DES LOCATIONS (Nouveau)
        # ---------------------------------------------------------
        elif choice == "3":
            manage_rentals(system)

        # ---------------------------------------------------------
        # 4. RAPPORTS FINANCIERS
        # ---------------------------------------------------------
        elif choice == "4":
            console.clear()
            system.generate_revenue_report()
            system.generate_active_rentals_report()
            Prompt.ask("\n[dim]Appuyez sur Entrée pour revenir...[/]")

        # ---------------------------------------------------------
        # 5. SAUVEGARDE GLOBALE
        # ---------------------------------------------------------
        elif choice == "5":
            # Pour l'instant on ne sauvegarde que la flotte tant que storage n'est pas updaté pour tout
            storage.save_fleet(system.fleet)
            console.print("[bold green]💾 Flotte sauvegardée ![/]")
            # TODO: Sauvegarder clients et locations ici plus tard
            Prompt.ask("[dim]Entrée pour continuer...[/]")

        # ---------------------------------------------------------
        # 0. QUITTER
        # ---------------------------------------------------------
        elif choice == "0":
            if Confirm.ask("Voulez-vous vraiment quitter ?"):
                console.print("[bold blue]Au revoir ! 👋[/]")
                sys.exit()

# --- VUES SECONDAIRES ---

def show_global_menu():
    text = """
[bold cyan]1.[/] 🚗 [bold]GESTION DE LA FLOTTE[/] (Garage, Écurie, Hangar)
       [dim]Ajouter véhicules, Maintenance, Attelages...[/]

[bold magenta]2.[/] 👥 [bold]GESTION DES CLIENTS[/]
       [dim]Inscrire un nouveau client, Voir la liste...[/]

[bold yellow]3.[/] 📝 [bold]COMPTOIR LOCATIONS[/]
       [dim]Louer un véhicule, Retourner un véhicule...[/]

[bold green]4.[/] 💰 [bold]RAPPORTS & FINANCE[/]
       [dim]Chiffre d'affaires, Locations actives...[/]

[bold blue]5.[/] 💾 [bold]SAUVEGARDER[/]

[bold red]0.[/] ❌ [bold]QUITTER[/]
    """
    console.print(Panel(text, title="[bold white on blue] CAR RENTAL SYSTEM [/]", expand=False))

def manage_customers(system):
    while True:
        console.clear()
        console.rule("[bold magenta]👥 GESTION CLIENTS[/]")
        rprint("[1] Liste des Clients\n[2] Nouveau Client\n[0] Retour")
        c = Prompt.ask("Choix", choices=["1", "2", "0"])
        
        if c == '0': break
        
        elif c == '1':
            table = Table(title="Fichier Client")
            table.add_column("ID", style="cyan")
            table.add_column("Nom", style="white")
            table.add_column("Permis", style="yellow")
            table.add_column("Email")
            
            for cust in system.customers:
                table.add_row(str(cust.id), cust.name, cust.driver_license, cust.email)
            console.print(table)
            Prompt.ask("\nEntrée pour continuer...")
            
        elif c == '2':
            # Création Client
            cid = len(system.customers) + 1
            name = Prompt.ask("Nom Prénom")
            permis = Prompt.ask("Numéro Permis")
            email = Prompt.ask("Email")
            tel = Prompt.ask("Téléphone")
            
            new_c = Customer(cid, name, permis, email, tel)
            system.add_customer(new_c)
            rprint(f"[green]Client {name} ajouté ![/]")
            Prompt.ask("Entrée pour continuer...")

def manage_rentals(system):
    while True:
        console.clear()
        console.rule("[bold yellow]📝 COMPTOIR LOCATIONS[/]")
        rprint("[1] 🔑 Nouvelle Location (Départ)\n[2] ↩️  Retour Véhicule (Fin)\n[3] 📜 Voir Contrats Actifs\n[0] Retour")
        c = Prompt.ask("Choix", choices=["1", "2", "3", "0"])
        
        if c == '0': break
        
        elif c == '1':
            # 1. Choisir Client
            cid = IntPrompt.ask("ID du Client")
            
            # 2. Choisir Véhicule (On pourrait afficher la liste dispo ici)
            vid = IntPrompt.ask("ID du Véhicule à louer")
            
            # 3. Dates (Simplifié pour le test, on met aujourd'hui et demain)
            d_start = date.today()
            # On demande la durée
            days = IntPrompt.ask("Durée (jours)")
            from datetime import timedelta
            d_end = d_start + timedelta(days=days)
            
            # Action
            system.create_rental(cid, vid, d_start, d_end)
            Prompt.ask("Entrée pour continuer...")

        elif c == '2':
            rid = IntPrompt.ask("ID du Contrat de Location à clôturer")
            system.return_vehicle(rid)
            Prompt.ask("Entrée pour continuer...")
            
        elif c == '3':
            system.generate_active_rentals_report()
            Prompt.ask("Entrée pour continuer...")

if __name__ == "__main__":
    main()