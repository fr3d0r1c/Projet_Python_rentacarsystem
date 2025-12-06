import streamlit as st
import pandas as pd
import sys
import os
from datetime import date, timedelta

# --- 1. CONFIGURATION DU CHEMIN (Comme pour main_global) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.join(current_dir, "CarRentalSystem")
if project_folder not in sys.path:
    sys.path.append(project_folder)

# --- 2. IMPORTS DU PROJET ---
from location.system import CarRentalSystem
from storage import StorageManager
from clients.customer import Customer
from GestionFlotte.vehicles import Car, Truck, Motorcycle, Boat, Submarine, Plane, Helicopter
from GestionFlotte.animals import Horse, Donkey, Dragon
from GestionFlotte.enums import VehicleStatus

# --- 3. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="CarRental Ultime", page_icon="🚗", layout="wide")

# --- 4. CHARGEMENT DU SYSTÈME (SESSION STATE) ---
# On utilise le cache de Streamlit pour ne pas recharger le JSON à chaque clic
if 'system' not in st.session_state:
    st.session_state.system = CarRentalSystem()
    storage = StorageManager("ma_flotte.json")
    st.session_state.system.fleet = storage.load_fleet()
    # Pour l'instant, clients et locations sont en mémoire, on pourrait aussi les charger
    st.session_state.storage = storage

system = st.session_state.system
storage = st.session_state.storage

# --- 5. FONCTIONS UTILITAIRES ---
def save_data():
    storage.save_fleet(system.fleet)
    st.toast("💾 Données sauvegardées !", icon="✅")

# --- 6. INTERFACE PRINCIPALE (SIDEBAR) ---
st.sidebar.title("🌍 Navigation")
menu = st.sidebar.radio("Aller vers :", ["Tableau de Bord", "Ajouter Véhicule", "Clients", "Comptoir Locations"])

st.sidebar.markdown("---")
st.sidebar.caption(f"Flotte actuelle : {len(system.fleet)} éléments")

