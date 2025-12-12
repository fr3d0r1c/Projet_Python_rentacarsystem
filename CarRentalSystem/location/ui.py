from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from .rental import Rental  # Import relatif

console = Console()

def menu_locations(system):
    """Gère le menu des locations."""
    while True:
        console.clear()
        console.rule("[bold yellow]📝 COMPTOIR LOCATIONS[/]")
        
        console.print("[1] 🔑 Nouvelle Location")
        console.print("[2] ↩️  Retour Véhicule")
        console.print("[3] 📜 Voir Contrats Actifs")
        console.print("[0] Retour")
        
        choice = Prompt.ask("Choix", choices=["1", "2", "3", "0"])
        
        if choice == '0': break
        
        # --- NOUVELLE LOCATION ---
        elif choice == '1':
            console.rule("[bold]Nouvelle Location[/]")
            client_id = IntPrompt.ask("ID du Client")
            customer = next((c for c in system.customers if c.id == client_id), None)
            
            if not customer:
                console.print(f"[red]Client introuvable.[/]")
                Prompt.ask("Entrée...")
                continue

            vehicle_id = IntPrompt.ask("ID du Véhicule")
            vehicle = next((v for v in system.fleet if v.id == vehicle_id), None)
            
            if not vehicle or not vehicle.is_available:
                console.print(f"[red]Véhicule introuvable ou indisponible.[/]")
                Prompt.ask("Entrée...")
                continue

            s_str = Prompt.ask("Date début (YYYY-MM-DD)", default="2023-10-01")
            e_str = Prompt.ask("Date fin (YYYY-MM-DD)", default="2023-10-05")

            try:
                new_rental = Rental(customer, vehicle, s_str, e_str)
                system.rentals.append(new_rental)
                cost = new_rental.calculate_cost()
                
                console.print(Panel(f"Location Validée !\nCoût estimé : {cost} €", style="green"))
            except ValueError as e:
                console.print(f"[red]Erreur : {e}[/]")
            
            Prompt.ask("Entrée...")

        # --- RETOUR ---
        elif choice == '2':
            # ... (Copiez ici votre logique de retour que nous avons faite précédemment) ...
            pass # Je raccourcis pour l'exemple
            
        # --- LISTE ---
        elif choice == '3':
            for r in system.rentals:
                status = "🟢" if r.is_active else "🔴"
                console.print(f"{status} {r.vehicle.model} loué par {r.customer.name}")
            Prompt.ask("Entrée...")