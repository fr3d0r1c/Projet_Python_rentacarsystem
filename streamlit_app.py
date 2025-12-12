import streamlit as st
import pandas as pd
import sys
import os
import requests
import time
import json
import base64
from datetime import date, timedelta, datetime
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# =========================================================
# 1. CONFIGURATION & IMPORTS
# =========================================================

st.set_page_config(
    page_title="Rent-A-Dream", 
    page_icon="🚗", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.join(current_dir, "CarRentalSystem")
if project_folder not in sys.path:
    sys.path.append(project_folder)
    
from location.system import CarRentalSystem
from location.rental import Rental
from storage import StorageManager
from clients.customer import Customer
from fleet.vehicles import *
from fleet.animals import *
from fleet.enums import VehicleStatus, MaintenanceType
from fleet.transport_base import MotorizedVehicle, TransportAnimal, TowedVehicle

# =========================================================
# 2. CONSTANTES & DESIGN
# =========================================================

SOUND_MAP = {
    "Voiture": "voiture",
    "Camion": "camion",      
    "Dragon": "dragon.aiff",        
    "Cheval": "cheval",
    "Âne": "ane",
    "Bateau": "bateau_klaxon",
    "Avion": "avion_decollage",
    "Sous-Marin": "sonar"
}

ADMIN_ACCOUNTS = {
    "admin": "admin123",
    "chef": "chef"
}

PRICE_MAP = {
    "Voiture": 50.0, "Camion": 250.0, "Moto": 90.0, "Corbillard": 300.0, "Karting": 60.0,
    "Cheval": 35.0, "Âne": 25.0, "Chameau": 80.0,
    "Calèche": 120.0, "Charrette": 40.0,
    "Bateau": 400.0, "Sous-Marin": 2000.0, "Baleine": 200.0, "Dauphin": 100.0,
    "Avion": 1500.0, "Hélicoptère": 800.0, "Aigle": 150.0, "Dragon": 5000.0
}

DEFAULT_MAINT_COSTS = {
    MaintenanceType.MECHANICAL_CHECK: 50.0, MaintenanceType.CLEANING: 20.0,
    MaintenanceType.HOOF_CARE: 40.0, MaintenanceType.SADDLE_MAINTENANCE: 15.0,
    MaintenanceType.TIRE_CHANGE: 120.0, MaintenanceType.OIL_CHANGE: 89.0,
    MaintenanceType.AXLE_GREASING: 30.0,
    MaintenanceType.HULL_CLEANING: 500.0,   
    MaintenanceType.SONAR_CHECK: 150.0,     
    MaintenanceType.NUCLEAR_SERVICE: 5000.0,
    MaintenanceType.AVIONICS_CHECK: 300.0,  
    MaintenanceType.ROTOR_INSPECTION: 200.0,
    MaintenanceType.WING_CARE: 60.0,        
    MaintenanceType.SCALE_POLISHING: 100.0  
}

DEFAULT_DURATIONS = {
    MaintenanceType.MECHANICAL_CHECK: 1.0, MaintenanceType.CLEANING: 0.5,
    MaintenanceType.HOOF_CARE: 0.5, MaintenanceType.SADDLE_MAINTENANCE: 2.0,
    MaintenanceType.TIRE_CHANGE: 0.5, MaintenanceType.OIL_CHANGE: 0.5,
    MaintenanceType.AXLE_GREASING: 1.0,
    MaintenanceType.HULL_CLEANING: 3.0,
    MaintenanceType.SONAR_CHECK: 1.0,
    MaintenanceType.NUCLEAR_SERVICE: 15.0,
    MaintenanceType.AVIONICS_CHECK: 2.0,
    MaintenanceType.ROTOR_INSPECTION: 1.0,
    MaintenanceType.WING_CARE: 1.0,
    MaintenanceType.SCALE_POLISHING: 0.5
}

CATALOG = {
    "Voiture": {
        "Peugeot": ["208", "308", "3008", "508"],
        "Renault": ["Clio", "Megane", "Captur", "Austral"],
        "Tesla": ["Model 3", "Model Y", "Model S", "Cybertruck"],
        "Ferrari": ["F8 Tributo", "Roma", "SF90"],
        "Toyota": ["Yaris", "Corolla", "RAV4"]
    },
    "Camion": {
        "Volvo": ["FH16", "FM", "FMX"],
        "Renault Trucks": ["T High", "K Series"],
        "Mercedes-Benz": ["Actros", "Arocs"]
    },
    "Moto": {
        "Yamaha": ["MT-07", "TMAX", "R1"],
        "Harley-Davidson": ["Sportster", "Fat Bob", "Iron 883"],
        "Kawasaki": ["Z900", "Ninja"]
    },
    "Bateau": {
        "Beneteau": ["Oceanis 40", "Flyer 8"],
        "Zodiac": ["Medline", "Pro Open"],
        "Riva": ["Aquarama", "Iseo"]
    },
    "Sous-Marin": {
        "Naval Group": ["Suffren", "Scorpene"],
        "US Navy": ["Virginia Class", "Seawolf"],
        "Comex": ["Remora 2000"]
    },
    "Avion": {
        "Boeing": ["747", "737 MAX", "777"],
        "Airbus": ["A320", "A380", "A350"],
        "Cessna": ["172 Skyhawk", "Citation"]
    },
    "Hélicoptère": {
        "Airbus": ["H160", "H145", "Ecureuil"],
        "Bell": ["206 JetRanger", "429"]
    },
    "Cheval": ["Shetland", "Pur-Sang Arabe", "Frison", "Percheron", "Mustang", "Selle Français"],
    "Âne": ["Âne du Poitou", "Âne de Provence", "Âne des Pyrénées", "Grand Noir du Berry"],
    "Dragon": ["Rouge de Feu", "Noir des Abysses", "Vert des Forêts", "Doré Impérial", "Blanc des Glaces"],
    "Aigle": ["Aigle Royal", "Aigle Géant de Manwë", "Pygargue"],
    "Baleine": ["Baleine Bleue", "Cachalot", "Baleine à Bosse"],
    "Dauphin": ["Grand Dauphin", "Orque", "Dauphin Bleu"]
}

THEMES = {
    "☀️ Clair (Rent-A-Car)": {
        "bg_color": "#F2F5F9",
        "sec_bg_color": "#FFFFFF",
        "text_color": "#1D3557",
        "card_bg": "#FFFFFF",
        "sidebar_text": "#1D3557",
        "border_color": "#D1D5DB",
        "shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
        "accent": "#E63946"
    },
    "🌙 Sombre (Nuit)": {
        "bg_color": "#0E1117",
        "sec_bg_color": "#161920",
        "text_color": "#E6E6E6",
        "card_bg": "#1E2127",
        "sidebar_text": "#FAFAFA",
        "border_color": "#41424C",
        "shadow": "0 4px 6px rgba(0,0,0,0.3)",
        "accent": "#FF4B4B"
    },
    "🔥 Rouge & Noir (Dragon)": {
        "bg_color": "#1A0505",
        "sec_bg_color": "#2D0A0A",
        "text_color": "#FFD700",
        "card_bg": "#3B0000",
        "sidebar_text": "#FFD700",
        "border_color": "#500000",
        "shadow": "0 0 15px rgba(255, 0, 0, 0.3)",
        "accent": "#FF0000"
    }
}

def play_sound(sound_key):
    sound_name = SOUND_MAP.get(sound_key, "Succes")

    sound_file = os.path.join(current_dir, "assets", "sounds", f"{sound_name}.mp3")

    if not os.path.exists(sound_file):
        return
    
    try:
        with open(sound_file, "rb") as f:
            data = f.read()
            b64_val = base64.b64encode(data).decode()

            md = f"""
                <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{b64_val}" type="audio/mp3">
                </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        print(f"Erreur lors de la lecture audio : {e}")

def get_sound_key_by_object(obj):
    class_name = obj.__class__.__name__

    if isinstance(obj, Car): return "Voiture"
    if isinstance(obj, Truck): return "Camion"
    if isinstance(obj, Dragon): return "Dragon"
    if isinstance(obj, Horse): return "Cheval"
    if isinstance(obj, Boat): return "Bateau"

    return "Succes"

def apply_theme(theme_name):

    t_name = st.session_state.get('current_theme', "☀️ Clair")
    if t_name not in THEMES: t_name = "☀️ Clair"

    t = THEMES[theme_name]

    css = f"""
    <style>
        /* FOND ET TEXTE GLOBAL */
        .stApp {{
            background-color: {t['bg_color']};
            color: {t['text_color']};
        }}
        
        /* SIDEBAR */
        section[data-testid="stSidebar"] {{
            background-color: {t['sec_bg_color']};
            border-right: 1px solid {t['border_color']};
        }}
        
        /* TITRES H1, H2, etc. */
        h1, h2, h3, h4, h5, h6 {{
            color: {t['text_color']} !important;
        }}
        
        /* CARTES ET CONTENEURS */
        div[data-testid="stMetric"], div[data-testid="stExpander"], div.stContainer {{
            background-color: {t['card_bg']};
            border-radius: 10px;
            border: 1px solid {t['border_color']};
            box-shadow: {t['shadow']};
        }}
        
        /* ============================================================ */
        /* 👇 C'EST ICI QUE LA MAGIE OPÈRE POUR VOS CHAMPS 👇 */
        /* ============================================================ */

        /* 1. COULEUR DES TITRES (LABELS) AU-DESSUS DES CHAMPS */
        /* On utilise la couleur 'accent' (ex: Rouge) pour les titres, ou 'text_color' (Jaune) */
        div[data-testid="stWidgetLabel"] p, label p {{
            color: {t['accent']} !important;  /* <-- Mettez t['text_color'] si vous préférez du jaune */
            font-weight: 600;
        }}

        /* 2. COULEUR DU TEXTE À L'INTÉRIEUR DES INPUTS */
        .stTextInput input, .stNumberInput input {{
            color: {t['text_color']} !important;
            caret-color: {t['text_color']} !important; /* Curseur qui clignote */
        }}
        
        /* 3. COULEUR DU PLACEHOLDER (Texte gris "Ex: Dragon...") */
        .stTextInput input::placeholder {{
            color: {t['text_color']} !important;
            opacity: 0.6; /* Un peu transparent */
        }}

        /* 4. COULEUR DU TEXTE DANS LES SELECTBOX */
        div[data-baseweb="select"] span {{
            color: {t['text_color']} !important;
        }}
        /* L'icône flèche du selectbox */
        div[data-baseweb="select"] svg {{
            fill: {t['text_color']} !important;
        }}

        /* ============================================================ */

        /* TEXTES DANS LES CARTES (Métriques) */
        div[data-testid="stMetricLabel"] p {{ color: {t['text_color']} !important; opacity: 0.8; }}
        div[data-testid="stMetricValue"] div {{ color: {t['text_color']} !important; }}
        
        /* BOUTONS */
        div.stButton > button {{
            background-color: {t['accent']};
            color: white !important;
            border: none;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def load_lottiefile(filepath: str):
    try:
        with open(filepath, "r", encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: return None

API_URL = "http://127.0.0.1:8000"

def get_all_fleet():
    try:
        response = requests.get(f"{API_URL}/fleet")
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []

def post_rental(customer_id, vehicle_id, start_str, end_str):
    payload = {
        "customer_id": customer_id,
        "vehicle_id": vehicle_id,
        "start_date": start_str,
        "end_date": end_str
    }
    try:
        response = requests.post(f"{API_URL}/rentals/", json=payload)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json()['detail']
    except Exception as e:
        return False, str(e)

# =========================================================
# 3. INITIALISATION SESSION
# =========================================================

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'current_theme' not in st.session_state: st.session_state.current_theme = "🔥 Rouge & Noir (Dragon)"
if 'show_login' not in st.session_state: st.session_state.show_login = False

if 'system' not in st.session_state:
    storage = StorageManager("data.json")
    st.session_state.system = storage.load_system()
    st.session_state.storage = storage
    st.session_state.lottie_cache = {}
    try:
        st.session_state.lottie_cache["Voiture"] = load_lottiefile("assets/car.json")
        st.session_state.lottie_cache["Dragon"] = load_lottiefile("assets/dragon.json")
        st.session_state.lottie_cache["Bateau"] = load_lottiefile("assets/boat.json")
        st.session_state.lottie_cache["Aigle"] = load_lottiefile("assets/eagle.json")
        st.session_state.lottie_cache["Cheval"] = load_lottiefile("assets/horse.json")
        st.session_state.lottie_cache["Camion"] = load_lottiefile("assets/truck.json")
        st.session_state.lottie_cache["Défaut"] = load_lottiefile("assets/default.json")
    except: pass

system = st.session_state.system
storage = st.session_state.storage

def save_data():
    storage.save_system(system)
    st.toast("Synchronisation effectuée.", icon="☁️")
    
# =========================================================
# 4. TOP BAR (CONNEXION)
# =========================================================

apply_theme(st.session_state.current_theme)

c_logo, c_spacer, c_login = st.columns([1, 4, 1.5])
with c_logo:
    logo_path = os.path.join(current_dir, "assets", "images", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        st.error("Logo introuvable")
with c_login:
    if st.session_state.authenticated:
        u_name = "Admin" if st.session_state.user_role == "admin" else st.session_state.current_user.name
        if st.button(f"🔓 Déconnexion ({u_name})"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.current_user = None
            st.session_state.show_login = False
            st.rerun()
    else:
        if st.button("🔒 Se connecter / S'inscrire"):
            st.session_state.show_login = not st.session_state.show_login

if st.session_state.show_login and not st.session_state.authenticated:
    with st.container(border=True):
        tabs_log = st.tabs(["Connexion", "Inscription Client"])

        with tabs_log[0]:
            u = st.text_input("Identifiant")
            p = st.text_input("Mot de passe", type="password")
            if st.button("Entrer", use_container_width=True):

                if u in ADMIN_ACCOUNTS and ADMIN_ACCOUNTS[u] == p:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "admin"
                    st.session_state.show_login = False
                    st.success("Mode Admin activé")
                    time.sleep(0.5); st.rerun()
                else:
                    found = next((c for c in system.customers if c.username == u and c.password == p), None)
                    if found:
                        st.session_state.authenticated = True
                        st.session_state.user_role = "client"
                        st.session_state.current_user = found
                        st.session_state.show_login = False
                        st.success(f"Bienvenue {found.name}")
                        time.sleep(0.5); st.rerun()
                    else:
                        st.error("Inconnu ou mauvais mot de passe.")
                        
        with tabs_log[1]:
            st.caption("Créez votre compte pour louer nos véhicules.")
            
            # --- 1. Informations Personnelles (sur 2 colonnes) ---
            c_perso1, c_perso2 = st.columns(2)
            
            with c_perso1:
                nn = st.text_input("Nom & Prénom *", placeholder="Ex: Jean Dupont")
                n_email = st.text_input("Email *", placeholder="jean@mail.com")
            
            with c_perso2:
                n_phone = st.text_input("Téléphone *", placeholder="06 12 34 56 78")
                nperm = st.text_input("Numéro de Permis", placeholder="B-123456 (Optionnel)")

            st.markdown("---")

            # --- 2. Identifiants de Connexion (sur 2 colonnes) ---
            c_login1, c_login2 = st.columns(2)
            
            with c_login1:
                nu = st.text_input("Choisir Identifiant *", placeholder="jdupont")
            with c_login2:
                np = st.text_input("Choisir Mot de passe *", type="password")

            # --- 3. Validation ---
            if st.button("✨ Créer mon Compte", use_container_width=True, type="primary"):
                # Vérification des champs obligatoires
                if nu and np and nn and n_email and n_phone:
                    
                    # Vérification d'unicité de l'identifiant
                    if any(c.username == nu for c in system.customers):
                        st.error("Cet identifiant est déjà pris. Veuillez en choisir un autre.")
                    
                    else:
                        # Génération ID
                        nid = 1 if not system.customers else max(c.id for c in system.customers) + 1
                        
                        # Création du client avec TOUS les champs
                        new_c = Customer(nid, nn, nperm, n_email, n_phone, nu, np)
                        
                        system.add_customer(new_c)
                        save_data()
                        
                        st.success("✅ Compte créé avec succès ! Connectez-vous dans l'onglet 'Connexion'.")
                        st.balloons()
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs marqués d'une étoile (*).")
# =========================================================
# 5. NAVIGATION & CONTENU (MULTI-ROLES)
# =========================================================

common_opts = ["Accueil", "Catalogue Public"]
common_icons = ["house", "grid"]

if st.session_state.user_role == "admin":
    menu_opts = common_opts + ["Dashboard", "Gestion Flotte", "Atelier", "Base Clients", "Locations Admin"]
    menu_icons = common_icons + ["speedometer2", "car-front", "tools", "people", "clipboard-data"]
    
elif st.session_state.user_role == "client":
    menu_opts = common_opts + ["Louer un véhicule", "Espace Personnel"]
    menu_icons = common_icons + ["cart4", "person-circle"]

else:
    menu_opts = common_opts
    menu_icons = common_icons
    
with st.sidebar:
    st.title("Navigation")
    
    # Gestion redirection (inchangée)
    default_idx = 0
    if 'navigate_to' in st.session_state:
        try: default_idx = menu_opts.index(st.session_state.navigate_to); del st.session_state.navigate_to
        except: pass

    selected = option_menu(
        menu_title=None, options=menu_opts, icons=menu_icons, default_index=default_idx,
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": THEMES[st.session_state.current_theme]['sec_bg_color']
            },
            "icon": {
                "font-size": "18px"
            }, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin":"0px", 
                "color": THEMES[st.session_state.current_theme]['sidebar_text']
            },
            "nav-link-selected": {
                "background-color": THEMES[st.session_state.current_theme]['accent'], 
                "color": "#FFFFFF"
            }
        }
    )
    
    st.markdown("---")
    def change_theme(): st.session_state.current_theme = st.session_state.theme_key
    st.selectbox("Style", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.current_theme), key="theme_key", on_change=change_theme)

# =========================================================
# CONTENU DES PAGES (STRUCTURE APLATIE)
# =========================================================

# --- 1. PAGES COMMUNES (ACCESSIBLES À TOUS) ---

if selected == "Accueil":

    st.title("Rent-A-Dream 🌍")
    st.markdown("### *« De la Fiat Panda au Dragon Rouge, nous louons vos rêves. »*")

    col_pres1, col_pres2 = st.columns([2, 1])

    with col_pres1:
        st.write("""
        Bienvenue dans la première agence de location multiverselle. 
        Notre mission est simple : fournir le moyen de transport adapté à **n'importe quelle situation**, 
        que ce soit pour aller chercher du pain, explorer les abysses ou conquérir un royaume voisin.
        
        **Nos engagements :**
        * 🛡️ **Sécurité** : Nos dragons sont vaccinés et nos freins vérifiés.
        * ⚡ **Rapidité** : Contrats signés en moins de 2 minutes.
        * 🤝 **Diversité** : Terre, Mer, Air... et au-delà.
        """)

    with col_pres2:
        logo_anim = st.session_state.lottie_cache.get("Voiture") or st.session_state.lottie_cache.get("default")
        if logo_anim:
            st_lottie(logo_anim, height=150, key="logo_anim")

    st.markdown("---")

    st.subheader("👥 L'Équipe de Direction")

    team1, team2, team3, team4 = st.columns(4)

    with team1:
        st.image("assets/images/Darwiche.jpg", width=100)
        st.markdown("**Ahmad Darwiche**")
        st.caption("PDG & Fondateur")
    
    with team2:
        st.image("assets/images/exemple.webp", width=100)
        st.markdown("**Maxence PARISSE**")
        st.caption("Conducteur de Calèche/Charette")

    with team3:
        st.image("assets/images/CC.png", width=100)
        st.markdown("**Clémence CHARLES**")
        st.caption("Directrice Vétérinaire & Dresseuse")

    with team4:
        st.image("assets/images/ludovic.jpg", width=100)
        st.markdown("**Ludovic ALLERON**")
        st.caption("Chef de la Sécurité & Responsable Flotte Marine")

elif selected == "Catalogue Public":
    st.title("🚗 Notre Catalogue")
    st.caption("Explorez notre collection unique de véhicules terrestres, marins, aériens et fantastiques.")

    with st.expander("🔍 Filtres & Recherche", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        search = c1.text_input("Recherche textuelle", placeholder="Ex: Dragon, Tesla, Rouge...")

        filter_env = c2.selectbox("Environnement", ["Tous", "Terre", "Mer", "Air"], index=0)
        filter_stat = c3.selectbox("Statut", ["Tous", "Disponible", "Loué", "Maintenance"], index=0)

    filtered_fleet = system.fleet

    if search:
        filtered_fleet = [v for v in filtered_fleet if search.lower() in str(v.show_details()).lower()]

    if filter_env == "Terre":
        filtered_fleet = [v for v in filtered_fleet if isinstance(v, (Car, Truck, Motorcycle, Hearse, GoKart, Horse, Donkey, Camel, Carriage, Cart))]
    elif filter_env == "Mer":
        filtered_fleet = [v for v in filtered_fleet if isinstance(v, (Boat, Submarine, Whale, Dolphin))]
    elif filter_env == "Air":
        filtered_fleet = [v for v in filtered_fleet if isinstance(v, (Plane, Helicopter, Eagle, Dragon))]

    if filter_stat == "Disponible":
        filtered_fleet = [v for v in filtered_fleet if v.status == VehicleStatus.AVAILABLE]
    elif filter_stat == "Loué":
        filtered_fleet = [v for v in filtered_fleet if v.status == VehicleStatus.RENTED]
    elif filter_stat == "Maintenance":
        filtered_fleet = [v for v in filtered_fleet if v.status == VehicleStatus.UNDER_MAINTENANCE]

    st.markdown(f"**{len(filtered_fleet)} véhicules trouvés**")
    st.markdown("---")

    if not filtered_fleet:
        st.info("Aucun véhicule ne correspond à vos critères.")
    else:
        cols = st.columns(3)

        for i, v in enumerate(filtered_fleet):
            with cols[i % 3]:

                img_url = "https://img.icons8.com/color/96/car--v1.png" # Défaut
                if isinstance(v, Dragon): img_url = "https://img.icons8.com/color/96/dragon.png"
                elif isinstance(v, Boat): img_url = "https://img.icons8.com/color/96/yacht.png"
                elif isinstance(v, Submarine): img_url = "https://img.icons8.com/color/96/submarine.png"
                elif isinstance(v, Plane): img_url = "https://img.icons8.com/color/96/airport.png"
                elif isinstance(v, Helicopter): img_url = "https://img.icons8.com/color/96/helicopter.png"
                elif isinstance(v, Horse): img_url = "https://img.icons8.com/color/96/horse.png"
                elif isinstance(v, Donkey): img_url = "https://img.icons8.com/color/96/donkey.png"
                elif isinstance(v, Whale): img_url = "https://img.icons8.com/color/96/whale.png"
                elif isinstance(v, Motorcycle): img_url = "https://img.icons8.com/color/96/motorcycle.png"
                elif isinstance(v, Truck): img_url = "https://img.icons8.com/color/96/truck.png"
                elif isinstance(v, Carriage): img_url = "https://img.icons8.com/color/96/chariot.png"

                if v.status == VehicleStatus.AVAILABLE:
                    badge_html = '<span class="badge badge-green">🟢 DISPONIBLE</span>'
                elif v.status == VehicleStatus.RENTED:
                    badge_html = '<span class="badge badge-yellow">🟡 LOUÉ</span>'
                elif v.status == VehicleStatus.UNDER_MAINTENANCE:
                    badge_html = '<span class="badge badge-red">🔧 MAINTENANCE</span>'
                else:
                    badge_html = '<span class="badge badge-grey">💀 HORS SERVICE</span>'

                titre = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))
                desc = getattr(v, 'model', getattr(v, 'breed', ''))

                specs = ""
                if hasattr(v, 'year'): specs += f"Année {v.year} • "
                elif hasattr(v, 'age'): specs += f"{v.age} ans • "

                if isinstance(v, Car): specs += f"{v.door_count} portes"
                elif isinstance(v, Dragon): specs += f"Feu {v.fire_range}m"
                elif isinstance(v, Submarine): specs += f"-{v.max_depth}m"

                with st.container(border=True):
                    c_img, c_bad = st.columns([1, 2])
                    with c_img: st.image(img_url, width=60)
                    with c_bad: st.markdown(badge_html, unsafe_allow_html=True)

                    st.markdown(f"### {titre}")
                    st.markdown(f"**{desc}**")
                    st.caption(specs)

                    st.markdown("---")

                    c_price, c_btn = st.columns([1, 1])
                    with c_price:
                        st.markdown(f"<div class='price-tag'>{v.daily_rate}€<span class='price-sub'>/j</span></div>", unsafe_allow_html=True)

                    with c_btn:
                        unique_key = f"grid_btn_{v.id}_{i}"

                        if v.status == VehicleStatus.AVAILABLE:
                            if st.button("Réserver", key=unique_key, type="primary"):
                                st.session_state.selected_vehicle_id = v.id
                                st.session_state.navigate_to = "Réservations"
                                st.rerun()
                        else:
                            st.button("Indisponible", key=unique_key, disabled=True)

# --- 2. PAGES CLIENT (SÉCURISÉES) ---

elif selected == "Louer un véhicule":
    if st.session_state.user_role != "client": st.error("Accès réservé aux clients."); st.stop()

    me = st.session_state.current_user
    st.title(f"Nouvelle Réservation pour {me.name}")

    c1, c2 = st.columns([3, 1])
    search = c1.text_input("Recherche...", placeholder="Modèle, Marque...")
    env = c2.selectbox("Filtrer par type", ["Tout", "Terre", "Mer", "Air"])

    available = [v for v in system.fleet if v.status == VehicleStatus.AVAILABLE]

    if env == "Terre": available = [v for v in available if isinstance(v, (Car, Truck, Motorcycle, Horse, Donkey, Carriage, Cart, GoKart, Hearse))]
    elif env == "Mer": available = [v for v in available if isinstance(v, (Boat, Submarine, Whale, Dolphin))]
    elif env == "Air": available = [v for v in available if isinstance(v, (Plane, Helicopter, Dragon, Eagle))]

    if search: available = [v for v in available if search.lower() in str(v.show_details()).lower()]

    if not available:
        st.info("Aucun véhicule disponible correspondant à vos critères.")
    else:
        cols = st.columns(3)
        for i, v in enumerate(available):
            with cols[i%3]:
                with st.container(border=True):
                    nom = getattr(v, 'brand', getattr(v, 'name', '?'))
                    modele = getattr(v, 'model', getattr(v, 'breed', ''))

                    icon = "🚗"
                    if isinstance(v, Dragon): icon = "🐉"
                    elif isinstance(v, Boat): icon = "🚤"
                    elif isinstance(v, Plane): icon = "✈️"
                    
                    st.markdown(f"### {icon} {nom}")
                    st.caption(modele)

                    st.markdown(f"**{v.daily_rate}€ / jour**")

                    with st.popover("📅 Réserver", use_container_width=True):
                        st.markdown(f"**Location de :** {nom} {modele}")

                        d_col1, d_col2 = st.columns(2)
                        d_start = d_col1.date_input("Début", value=date.today(), key=f"start_{v.id}")
                        d_end = d_col2.date_input("Fin", value=date.today() + timedelta(days=1), key=f"end_{v.id}")

                        if d_end >= d_start:
                            days = (d_end - d_start).days
                            days = max(1, days)
                            total_estime = days * v.daily_rate
                            st.info(f"Durée : {days} jours\n\nTotal estimé : **{total_estime}€**")
                        
                        if st.button("Confirmer la réservation", key=f"conf_{v.id}", type="primary"):
                            s_str = d_start.strftime("%Y-%m-%d")
                            e_str = d_end.strftime("%Y-%m-%d")

                            try:
                                # 1. Création via la classe Rental (Validation incluse)
                                new_rental = Rental(me, v, s_str, e_str)
                                
                                # 2. Ajout au système
                                system.rentals.append(new_rental)
                                save_data()

                                type_vehicule = v.__class__.__name__

                                v_class = v.__class__.__name__
                                sound_to_play = "succes"

                                class_to_key = {
                                    "Car": "Voiture", "Truck": "Camion", "Dragon": "Dragon", 
                                    "Horse": "Cheval", "Donkey": "Âne", "Boat": "Bateau",
                                    "Submarine": "Sous-Marin", "Plane": "Avion"
                                }

                                sound_key = get_sound_key_by_object(v)
                                play_sound(sound_to_play)

                                
                                st.success("✅ Réservation validée !")
                                time.sleep(2.5)
                                st.rerun()
                                
                            except ValueError as e:
                                st.error(f"Erreur : {e}")

elif selected == "Espace Personnel":
    if st.session_state.user_role != "client": st.error("Accès réservé."); st.stop()

    me = st.session_state.current_user
    st.title(f"Espace Personnel de {me.name}")

    my_rentals = [r for r in system.rentals if r.customer.id == me.id]
    active_rentals = [r for r in my_rentals if r.is_active]
    history_rentals = [r for r in my_rentals if not r.is_active]
    total_spent = sum(r.total_cost for r in history_rentals)

    tab_active, tab_hist, tab_profile = st.tabs(["🔑 Locations en Cours", "📜 Historique", "⚙️ Mon Profil"])

    with tab_active:
        st.subheader("Véhicules à rendre")

        if not active_rentals:
            st.info("Vous n'avez aucune location en cours. Profitez-en pour louer un Dragon !")
            if st.button("Louer un véhicule maintenant"):
                st.switch_page("streamlit_app.py")
        else:
            for r in active_rentals:
                nom_vehicule = getattr(r.vehicle, 'brand', getattr(r.vehicle, 'name', 'Véhicule'))
                detail_vehicule = getattr(r.vehicle, 'model', getattr(r.vehicle, 'breed', ''))
                
                titre_expander = f"🚗 {nom_vehicule} {detail_vehicule} (Retour prévu : {r.end_date.date()})"

                with st.expander(titre_expander, expanded=True):
                    c1, c2 = st.columns([2, 1])

                    with c1:
                        st.write(f"**Début :** {r.start_date.date()}")
                        st.write(f"**Fin prévue :** {r.end_date.date()}")
                        st.info(f"💰 Coût estimé actuel : **{r.calculate_cost()} €**")

                    with c2:
                        d_return = st.date_input("Date de retour", value=date.today(), key=f"ret_{r.id}")
                        
                        if st.button("Valider le retour", key=f"btn_ret_{r.id}", type="primary"):
                            ret_str = d_return.strftime("%Y-%m-%d")
                            try:
                                final = r.close_rental(ret_str)
                                save_data()
                                st.balloons()
                                st.success(f"Retour confirmé ! Total : {final} €")
                                if r.penalty > 0: 
                                    st.warning(f"Pénalité retard : {r.penalty} €")
                                time.sleep(2)
                                st.rerun()
                            except ValueError as e: 
                                st.error(str(e))
    
    with tab_hist:
        st.subheader("Mes aventures passées")
        c1, c2 = st.columns(2)
        c1.metric("Total Locations", len(history_rentals))
        c2.metric("Budget Total", f"{total_spent} €")

        if not history_rentals:
            st.caption("Aucun historique.")
        else:
            data = []
            for r in history_rentals:
                nom = getattr(r.vehicle, 'brand', getattr(r.vehicle, 'name', '?'))
                model = getattr(r.vehicle, 'model', getattr(r.vehicle, 'breed', ''))

                data.append({
                    "Véhicule": f"{nom} {model}",
                    "Période": f"{r.start_date.date()} -> {r.actual_return_date.date()}",
                    "Coût": f"{r.total_cost} €"
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab_profile:
        st.subheader("Mes Informations")
        
        # On utilise un formulaire pour ne pas recharger la page à chaque lettre tapée
        with st.form("profile_form"):
            col_info, col_img = st.columns([3, 1])
            
            with col_info:
                # Les champs sont pré-remplis avec les infos actuelles (value=me.x)
                # On retire 'disabled=True' pour les rendre modifiables
                new_name = st.text_input("Nom Complet", value=me.name)
                new_email = st.text_input("Email", value=me.email)
                new_phone = st.text_input("Téléphone", value=me.phone)
                new_license = st.text_input("Numéro de Permis", value=me.driver_license)
                
                # L'identifiant reste souvent fixe pour éviter les conflits, on le laisse gris
                st.text_input("Identifiant (Non modifiable)", value=me.username, disabled=True)
            
            with col_img:
                # L'avatar se mettra à jour si le nom change !
                st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={me.name}", width=150)
                st.caption("Votre avatar unique")

            # Bouton de validation du formulaire
            if st.form_submit_button("💾 Enregistrer les modifications", type="primary"):
                # 1. Mise à jour de l'objet Client en mémoire
                me.name = new_name
                me.email = new_email
                me.phone = new_phone
                me.driver_license = new_license
                
                # 2. Sauvegarde dans le fichier JSON
                save_data()
                
                # 3. Feedback et rechargement
                st.success("Profil mis à jour avec succès !")
                time.sleep(1)
                st.rerun() # Force le rafraîchissement pour voir les changements partout

        st.markdown("---")
        st.subheader("Zone de Danger")
        with st.expander("🗑️ Supprimer mon compte", expanded=False):
            st.warning("Cette action est irréversible. Toutes vos données seront effacées.")
            
            if active_rentals:
                st.error("⛔ Impossible de supprimer le compte : Vous avez des locations en cours.")
            else:
                confirm_del = st.checkbox("Je confirme vouloir supprimer mon compte.")
                if st.button("CONFIRMER LA SUPPRESSION", type="primary", disabled=not confirm_del):
                    if me in system.customers:
                        system.customers.remove(me)
                        save_data()
                        
                        st.session_state.authenticated = False
                        st.session_state.user_role = None
                        st.session_state.current_user = None
                        
                        st.success("Compte supprimé. Au revoir !")
                        time.sleep(2)
                        st.rerun()

        
# --- 3. PAGES ADMIN (SÉCURISÉES) ---
elif selected == "Dashboard":
    if st.session_state.user_role != "admin": st.error("Accès Admin requis."); st.stop()
    st.title("📊 Tableau de Bord")
    k1, k2 = st.columns(2)
    k1.metric("CA Total", f"{sum(r.total_price for r in system.rentals)}€")
    k2.metric("Clients", len(system.customers))
    st.markdown("---")
    k3, k4 = st.columns(2)
    with k3:
        st.subheader("🔴 Loués / Indisponibles")
        data_loues = []
        for v in system.fleet:
            if v.status != VehicleStatus.AVAILABLE: # On prend tout ce qui n'est pas dispo
                # 1. Récupération sécurisée du Nom (Marque ou Name)
                nom = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))
                # 2. Récupération sécurisée du Modèle (Model ou Breed)
                modele = getattr(v, 'model', getattr(v, 'breed', ''))
                # 3. Récupération du Type (Nom de la classe)
                v_type = v.__class__.__name__

                data_loues.append({
                    "Type": v_type, 
                    "Véhicule": f"{nom} {modele}"
                })
        if data_loues:
            st.dataframe(pd.DataFrame(data_loues), use_container_width=True, hide_index=True)
        else:
            st.info("Aucun véhicule loué.")

    with k4:
        st.subheader("🟢 Disponibles")
        data_dispo = []
        for v in system.fleet:
            if v.status == VehicleStatus.AVAILABLE:
                # Même logique sécurisée ici
                nom = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))
                modele = getattr(v, 'model', getattr(v, 'breed', ''))
                v_type = v.__class__.__name__

                data_dispo.append({
                    "Type": v_type, 
                    "Véhicule": f"{nom} {modele}"
                })
        if data_dispo:
            st.dataframe(pd.DataFrame(data_dispo), use_container_width=True, hide_index=True)
        else:
            st.warning("Aucun véhicule disponible.")

