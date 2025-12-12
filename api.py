import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Vos imports
from CarRentalSystem.location.system import CarRentalSystem
from CarRentalSystem.storage import StorageManager
from CarRentalSystem.location.rental import Rental

# 1. Initialisation
app = FastAPI(title="Rent-A-Dream API 🚀")
storage = StorageManager("data.json")
system = storage.load_system()

if system is None:
    system = CarRentalSystem()

# 2. Modèles de données (Le contrat d'interface)
# Ce sont les données que le Streamlit doit envoyer pour créer une location
class RentalRequest(BaseModel):
    customer_id: int
    vehicle_id: int
    start_date: str  # Format YYYY-MM-DD
    end_date: str    # Format YYYY-MM-DD

# --- ROUTES (ENDPOINTS) ---

@app.get("/")
def home():
    return {"message": "API Rent-A-Dream opérationnelle !"}

@app.get("/fleet")
def get_fleet():
    """Renvoie tout le parc en JSON."""
    return [v.to_dict() for v in system.fleet]

@app.get("/customers")
def get_customers():
    """Renvoie tous les clients."""
    return [c.to_dict() for c in system.customers]

@app.get("/rentals")
def get_rentals():
    """Renvoie toutes les locations (pour l'admin)."""
    # Assurez-vous d'avoir ajouté to_dict() dans la classe Rental !
    return [r.to_dict() for r in system.rentals] 

@app.post("/rentals/")
def create_rental(data: RentalRequest):
    """Crée une nouvelle location."""
    # 1. On cherche les objets réels à partir des IDs reçus
    customer = next((c for c in system.customers if c.id == data.customer_id), None)
    vehicle = next((v for v in system.fleet if v.id == data.vehicle_id), None)

    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule introuvable")
    
    try:
        # 2. On utilise votre classe Rental existante
        new_rental = Rental(customer, vehicle, data.start_date, data.end_date)
        system.rentals.append(new_rental)
        
        # 3. On sauvegarde immédiatement
        storage.save_system(system)
        
        return {
            "message": "Location créée", 
            "cost": new_rental.total_cost,
            "rental_id": len(system.rentals) # Ou un vrai ID si vous en avez mis un
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rentals/{rental_index}/return")
def return_vehicle(rental_index: int, return_date: str):
    """Clôture une location."""
    try:
        if rental_index < 0 or rental_index >= len(system.rentals):
            raise HTTPException(status_code=404, detail="Location introuvable")
            
        rental = system.rentals[rental_index]
        final_cost = rental.close_rental(return_date)
        storage.save_system(system)
        
        return {"message": "Retour validé", "final_cost": final_cost, "penalty": rental.penalty}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Lancement pour le débogage direct (facultatif)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)