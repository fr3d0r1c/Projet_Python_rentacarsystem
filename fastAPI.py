import sys
import os
from fastapi import FastAPI

# =========================================================
# 🔧 LE CORRECTIF (HACK DU CHEMIN)
# =========================================================
# 1. On prend le dossier où se trouve api.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. On cible le dossier INTERNE "CarRentalSystem"
# C'est là que se cachent 'fleet', 'location', etc.
project_folder = os.path.join(current_dir, "CarRentalSystem")

# 3. On ajoute ce dossier interne à la liste de recherche de Python
if project_folder not in sys.path:
    sys.path.append(project_folder)

# =========================================================
# MAINTENANT, ON IMPORTE "COMME SI" ON ÉTAIT DEDANS
# =========================================================
# ⚠️ ATTENTION : Ne remets PAS "CarRentalSystem." devant !
from location.system import CarRentalSystem
from storage import StorageManager
from fleet.enums import VehicleStatus

# --- DÉMARRAGE DE L'API ---
app = FastAPI()

# Chargement des données
storage = StorageManager("data.json")
system = storage.load_system()

@app.get("/api/dashboard")
def get_dashboard_data():
    # Calcul du CA pour les locations terminées
    total_ca = sum(r.total_cost for r in system.rentals if not r.is_active)
    
    loues = []
    dispos = []

    for v in system.fleet:
        # Sécurisation des noms (marche pour tout type de véhicule)
        nom = getattr(v, 'brand', getattr(v, 'name', '?'))
        modele = getattr(v, 'model', getattr(v, 'breed', ''))
        
        info = {
            "Type": v.__class__.__name__,
            "Véhicule": f"{nom} {modele}",
            "ID": v.id
        }
        
        if v.status == VehicleStatus.AVAILABLE:
            dispos.append(info)
        else:
            loues.append(info)

    return {
        "ca_total": total_ca,
        "nb_clients": len(system.customers),
        "nb_flotte": len(system.fleet),
        "loues": loues,
        "dispos": dispos
    }