elif selected == "Gestion Flotte":
    st.title("🚜 Gestion du Parc")

    tab_add, tab_del, tab_harness = st.tabs(["➕ Ajouter", "🗑️ Supprimer", "🐴 Atteler (Attelages)"])

    with tab_add:
        st.subheader("Nouvelle Acquisition")
        st.caption("Sélectionnez l'environnement et le type pour voir les options.")

        col_env, col_type = st.columns(2)
        env = col_env.selectbox("Environnement", ["Terre", "Mer", "Air"], index=0)

        if env == "Terre": 
            type_options = ["Voiture", "Camion", "Moto", "Corbillard", "Karting", "Cheval", "Âne", "Chameau", "Calèche", "Charrette"]
        elif env == "Mer": 
            type_options = ["Bateau", "Sous-Marin", "Baleine", "Dauphin"]
        else: 
            type_options = ["Avion", "Hélicoptère", "Aigle", "Dragon"]

        v_type = col_type.selectbox("Type d'élément", type_options)

        default_price = PRICE_MAP.get(v_type, 50.0)

        st.markdown("---")

        c1, c2 = st.columns(2)

        brand_val, model_val = "", ""

        if v_type in CATALOG and isinstance(CATALOG[v_type], dict):
            brands_list = sorted(list(CATALOG[v_type].keys())) + ["➕ Autre (Manuel)"]

            selected_brand = c1.selectbox(f"Marque ({v_type})", brands_list)

            if selected_brand == "➕ Autre (Manuel)":
                brand_val = c1.text_input("Saisir la marque manuellement")
                model_val = c2.text_input("Saisir le modèle")
            else:
                brand_val = selected_brand
                models_list = sorted(CATALOG[v_type][selected_brand]) + ["➕ Autre (Manuel)"]
                selected_model = c2.selectbox(f"Modèle ({brand_val})", models_list)

                if selected_model == "➕ Autre (Manuel)":
                    model_val = c2.text_input("Saisir le modèle manuellement")
                else:
                    model_val = selected_model

        elif v_type in CATALOG and isinstance(CATALOG[v_type], list):
            brand_val = c1.text_input("Nom de l'animal")

            races_list = sorted(CATALOG[v_type]) + ["➕ Autre (Manuel)"]
            selected_race = c2.selectbox(f"Race / Espèce ({v_type})", races_list)

            if selected_race == "➕ Autre (Manuel)":
                model_val = c2.text_input("Saisir la race")
            else:
                model_val = selected_race

        else:
            if v_type in ["Calèche", "Charrette"]:
                pass
            else:
                lbl_b = "Marque / Constructeur"
                lbl_m = "Modèle"
                brand_val = c1.text_input(lbl_b)
                model_val = c2.text_input(lbl_m)

        rate = st.number_input("Tarif Journalier (€)", value=default_price, step=5.0)

        plate, year, age = "", 2024, 5
        arg_a, arg_b, arg_c = 0, False, ""

        if v_type in ["Voiture", "Camion", "Moto", "Corbillard", "Karting", "Bateau", "Sous-Marin", "Avion", "Hélicoptère"]:
            lbl_id = "Plaque"
            if v_type in ["Bateau", "Sous-Marin"]: lbl_id = "Nom du Vaisseau / Coque"
            if v_type == "Avion": lbl_id = "Immatriculation (F-XXXX)"

            c3, c4 = st.columns(2)
            plate = c3.text_input(lbl_id)
            year = c4.number_input("Année", value=2024, step=1)

            c_spec1, c_spec2 = st.columns(2)

            if v_type == "Voiture":
                arg_a = c_spec1.number_input("Portes", 3, 5, 5)
                arg_b = c_spec2.checkbox("Clim ?", True)
            elif v_type == "Camion":
                arg_a = c_spec1.number_input("Volume (m3)", 20.0)
                arg_c = c_spec2.number_input("Poids (T)", 10.0)
            elif v_type == "Moto":
                arg_a = c_spec1.number_input("Cylindrée", 500)
                arg_b = c_spec2.checkbox("TopCase ?", False)
            elif v_type == "Sous-Marin":
                arg_a = c_spec1.number_input("Profondeur", 500.0)
                arg_b = c_spec2.checkbox("Nucléaire ?", True)
            elif v_type == "Avion":
                arg_a = c_spec1.number_input("Envergure", 15.0)
                arg_c = c_spec2.number_input("Moteurs", 1)
            elif v_type == "Hélicoptère":
                arg_a = c_spec1.number_input("Pales", 2)
                arg_c = c_spec2.number_input("Alt. Max", 3000)
            elif v_type == "Bateau":
                arg_a = c_spec1.number_input("Longueur", 10.0)
                arg_c = c_spec2.number_input("CV", 150.0)
            elif v_type == "Karting":
                arg_c = c_spec1.text_input("Moteur", "4T")
                arg_b = c_spec2.checkbox("Indoor ?", True)
            elif v_type == "Corbillard":
                arg_a = c_spec1.number_input("Longueur (m)", 2.2)
                arg_b = c_spec2.checkbox("Frigo ?", True)

        elif v_type in ["Cheval", "Âne", "Chameau", "Baleine", "Dauphin", "Aigle", "Dragon"]:
            age = st.number_input("Âge", 1, 500, 5)

            c_spec1, c_spec2 = st.columns(2)
            if v_type == "Dragon":
                arg_a = c_spec1.number_input("Portée Feu (m)", 100.0)
                arg_c = c_spec2.text_input("Couleur", "Rouge")
            elif v_type == "Cheval":
                arg_a = c_spec1.number_input("Taille (cm)", 160)
                arg_c = c_spec2.number_input("Fers (mm)", 100)
            elif v_type == "Âne":
                arg_a = c_spec1.number_input("Charge (kg)", 50.0)
                arg_b = c_spec2.checkbox("Têtu ?", True)
            elif v_type == "Chameau":
                arg_a = c_spec1.number_input("Bosses", 1, 2, 2)
                arg_c = c_spec2.number_input("Eau (L)", 100.0)
            elif v_type == "Baleine":
                arg_a = c_spec1.number_input("Poids (T)", 100.0)
                arg_b = c_spec2.checkbox("Chante ?", True)
            elif v_type == "Dauphin":
                arg_a = c_spec1.number_input("Vitesse", 40.0)
                arg_b = c_spec2.checkbox("Tours ?", True)
            elif v_type == "Aigle":
                arg_a = c_spec1.number_input("Envergure (cm)", 220)
                arg_c = c_spec2.number_input("Alt Max", 2000)

        elif v_type in ["Calèche", "Charrette"]:
            seats = st.number_input("Places", 2)
            c_spec1, c_spec2 = st.columns(2)
            if v_type == "Calèche": arg_b = c_spec1.checkbox("Toit ?", True)
            else: arg_a = c_spec1.number_input("Charge Max", 200.0)

        st.markdown("###")

        if st.button("💾 Créer et Ajouter au Parc", type="primary", use_container_width=True):
            new_id = 1 if not system.fleet else max(v.id for v in system.fleet) + 1
            obj = None

            if v_type == "Voiture": obj = Car(new_id, rate, brand_val, model_val, plate, year, int(arg_a), arg_b)
            elif v_type == "Camion": obj = Truck(new_id, rate, brand_val, model_val, plate, year, float(arg_a), float(arg_c))
            elif v_type == "Moto": obj = Motorcycle(new_id, rate, brand_val, model_val, plate, year, int(arg_a), arg_b)
            elif v_type == "Sous-Marin": obj = Submarine(new_id, rate, brand_val, model_val, plate, year, float(arg_a), arg_b)
            elif v_type == "Bateau": obj = Boat(new_id, rate, brand_val, model_val, plate, year, float(arg_a), float(arg_c))
            elif v_type == "Avion": obj = Plane(new_id, rate, brand_val, model_val, plate, year, float(arg_a), int(arg_c))
            elif v_type == "Hélicoptère": obj = Helicopter(new_id, rate, brand_val, model_val, plate, year, int(arg_a), int(arg_c))
            elif v_type == "Corbillard": obj = Hearse(new_id, rate, brand_val, model_val, plate, year, float(arg_a), arg_b)
            elif v_type == "Karting": obj = GoKart(new_id, rate, brand_val, model_val, plate, year, arg_c, arg_b)

            elif v_type == "Cheval": obj = Horse(new_id, rate, brand_val, model_val, age, int(arg_a), int(arg_c), int(arg_c))
            elif v_type == "Dragon": obj = Dragon(new_id, rate, brand_val, model_val, age, float(arg_a), arg_c)
            elif v_type == "Âne": obj = Donkey(new_id, rate, brand_val, model_val, age, float(arg_a), arg_b)
            elif v_type == "Chameau": obj = Camel(new_id, rate, brand_val, model_val, age, int(arg_a), float(arg_c))
            elif v_type == "Baleine": obj = Whale(new_id, rate, brand_val, model_val, age, float(arg_a), arg_b)
            elif v_type == "Dauphin": obj = Dolphin(new_id, rate, brand_val, model_val, age, float(arg_a), arg_b)
            elif v_type == "Aigle": obj = Eagle(new_id, rate, brand_val, model_val, age, int(arg_a), int(arg_c))
            
            elif v_type == "Calèche": obj = Carriage(new_id, rate, int(seats), arg_b)
            elif v_type == "Charrette": obj = Cart(new_id, rate, int(seats), float(arg_a))

            if obj:
                system.add_vehicle(obj)
                save_data()

                sound_key = get_sound_key_by_object(obj)
                play_sound(sound_key)

                st.success(f"✅ **{v_type}** ajouté avec succès !")
                time.sleep(1.5)
                st.rerun()

    with tab_del:
        st.subheader("Retirer un élément du parc")
        if not system.fleet:
            st.info("Le parc est vide.")
        else:
            del_opts = {}
            for v in system.fleet:
                nom = getattr(v, 'brand', getattr(v, 'name', 'Element'))
                label = f"#{v.id} - {nom} ({v.__class__.__name__})"
                del_opts[label] = v
            
            sel_del = st.selectbox("Sélectionner l'élément à supprimer", list(del_opts.keys()))

            if st.button("🗑️ Confirmer la suppression", type="primary"):
                obj_to_del = del_opts[sel_del]
                system.fleet.remove(obj_to_del)
                save_data()
                st.success("Élément retiré du parc.")
                time.sleep(1)
                st.rerun()

    with tab_harness:
        st.subheader("Gestion des Attelages")

        towed_list = [v for v in system.fleet if isinstance(v, TowedVehicle)]
        anim_list = [a for a in system.fleet if isinstance(a, TransportAnimal)]

        if not towed_list:
            st.warning("Aucune Calèche ou Charrette disponible.")
        elif not anim_list:
            st.warning("Aucun animal disponible.")
        else:
            c1, c2 = st.columns(2)

            towed_map = {f"#{v.id} {v.__class__.__name__} ({v.seat_count} pl.)": v for v in towed_list}
            sel_towed = c1.selectbox("Véhicule", list(towed_map.keys()))
            veh_obj = towed_map[sel_towed]

            anim_map = {f"#{a.id} {a.name} ({a.__class__.__name__})": a for a in anim_list}
            sel_anim = c2.selectbox("Animal", list(anim_map.keys()))
            anim_obj = anim_map[sel_anim]

            if st.button("🔗 Lier l'animal"):
                error_msg = None
                if isinstance(veh_obj, Carriage):
                    if not isinstance(anim_obj, Horse) or anim_obj.wither_height < 140:
                        error_msg = "❌ Calèche = Grand Cheval (>140cm) uniquement."
                elif isinstance(veh_obj, Cart):
                    if not isinstance(anim_obj, Donkey):
                        error_msg = "❌ Charrette = Âne uniquement."

                if error_msg:
                    st.error(error_msg)
                else:
                    veh_obj.harness_animal(anim_obj)
                    save_data()
                    st.balloons()
                    st.success(f"✅ {anim_obj.name} attelé !")
                    time.sleep(1)
                    st.rerun()

