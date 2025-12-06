from enum import Enum

class VehicleStatus(Enum):
    AVAILABLE = "Disponible"
    RENTED = "Loué"
    UNDER_MAINTENANCE = "En Maintenance"
    OUT_OF_SERVICE = "Hors Service"

class MaintenanceType(Enum):
    MECHANICAL_CHECK = "Contrôle Mécanique"
    CLEANING = "Nettoyage"
    HOOF_CARE = "Soin Sabots/Griffes"
    SADDLE_MAINTENANCE = "Entretien Sellerie"
    TIRE_CHANGE = "Changement Pneus"
    OIL_CHANGE = "Vidange"
    AXLE_GREASING = "Graissage Essieux"
    
    # --- NOUVEAUX (MER/AIR/FANTASY) ---
    HULL_CLEANING = "Carénage (Coque)"       # Bateaux
    SONAR_CHECK = "Calibrage Sonar"          # Sous-marins/Bateaux
    NUCLEAR_SERVICE = "Révision Réacteur"    # Sous-marins
    AVIONICS_CHECK = "Systèmes Avioniques"   # Avions/Hélico
    ROTOR_INSPECTION = "Inspection Rotor"    # Hélico
    WING_CARE = "Soin des Ailes"             # Aigle/Dragon
    SCALE_POLISHING = "Lustrage Écailles"    # Dragon