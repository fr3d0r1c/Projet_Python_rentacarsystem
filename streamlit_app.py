import streamlit as st
import pandas as pd
import sys
import os
import json
import time
import requests
from streamlit_lottie import st_lottie
from datetime import date, timedelta


# --- 1. CONFIGURATION DU CHEMIN ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.join(current_dir, "CarRentalSystem")
if project_folder not in sys.path:
    sys.path.append(project_folder)

# --- 2. IMPORTS DU PROJET ---
from location.system import CarRentalSystem
from storage import StorageManager
from clients.customer import Customer
# Import de TOUTES les classes
from GestionFlotte.vehicles import *
from GestionFlotte.animals import *
from GestionFlotte.enums import VehicleStatus

# --- 3. PRIX PAR DÉFAUT ---
PRICE_MAP = {
    "Voiture": 50.0, "Camion": 250.0, "Moto": 90.0, "Corbillard": 300.0, "Karting": 60.0,
    "Cheval": 35.0, "Âne": 25.0, "Chameau": 80.0,
    "Calèche": 120.0, "Charrette": 40.0,
    "Bateau": 400.0, "Sous-Marin": 2000.0, "Baleine": 200.0, "Dauphin": 100.0,
    "Avion": 1500.0, "Hélicoptère": 800.0, "Aigle": 150.0, "Dragon": 5000.0
}

# --- 4. SETUP STREAMLIT ---
st.set_page_config(page_title="CarRental Ultime", page_icon="🚗", layout="wide")

if 'system' not in st.session_state:
    # 👇 CORRECTION ICI : On utilise le nouveau fichier et la nouvelle méthode
    storage = StorageManager("data.json")
    st.session_state.system = storage.load_system()
    st.session_state.storage = storage

system = st.session_state.system
storage = st.session_state.storage

def save_data():
    # 👇 CORRECTION ICI : On sauvegarde tout le système
    storage.save_system(system)
    st.toast("Sauvegarde complète effectuée !", icon="💾")

# --- FONCTION POUR CHARGER LES ANIMATIONS LOTTIE ---
def load_lottiefile(filepath: str):
    """Charge un fichier Lottie JSON depuis le disque."""
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- MAPPING DES ANIMATIONS PAR TYPE ---
# ⚠️ C'est ici que vous devez coller les URLs LottieFiles que vous trouvez !
# J'ai mis des exemples pour Voiture, Cheval et Dragon.
ANIMATION_MAP = {
    # T E R R E
    "Voiture": "assets/car.json",
    "Camion": "assets/truck.json",
    "Bateau": "assets/boat.json",
    "Aigle": "assets/eagle.json",
    "Dragon": "assets/dragon.json",
    "Cheval": "assets/horse.json",
    "default": "assets/default.json"
}

# Chargez les animations en mémoire au début (Session State) pour éviter de les retélécharger tout le temps
if 'lottie_cache' not in st.session_state:
    st.session_state.lottie_cache = {}
    for v_type, path in ANIMATION_MAP.items():
        anim_data = load_lottiefile(path)
        if anim_data:
            st.session_state.lottie_cache[v_type] = anim_data

# --- 5. SIDEBAR ---
st.sidebar.header("🌍 Navigation")
menu = st.sidebar.radio("Menu", ["Tableau de Bord", "Gestion Flotte", "Clients", "Locations"])
st.sidebar.info(f"Flotte : {len(system.fleet)} véhicules")

# =========================================================
# PAGE 1 : TABLEAU DE BORD
# =========================================================
if menu == "Tableau de Bord":
    st.title("📊 État de la Flotte")
    
    if not system.fleet:
        st.warning("La flotte est vide.")
    else:
        data = []
        for v in system.fleet:
            s_icon = "🟢"
            if v.status == VehicleStatus.RENTED: s_icon = "🟡"
            elif v.status == VehicleStatus.UNDER_MAINTENANCE: s_icon = "🔧"
            elif v.status == VehicleStatus.OUT_OF_SERVICE: s_icon = "💀"
            
            nom = getattr(v, 'brand', getattr(v, 'name', '?'))
            modele = getattr(v, 'model', getattr(v, 'breed', '-'))
            
            details = "-"
            if isinstance(v, Car): details = f"{v.door_count}p {'❄️' if v.has_ac else ''}"
            elif isinstance(v, Dragon): details = f"Feu {v.fire_range}m"
            elif isinstance(v, Submarine): details = f"-{v.max_depth}m {'☢️' if v.is_nuclear else ''}"
            elif isinstance(v, Horse): details = f"{v.wither_height}cm"
            elif isinstance(v, Carriage): details = f"{v.seat_count}pl (Attelage)"

            data.append({
                "ID": v.id,
                "Type": v.__class__.__name__,
                "Identifiant": nom,
                "Description": modele,
                "Année/Âge": getattr(v, 'year', getattr(v, 'age', '-')),
                "Détails": details,
                "Prix/j": f"{v.daily_rate}€",
                "Statut": f"{s_icon} {v.status.value}"
            })
        
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# =========================================================
# PAGE 2 : AJOUTER UN VÉHICULE
# =========================================================