elif selected == "Atelier":
    if st.session_state.user_role != "admin": st.error("Accès Admin requis."); st.stop()
    st.title("🔧 Atelier & Soins")
    
    tab_new_maint, tab_release, tab_history = st.tabs(["🛠️ Déclarer Intervention", "✅ Fin de Maintenance", "📜 Historique"])

    # --- ONGLET 1 : DÉCLARER UNE MAINTENANCE ---
    with tab_new_maint:
        st.subheader("Nouvelle intervention")
        
        # Filtre : On ne répare pas ce qui est loué
        targets = [v for v in system.fleet if v.status != VehicleStatus.RENTED]
        
        if not targets:
            st.info("Aucun véhicule au garage (tout est loué).")
        else:
            # 1. Sélection du Véhicule
            v_dict = {}
            for v in targets:
                nom = getattr(v, 'brand', getattr(v, 'name', '?'))
                lbl = f"#{v.id} {nom} ({v.status.value})"
                v_dict[lbl] = v.id
            
            sel_v = st.selectbox("Véhicule / Animal concerné", list(v_dict.keys()))
            target_obj = next(v for v in system.fleet if v.id == v_dict[sel_v])

            # 2. LOGIQUE DE FILTRAGE DES TYPES (Le Cerveau)
            options = [MaintenanceType.CLEANING] # Nettoyage dispo pour tous

            # A. ANIMAUX
            if isinstance(target_obj, TransportAnimal):
                if isinstance(target_obj, (Horse, Donkey, Camel)):
                    options.extend([MaintenanceType.HOOF_CARE, MaintenanceType.SADDLE_MAINTENANCE])
                elif isinstance(target_obj, (Eagle, Dragon)):
                    options.append(MaintenanceType.WING_CARE)
                    if isinstance(target_obj, Dragon): options.append(MaintenanceType.SCALE_POLISHING)
                elif isinstance(target_obj, (Whale, Dolphin)):
                    options.append(MaintenanceType.HOOF_CARE) # Checkup santé générique

            # B. MOTEURS
            elif isinstance(target_obj, MotorizedVehicle):
                options.extend([MaintenanceType.MECHANICAL_CHECK, MaintenanceType.OIL_CHANGE])
                
                if isinstance(target_obj, (Car, Truck, Motorcycle, Hearse, GoKart)):
                    options.append(MaintenanceType.TIRE_CHANGE)
                
                elif isinstance(target_obj, (Boat, Submarine)):
                    options.append(MaintenanceType.HULL_CLEANING)
                    if isinstance(target_obj, Submarine):
                        options.extend([MaintenanceType.SONAR_CHECK, MaintenanceType.NUCLEAR_SERVICE])
                
                elif isinstance(target_obj, (Plane, Helicopter)):
                    options.append(MaintenanceType.AVIONICS_CHECK)
                    if isinstance(target_obj, Helicopter):
                        options.append(MaintenanceType.ROTOR_INSPECTION)

            # C. ATTELAGES
            elif isinstance(target_obj, TowedVehicle):
                options.extend([MaintenanceType.AXLE_GREASING, MaintenanceType.TIRE_CHANGE])

            # 3. Formulaire Dynamique
            with st.form("maint_form"):
                c1, c2 = st.columns(2)
                
                # On affiche seulement les options filtrées
                m_types_str = [t.value for t in options]
                type_str = c1.selectbox("Type d'intervention", m_types_str)
                
                # Retrouver l'Enum réel
                real_type = next(t for t in MaintenanceType if t.value == type_str)
                
                # Prix/Durée par défaut (Intelligent)
                def_cost = DEFAULT_MAINT_COSTS.get(real_type, 50.0)
                def_time = int(DEFAULT_DURATIONS.get(real_type, 1.0))
                
                cost = c2.number_input("Coût Estimé (€)", value=def_cost)
                desc = st.text_input("Description / Notes", placeholder="Détails techniques...")
                duration = st.slider("Durée immobilisation (jours)", 0, 30, def_time)
                
                bloque = st.checkbox("🛑 Immobiliser (Statut 'En Maintenance')", value=True)
                
                if st.form_submit_button("Valider Intervention"):
                    m_id = len(target_obj.maintenance_log) + 1
                    new_m = Maintenance(m_id, date.today(), real_type, cost, desc, float(duration))
                    target_obj.add_maintenance(new_m)
                    
                    if bloque:
                        target_obj.status = VehicleStatus.UNDER_MAINTENANCE
                    
                    save_data()
                    st.success(f"Intervention **{type_str}** enregistrée !")
                    time.sleep(1)
                    st.rerun()

    # --- ONGLET 2 : FIN DE MAINTENANCE ---
    with tab_release:
        st.subheader("Remettre en service")
        in_maint = [v for v in system.fleet if v.status == VehicleStatus.UNDER_MAINTENANCE]
        
        if not in_maint:
            st.success("Aucun véhicule bloqué en maintenance. Tout roule ! 🟢")
        else:
            opts = {}
            for v in in_maint:
                nom_affiche = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))

                label = f"#{v.id} {nom_affiche}"
                opts[label] = v

            choice = st.selectbox("Véhicule prêt", list(opts.keys()))

            target_release = opts[choice]
            
            if st.button("✅ Valider la fin des travaux", type="primary"):
                opts[choice].status = VehicleStatus.AVAILABLE
                save_data()
                st.balloons()
                st.success("Véhicule disponible !")
                time.sleep(1)
                st.rerun()

    # --- ONGLET 3 : HISTORIQUE ---
    with tab_history:
        st.subheader("Journal des interventions")
        all_logs = []
        for v in system.fleet:
            v_name = getattr(v, 'brand', getattr(v, 'name', '?'))
            for m in v.maintenance_log:
                all_logs.append({
                    "Date": m.date,
                    "Véhicule": v_name,
                    "Type": m.type.value,
                    "Coût": f"{m.cost}€",
                    "Durée": f"{m.duration}j",
                    "Notes": m.description
                })
        
        if all_logs:
            st.dataframe(pd.DataFrame(all_logs), use_container_width=True)
        else:
            st.info("Aucun historique disponible.")

