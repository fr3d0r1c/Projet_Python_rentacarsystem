from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import print as rprint
from .customer import Customer

console = Console()

def menu_clients(system):
    while True:
        console.clear()
        console.rule("[bold magenta]👥 GESTION CLIENTS[/]")
        rprint("[1] Liste des Clients\n[2] Nouveau Client\n[0] Retour")

        choice = Prompt.ask("Choix", choices=["1", "2", "0"])

        if choice == '0': break

        elif choice == '1':
            table = Table(title="Fichier Client")
            table.add_column("ID", style="cyan")
            table.add_column("Nom", style="white")
            table.add_column("Permis", style="yellow")
            table.add_column("Email")

            for cust in system.customers:
                table.add_row(str(cust.id), cust.name, cust.driver_license, cust.email)
            console.print(table)
            Prompt.ask("\nEntrée pour continuer...")

        elif choice == '2':
            cid = len(system.customers) + 1
            name = Prompt.ask("Nom Prénom")
            permis = Prompt.ask("Numéro Permis")
            email = Prompt.ask("Email")
            tel = Prompt.ask("Téléphone")

            new_c = Customer(cid, name, permis, email, tel, username=name, password="123")
            system.add_customer(new_c)

            rprint(f"[green]Client {name} ajouté ![/]")
            Prompt.ask("Entrée pour continuer...")