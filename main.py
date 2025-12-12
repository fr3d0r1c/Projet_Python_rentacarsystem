import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm
from rich import print as rprint
from rich.columns import Columns
from rich.box import ROUNDED

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "CarRentalSystem"))

from CarRentalSystem.location.system import CarRentalSystem
from CarRentalSystem.storage import StorageManager
from CarRentalSystem.fleet import ui as fleet_ui
from CarRentalSystem.clients import ui as clients_ui
from CarRentalSystem.location import ui as rentals_ui

console = Console()

def show_global_menu():
    text = """
[bold cyan]1.[/] 🚗 [bold]GESTION FLOTTE[/]
[bold magenta]2.[/] 👥 [bold]GESTION CLIENTS[/]
[bold yellow]3.[/] 📝 [bold]LOCATIONS[/]
[bold green]4.[/] 💾 [bold]SAUVEGARDER[/]
[bold red]0.[/] ❌ [bold]QUITTER[/]
    """
    console.print(Panel(text, title="[bold white on blue] CAR RENTAL SYSTEM [/]", expand=False))
    
def main():
    storage = StorageManager("data.json")
    system = storage.load_system()
    if system is None: system = CarRentalSystem()
    
    while True:
        console.clear()
        show_global_menu()
        choice = Prompt.ask("Votre choix ", choices=["1", "2", "3", "4", "0"])
        
        if choice == "1":
            fleet_ui.show_main_menu(system, storage)
            
        elif choice == "2":
            clients_ui.menu_clients(system)
            
        elif choice == "3":
            rentals_ui.menu_locations(system)
            
        elif choice == "4":
            storage.save_system(system)
            console.print("[green]Sauvegarde effectuée ![/]")
            Prompt.ask("Entrée...")
            
        elif choice == "0":
            if Confirm.ask("Quitter ?"):
                sys.exit()
                
if __name__ == "__main__":
    main()