elif selected == "Base Clients":
    if st.session_state.user_role != "admin": st.error("Accès Admin requis."); st.stop()
    st.title("👥 Base Clients")
    for c in system.customers:
        st.text(f"ID {c.id} : {c.name} ({c.email}) - {c.driver_license}")

elif selected == "Locations Admin":
    if st.session_state.user_role != "admin": st.error("Accès Admin requis."); st.stop()

    st.title("📝 Registre Global des Locations")

    active_count = len([r for r in system.rentals if r.is_active])
    total_rev = sum([r.total_cost for r in system.rentals if not r.is_active])

    k1, k2 = st.columns(2)
    k1.metric("Véhicules loués actuellement", active_count)
    k2.metric("Chiffre d'Affaires (Clôturés)", f"{total_rev} €")

    st.divider()

    if not system.rentals:
        st.info("Aucune donnée de location.")
    else:
        admin_data = []
        for r in system.rentals:
            status_icon = "🟢 En cours" if r.is_active else "🔴 Terminé"

            d_start = r.start_date.date()
            d_end = r.end_date.date()
            d_real = r.actual_return_date.date() if r.actual_return_date else "En attente"

            client_name = r.customer.name if hasattr(r.customer, 'name') else f"ID {r.customer}"
            vehicle_name = f"{r.vehicle.brand} {r.vehicle.model}"

            admin_data.append({
                "Statut": status_icon,
                "Client": client_name,
                "Véhicule": vehicle_name,
                "Début": d_start,
                "Fin Prévue": d_end,
                "Retour Réel": d_real,
                "Montant": f"{r.total_cost} €",
                "Pénalité": f"{r.penalty} €"
            })
        
        st.dataframe(pd.DataFrame(admin_data), use_container_width=True)