# =========================================================
# PAGE 2 : GESTION FLOTTE (AJOUT / SUPPRESSION / ATTELAGE)
# =========================================================
elif menu == "Gestion Flotte":
    st.title("🚜 Gestion du Parc")
    
    # Création des 3 onglets
    tab_add, tab_del, tab_harness = st.tabs(["➕ Ajouter", "🗑️ Supprimer", "🐴 Atteler (Attelages)"])

    # ---------------------------------------------------------
    # ONGLET 1 : AJOUTER UN ÉLÉMENT
    # ---------------------------------------------------------
    
    with tab_add:
        st.subheader("Créer un nouveau Véhicule ou Animal")

        nature = st.radio("Nature de l'élément :", ["🏎️ Véhicule / Machine", "🐉 Animal Vivant"], horizontal=True)

        col_env, col_type = st.columns(2)
        env = col_env.selectbox("Environnement", ["Terre", "Mer", "Air"])

        type_options = []

        if nature == "🏎️ Véhicule / Machine":
            if env == "Terre":
                type_options = ["Voiture", "Camion", "Moto", "Corbillard", "Karting", "Calèche", "Charrette"]
            elif env == "Mer":
                type_options = ["Bateau", "Sous-Marin"]
            elif env == "Air":
                type_options = ["Avion", "Hélicoptère"]

        else:
            if env == "Terre":
                type_options = ["Cheval", "Âne", "Chameau"]
            elif env == "Mer":
                type_options = ["Baleine", "Dauphin"]
            elif env == "Air":
                type_options = ["Aigle", "Dragon"]

        v_type = col_type.selectbox("Type précis", type_options)

        default_price = PRICE_MAP.get(v_type, 50.0)

        st.markdown("---")

        with st.form("add_vehicle_form"):
            c1, c2 = st.columns(2)

            rate = c1.number_input("Tarif Journalier (€)", value=default_price, step=5.0)

            if nature == "🏎️ Véhicule / Machine":
                if v_type not in ["Calèche", "Charrette"]:
                    lbl_id = "Plaque d'immatriculation"
                    if v_type in ["Bateau", "Sous-Marin"]: lbl_id = "Nom du Vaisseau / N° Coque"
                    if v_type == "Avion": lbl_id = "Immatriculation (F-XXXX)"
                    if v_type == "Karting": lbl_id = "Numéro de Kart"

                    brand = c1.text_input("Marque / Constructeur")
                    model = c2.text_input("Modèle")
                    plate = c1.text_input(lbl_id)
                    year = c2.number_input("Année de fabrication", value=2023, step=1)

                    st.caption(f"Options : {v_type}")
                    cs1, cs2 = st.columns(2)
                    arg_a = 0; arg_b = False; arg_c = ""

                    if v_type == "Voiture":
                        arg_a = cs1.number_input("Nb Portes", 3, 5, 5)
                        arg_b = cs2.checkbox("Climatisation ?", True)
                    elif v_type == "Camion":
                        arg_a = cs1.number_input("Volume (m3)", value=20.0)
                        arg_c = cs2.number_input("Poids Max (T)", value=10.0)
                    elif v_type == "Moto":
                        arg_a = cs1.number_input("Cylindrée (cc)", value=500)
                        arg_b = cs2.checkbox("TopCase ?", False)
                    elif v_type == "Corbillard":
                        arg_a = cs1.number_input("Long. Cercueil (m)", value=2.2)
                        arg_b = cs2.checkbox("Réfrigéré ?", True)
                    elif v_type == "Karting":
                        arg_c = cs1.text_input("Moteur", "4 Temps")
                        arg_b = cs2.checkbox("Indoor ?", True)
                    elif v_type == "Bateau":
                        arg_a = cs1.number_input("Long. (m)", value=10.0)
                        arg_c = cs2.number_input("Puissance (cv)", value=150.0)
                    elif v_type == "Sous-Marin":
                        arg_a = cs1.number_input("Prof. Max (m)", value=500.0)
                        arg_b = cs2.checkbox("Nucléaire ?", True)
                    elif v_type == "Avion":
                        arg_a = cs1.number_input("Envergure (m)", value=15.0)
                        arg_c = cs2.number_input("Nb Moteurs", 1, 4, 1)
                    elif v_type == "Hélicoptère":
                        arg_a = cs1.number_input("Nb Pales", 2, 6, 4)
                        arg_c = cs2.number_input("Alt. Max (m)", value=3000)

                else:
                    seats = c1.number_input("Nb Places", 1, 10, 2)
                    cs1, cs2 = st.columns(2)
                    arg_a = 0; arg_b = False
                    if v_type == "Calèche": arg_b = cs1.checkbox("Toit ?", True)
                    elif v_type == "Charrette": arg_a = cs1.number_input("Charge Max (kg)", value=200.0)

            else:
                name = c1.text_input("Nom")
                breed = c2.text_input("Race / Espèce")
                age = c1.number_input("Âge (ans)", 1, 500, 5)

                st.caption(f"Options : {v_type}")
                cs1, cs2 = st.columns(2)
                arg_a = 0; arg_b = False; arg_c = 0

                if v_type == "Cheval":
                    arg_a = cs1.number_input("Taille (cm)", value=160)
                    arg_c = cs2.number_input("Fers (mm)", value=100)
                elif v_type == "Âne":
                    arg_a = cs1.number_input("Capacité (kg)", value=50.0)
                    arg_b = cs2.checkbox("Têtu ?", True)
                elif v_type == "Chameau":
                    arg_a = cs1.number_input("Nb Bosses", 1, 2, 2)
                    arg_c = cs2.number_input("Eau (L)", value=100.0)
                elif v_type == "Baleine":
                    arg_a = cs1.number_input("Poids (T)", value=100.0)
                    arg_b = cs2.checkbox("Chante ?", True)
                elif v_type == "Dauphin":
                    arg_a = cs1.number_input("Vitesse (km/h)", value=40.0)
                    arg_b = cs2.checkbox("Tours ?", True)
                elif v_type == "Aigle":
                    arg_a = cs1.number_input("Envergure (cm)", value=220)
                    arg_c = cs2.number_input("Alt. Max (m)", value=2000)
                elif v_type == "Dragon":
                    arg_a = cs1.number_input("Portée Feu (m)", value=100.0)
                    arg_c = cs2.text_input("Couleur", "Rouge")

            submitted = st.form_submit_button("💾 Créer et Sauvegarder")

            if submitted:
                new_id = 1 if not system.fleet else max(v.id for v in system.fleet) + 1
                obj = None

                if v_type == "Voiture": obj = Car(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Camion": obj = Truck(new_id, rate, brand, model, plate, year, arg_a, arg_c)
                elif v_type == "Moto": obj = Motorcycle(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Corbillard": obj = Hearse(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Karting": obj = GoKart(new_id, rate, brand, model, plate, year, arg_c, arg_b)
                elif v_type == "Bateau": obj = Boat(new_id, rate, brand, model, plate, year, arg_a, arg_c)
                elif v_type == "Sous-Marin": obj = Submarine(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Avion": obj = Plane(new_id, rate, brand, model, plate, year, arg_a, int(arg_c))
                elif v_type == "Hélicoptère": obj = Helicopter(new_id, rate, brand, model, plate, year, int(arg_a), int(arg_c))

                elif v_type == "Cheval": obj = Horse(new_id, rate, name, breed, age, arg_a, arg_c, arg_c)
                elif v_type == "Âne": obj = Donkey(new_id, rate, name, breed, age, arg_a, arg_b)
                elif v_type == "Chameau": obj = Camel(new_id, rate, name, breed, age, arg_a, arg_c)
                elif v_type == "Baleine": obj = Whale(new_id, rate, name, breed, age, arg_a, arg_b)
                elif v_type == "Dauphin": obj = Dolphin(new_id, rate, name, breed, age, arg_a, arg_b)
                elif v_type == "Aigle": obj = Eagle(new_id, rate, name, breed, age, arg_a, int(arg_c))
                elif v_type == "Dragon": obj = Dragon(new_id, rate, name, breed, age, arg_a, arg_c)

                elif v_type == "Calèche": obj = Carriage(new_id, rate, seats, arg_b)
                elif v_type == "Charrette": obj = Cart(new_id, rate, seats, arg_a)

                if obj:
                    system.add_vehicle(obj)
                    save_data()

                    lottie_json = st.session_state.lottie_cache.get(v_type)
                    if not lottie_json:
                        lottie_json = st.session_state.lottie_cache.get("default")

                    st.success(f"✅ {v_type} ajouté avec succès ! (ID: {new_id})")

                    if lottie_json:
                        st_lottie(lottie_json, height=250, key=f"anim_add_{new_id}")
                        time.sleep(3)
                    st.rerun()

    # ---------------------------------------------------------
    # ONGLET 2 : SUPPRIMER UN ÉLÉMENT
    # ---------------------------------------------------------
    with tab_del:
        st.subheader("Retirer un élément du parc")
        
        if not system.fleet:
            st.info("La flotte est vide, rien à supprimer.")
        else:
            # Création d'une liste lisible pour le selectbox
            del_opts = {}
            for v in system.fleet:
                nom = getattr(v, 'brand', getattr(v, 'name', 'Element'))
                # Petit aperçu pour être sûr de ce qu'on supprime
                label = f"#{v.id} - {nom} ({v.__class__.__name__}) - {v.daily_rate}€/j"
                del_opts[label] = v

            sel_del = st.selectbox("Sélectionner l'élément à supprimer", list(del_opts.keys()))
            
            # Bouton de confirmation
            if st.button("🗑️ Confirmer la suppression définitive", type="primary"):
                obj_to_del = del_opts[sel_del]
                system.fleet.remove(obj_to_del)
                save_data()
                st.success("Élément supprimé avec succès !")
                st.rerun()

    # ---------------------------------------------------------
    # ONGLET 3 : ATTELER (LIER ANIMAL ET VÉHICULE)
    # ---------------------------------------------------------
    with tab_harness:
        st.subheader("Atteler un animal à un véhicule tracté")
        
        col_left, col_right = st.columns(2)
        
        # 1. Filtre Véhicules Tractés (Gauche)
        towed_list = [v for v in system.fleet if isinstance(v, TowedVehicle)]
        
        # 2. Filtre Animaux (Droite)
        anim_list = [a for a in system.fleet if isinstance(a, TransportAnimal)]
        
        if not towed_list:
            st.warning("Aucune Calèche ou Charrette disponible. Veuillez en créer une.")
        elif not anim_list:
            st.warning("Aucun animal disponible. Veuillez en créer un.")
        else:
            # Select Véhicule
            towed_map = {f"#{v.id} {v.__class__.__name__} ({v.seat_count} pl.)": v for v in towed_list}
            sel_towed = col_left.selectbox("Choisir le Véhicule", list(towed_map.keys()))
            veh_obj = towed_map[sel_towed]
            
            # Select Animal
            anim_map = {f"#{a.id} {a.name} ({a.__class__.__name__})": a for a in anim_list}
            sel_anim = col_right.selectbox("Choisir l'Animal", list(anim_map.keys()))
            anim_obj = anim_map[sel_anim]
            
            st.info(f"Action : Atteler **{anim_obj.name}** à **{veh_obj.__class__.__name__} #{veh_obj.id}**")
            
            if st.button("🔗 Lier l'animal"):
                # Vérification manuelle des règles métier pour afficher une belle erreur
                error_msg = None
                
                # Règle Calèche
                if isinstance(veh_obj, Carriage):
                    if not isinstance(anim_obj, Horse) or anim_obj.wither_height < 140:
                        error_msg = "❌ Règle violée : Une Calèche ne peut être tirée que par un Grand Cheval (>140cm)."
                
                # Règle Charrette
                elif isinstance(veh_obj, Cart):
                    if not isinstance(anim_obj, Donkey):
                        error_msg = "❌ Règle violée : Une Charrette ne peut être tirée que par un Âne."
                
                if error_msg:
                    st.error(error_msg)
                else:
                    # Tout est bon, on effectue l'attelage
                    veh_obj.harness_animal(anim_obj)
                    save_data()
                    st.balloons()
                    st.success(f"✅ Succès ! {anim_obj.name} a été attelé.")
                    st.rerun()

# =========================================================
# PAGE 3 : GESTION CLIENTS
# =========================================================
elif menu == "Clients":
    st.title("👥 Gestion Clients")
    
    tab_create, tab_list = st.tabs(["🆕 Création", "📋 Liste"])

    with tab_create:
        with st.form("client_form"):
            c1, c2 = st.columns(2)
            nom = c1.text_input("Nom Prénom")
            permis = c2.text_input("Numéro Permis")
            email = c1.text_input("Email")
            phone = c2.text_input("Téléphone")
            
            if st.form_submit_button("Ajouter Client"):
                if nom and permis:
                    cid = 1 if not system.customers else max(c.id for c in system.customers) + 1
                    new_c = Customer(cid, nom, permis, email, phone)
                    system.add_customer(new_c)
                    save_data() # Sauvegarde immédiate
                    st.success("Client ajouté !")
                else:
                    st.error("Nom et Permis requis.")

    with tab_list:
        if system.customers:
            data_c = [{"ID": c.id, "Nom": c.name, "Permis": c.driver_license, "Email": c.email} for c in system.customers]
            st.dataframe(pd.DataFrame(data_c), use_container_width=True)
        else:
            st.info("Aucun client.")

# =========================================================
# PAGE 4 : COMPTOIR LOCATIONS
# =========================================================
elif menu == "Locations":
    st.title("📝 Comptoir Locations")

    tab_rent, tab_return = st.tabs(["🔑 Nouvelle Location", "↩️ Retour Véhicule"])

    with tab_rent:
        # Filtre : Véhicules disponibles uniquement
        dispos = [v for v in system.fleet if v.status == VehicleStatus.AVAILABLE]
        
        if not dispos:
            st.warning("Aucun véhicule disponible.")
        elif not system.customers:
            st.warning("Aucun client enregistré.")
        else:
            with st.form("rent_form"):
                col1, col2 = st.columns(2)
                
                # Sélection Client
                client_map = {f"{c.name} (Permis: {c.driver_license})": c.id for c in system.customers}
                c_label = col1.selectbox("Client", list(client_map.keys()))
                
                # Sélection Véhicule
                veh_map = {}
                for v in dispos:
                    nom = getattr(v, 'brand', getattr(v, 'name', 'Véhicule'))
                    modele = getattr(v, 'model', getattr(v, 'breed', ''))
                    label = f"#{v.id} - {nom} {modele} ({v.daily_rate}€/j)"
                    veh_map[label] = v.id
                
                v_label = col2.selectbox("Véhicule à louer", list(veh_map.keys()))
                
                # Dates
                d_col1, d_col2 = st.columns(2)
                start_d = d_col1.date_input("Début", date.today())
                days = d_col2.number_input("Durée (jours)", min_value=1, value=3)
                
                if st.form_submit_button("Valider la Location"):
                    cid = client_map[c_label]
                    vid = veh_map[v_label]
                    end_d = start_d + timedelta(days=days)
                    
                    rental = system.create_rental(cid, vid, start_d, end_d)
                    if rental:
                        save_data()
                        st.balloons()
                        st.success(f"Location validée ! Total : **{rental.total_price}€**")
                        st.rerun()

    with tab_return:
        active_rentals = [r for r in system.rentals if r.is_active]
        if not active_rentals:
            st.info("Aucune location en cours.")
        else:
            rental_opts = {}
            for r in active_rentals:
                v = r.vehicle
                nom_vehicule = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))
                label = f"Contrat #{r.id} | {r.customer.name} ➡️ {nom_vehicule}"
                rental_opts[label] = r.id
            
            selected_rental_label = st.selectbox("Sélectionner le contrat à terminer", list(rental_opts.keys()))
            
            if st.button("Confirmer le Retour", type="primary"):
                rid = rental_opts[selected_rental_label]
                system.return_vehicle(rid)
                save_data()
                st.success("Véhicule retourné avec succès !")
                st.rerun()