# =========================================================
# PAGE 1 : TABLEAU DE BORD (La Flotte)
# =========================================================
if menu == "Tableau de Bord":
    st.title("📊 État de la Flotte")

    if not system.fleet:
        st.info("La flotte est vide. Commencez par ajouter des véhicules !")
    else:
        # Création d'un DataFrame pour un affichage propre
        data = []
        for v in system.fleet:
            # Icônes de statut
            stat = "🟢 Dispo"
            if v.status == VehicleStatus.RENTED: stat = "🟡 Loué"
            elif v.status == VehicleStatus.UNDER_MAINTENANCE: stat = "🔧 Maintenance"
            
            data.append({
                "ID": v.id,
                "Type": v.__class__.__name__,
                "Marque/Nom": getattr(v, 'brand', getattr(v, 'name', '-')),
                "Modèle/Race": getattr(v, 'model', getattr(v, 'breed', '-')),
                "Année/Âge": getattr(v, 'year', getattr(v, 'age', '-')),
                "Tarif (€/j)": v.daily_rate,
                "Statut": stat
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Statistiques rapides
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Véhicules", len(system.fleet))
        col2.metric("Disponible", len([v for v in system.fleet if v.status == VehicleStatus.AVAILABLE]))
        col3.metric("En Maintenance", len([v for v in system.fleet if v.status == VehicleStatus.UNDER_MAINTENANCE]))

# =========================================================
# PAGE 2 : AJOUTER UN VÉHICULE
# =========================================================
elif menu == "Ajouter Véhicule":
    st.title("➕ Ajouter un élément")

    env = st.selectbox("Environnement", ["Terre", "Mer", "Air"])
    
    with st.form("add_vehicle_form"):
        col1, col2 = st.columns(2)
        
        # Champs communs
        daily_rate = col1.number_input("Tarif Journalier (€)", min_value=10.0, value=50.0)
        
        # Logique dynamique selon le type (Simplifiée pour l'exemple Streamlit)
        if env == "Terre":
            v_type = st.selectbox("Type", ["Voiture", "Camion", "Moto", "Cheval", "Dragon"])
        elif env == "Mer":
            v_type = st.selectbox("Type", ["Bateau", "Sous-Marin"])
        else:
            v_type = st.selectbox("Type", ["Avion", "Hélicoptère"])

        # Champs spécifiques (Exemple générique)
        ident = col1.text_input("Marque / Nom")
        model = col2.text_input("Modèle / Race")
        year_age = col1.number_input("Année / Âge", min_value=0, value=2020)
        spec = col2.text_input("Spécifique (Plaque, Immat...)")

        submitted = st.form_submit_button("Créer le véhicule")
        
        if submitted:
            new_id = 1 if not system.fleet else max(v.id for v in system.fleet) + 1
            
            # Création simplifiée (À adapter pour appeler TOUS vos constructeurs précis)
            if v_type == "Voiture":
                obj = Car(new_id, daily_rate, ident, model, spec, int(year_age), 5, True)
            elif v_type == "Cheval":
                obj = Horse(new_id, daily_rate, ident, model, int(year_age), 160, 100, 100)
            elif v_type == "Sous-Marin":
                obj = Submarine(new_id, daily_rate, ident, model, spec, int(year_age), 500, True)
            # ... (Ajoutez les autres if/elif pour vos 18 classes)
            else:
                # Fallback pour le test
                obj = Car(new_id, daily_rate, ident, model, spec, int(year_age), 4, False)

            system.add_vehicle(obj)
            save_data() # Sauvegarde automatique
            st.success(f"{v_type} ajouté avec succès ! (ID: {new_id})")

# =========================================================
# PAGE 3 : GESTION CLIENTS
# =========================================================
elif menu == "Clients":
    st.title("👥 Gestion Clients")
    
    # Formulaire Ajout
    with st.expander("Nouveau Client", expanded=True):
        c_name = st.text_input("Nom Prénom")
        c_permis = st.text_input("Numéro Permis")
        if st.button("Ajouter Client"):
            cid = len(system.customers) + 1
            new_c = Customer(cid, c_name, c_permis, "email@test.com", "0600")
            system.add_customer(new_c)
            st.success(f"Client {c_name} ajouté !")

    # Liste
    if system.customers:
        st.write("### Liste des Clients")
        for c in system.customers:
            st.text(f"ID {c.id} : {c.name} ({c.driver_license})")
    else:
        st.warning("Aucun client enregistré.")

# =========================================================
# PAGE 4 : COMPTOIR LOCATIONS
# =========================================================
elif menu == "Comptoir Locations":
    st.title("📝 Location & Retour")

    tab1, tab2 = st.tabs(["🔑 Nouvelle Location", "↩️ Retour Véhicule"])

    with tab1:
        if not system.customers or not system.fleet:
            st.error("Il faut des clients et des véhicules pour faire une location.")
        else:
            col1, col2 = st.columns(2)
            
            # Sélecteur de Client
            client_options = {c.name: c.id for c in system.customers}
            c_name = col1.selectbox("Client", list(client_options.keys()))
            
            # Sélecteur de Véhicule (Uniquement les DISPONIBLES)
            avail_fleet = [v for v in system.fleet if v.status == VehicleStatus.AVAILABLE]
            if not avail_fleet:
                st.warning("Aucun véhicule disponible.")
            else:
                v_options = {f"{v.brand if hasattr(v,'brand') else v.name} (#{v.id}) - {v.daily_rate}€/j": v.id for v in avail_fleet}
                v_label = col2.selectbox("Véhicule", list(v_options.keys()))
                
                # Dates
                d_start = col1.date_input("Début", date.today())
                d_end = col2.date_input("Fin", date.today() + timedelta(days=3))

                if st.button("Valider la Location"):
                    cid = client_options[c_name]
                    vid = v_options[v_label]
                    
                    rental = system.create_rental(cid, vid, d_start, d_end)
                    if rental:
                        st.balloons()
                        st.success(f"Location validée ! Total : {rental.total_price}€")
                        save_data() # On sauvegarde le changement de statut du véhicule

    with tab2:
        # Filtrer les locations actives
        active_rentals = [r for r in system.rentals if r.is_active]
        if not active_rentals:
            st.info("Aucune location en cours.")
        else:
            r_opts = {f"Loc #{r.id} - {r.vehicle.brand}/{r.vehicle.name} ({r.customer.name})": r.id for r in active_rentals}
            r_choice = st.selectbox("Choisir la location à clôturer", list(r_opts.keys()))
            
            if st.button("Confirmer le Retour"):
                rid = r_opts[r_choice]
                system.return_vehicle(rid)
                st.success("Véhicule retourné et disponible !")
                save_data() # Sauvegarde le statut disponible