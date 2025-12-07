import streamlit as st
import pandas as pd
import sys
import os
import time
import json
from datetime import date, timedelta
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION DU CHEMIN ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_folder = os.path.join(current_dir, "CarRentalSystem")
if project_folder not in sys.path:
    sys.path.append(project_folder)

# --- 2. IMPORTS DU PROJET ---
from location.system import CarRentalSystem
from storage import StorageManager
from clients.customer import Customer
from GestionFlotte.vehicles import *
from GestionFlotte.animals import *
from GestionFlotte.enums import MaintenanceType, VehicleStatus
from GestionFlotte.maintenance import Maintenance


# --- 3. PRIX PAR DÉFAUT ---
PRICE_MAP = {
    "Voiture": 50.0, "Camion": 250.0, "Moto": 90.0, "Corbillard": 300.0, "Karting": 60.0,
    "Cheval": 35.0, "Âne": 25.0, "Chameau": 80.0,
    "Calèche": 120.0, "Charrette": 40.0,
    "Bateau": 400.0, "Sous-Marin": 2000.0, "Baleine": 200.0, "Dauphin": 100.0,
    "Avion": 1500.0, "Hélicoptère": 800.0, "Aigle": 150.0, "Dragon": 5000.0
}

DEFAULT_MAINT_COSTS = {
    # Basiques
    MaintenanceType.MECHANICAL_CHECK: 50.0, MaintenanceType.CLEANING: 20.0,
    MaintenanceType.HOOF_CARE: 40.0, MaintenanceType.SADDLE_MAINTENANCE: 15.0,
    MaintenanceType.TIRE_CHANGE: 120.0, MaintenanceType.OIL_CHANGE: 89.0,
    MaintenanceType.AXLE_GREASING: 30.0,
    # Spécifiques (MER / AIR / FANTASY)
    MaintenanceType.HULL_CLEANING: 500.0,    # Bateau
    MaintenanceType.SONAR_CHECK: 150.0,      # Sous-marin
    MaintenanceType.NUCLEAR_SERVICE: 5000.0, # Sous-marin
    MaintenanceType.AVIONICS_CHECK: 300.0,   # Avion
    MaintenanceType.ROTOR_INSPECTION: 200.0, # Hélico
    MaintenanceType.WING_CARE: 60.0,         # Aigle/Dragon
    MaintenanceType.SCALE_POLISHING: 100.0   # Dragon
}

DEFAULT_DURATIONS = {
    # Basiques
    MaintenanceType.MECHANICAL_CHECK: 1.0, MaintenanceType.CLEANING: 0.5,
    MaintenanceType.HOOF_CARE: 0.5, MaintenanceType.SADDLE_MAINTENANCE: 2.0,
    MaintenanceType.TIRE_CHANGE: 0.5, MaintenanceType.OIL_CHANGE: 0.5,
    MaintenanceType.AXLE_GREASING: 1.0,
    # Spécifiques
    MaintenanceType.HULL_CLEANING: 3.0,
    MaintenanceType.SONAR_CHECK: 1.0,
    MaintenanceType.NUCLEAR_SERVICE: 15.0,
    MaintenanceType.AVIONICS_CHECK: 2.0,
    MaintenanceType.ROTOR_INSPECTION: 1.0,
    MaintenanceType.WING_CARE: 1.0,
    MaintenanceType.SCALE_POLISHING: 0.5
}

# --- 4. SETUP STREAMLIT ---
st.set_page_config(page_title="Rent-A-Dream", page_icon="🚗", layout="wide", initial_sidebar_state="expanded")

if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "☀️ Clair (Rent-A-Car)"

THEMES = {
    "☀️ Clair (Rent-A-Car)": {
        "bg_color": "#F2F5F9",
        "sec_bg_color": "#FFFFFF",
        "text_color": "#1D3557",
        "card_bg": "#FFFFFF",
        "sidebar_text": "#1D3557",
        "border_color": "#D1D5DB",
        "shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
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
        "sidebar_text": "#FF4444",
        "border_color": "#500000",
        "shadow": "0 0 15px rgba(255, 0, 0, 0.3)",
        "accent": "#FF0000"
    }
}

def apply_theme(theme_name):
    t = THEMES[theme_name]

    css = f"""
    <style>
        /* --- GLOBAL --- */
        .stApp {{
            background-color: {t['bg_color']};
            color: {t['text_color']};
        }}
        
        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {{
            background-color: {t['sec_bg_color']};
            border-right: 1px solid {t['border_color']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {t['sidebar_text']} !important;
        }}

        /* --- TITRES --- */
        h1, h2, h3, h4 {{
            color: {t['text_color']} !important;
            font-family: 'Helvetica Neue', sans-serif;
        }}

        /* ============================================= */
        /* ZONE CRITIQUE : STYLES GÉNÉRAUX INPUTS     */
        /* ============================================= */
        
        /* Champs Texte & Nombre */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input {{
            background-color: {t['card_bg']} !important;
            color: {t['text_color']} !important;
            border: 1px solid {t['border_color']} !important;
            border-radius: 8px;
        }}

        /* Menus Déroulants (Fermés) */
        div[data-baseweb="select"] > div {{
            background-color: {t['card_bg']} !important;
            color: {t['text_color']} !important;
            border: 1px solid {t['border_color']} !important;
            border-radius: 8px;
        }}
        div[data-baseweb="select"] span {{
            color: {t['text_color']} !important;
        }}
        div[data-baseweb="select"] svg {{
            fill: {t['text_color']} !important;
        }}

        /* Labels Généraux */
        div[data-testid="stWidgetLabel"] p, label p {{
            color: {t['text_color']} !important;
            font-weight: 600;
        }}

        /* ============================================= */
        /* CORRECTIF SPÉCIAL : EXPANDER (FILTRES)     */
        /* ============================================= */

        /* 1. Le conteneur global de l'expander */
        div[data-testid="stExpander"] {{
            background-color: {t['card_bg']} !important;
            border: 1px solid {t['border_color']} !important;
            border-radius: 8px;
            color: {t['text_color']} !important;
        }}

        /* 2. Le titre cliquable ("Filtres & Recherche") */
        div[data-testid="stExpander"] summary p {{
            color: {t['text_color']} !important;
            font-weight: 700;
        }}
        div[data-testid="stExpander"] summary svg {{
            fill: {t['text_color']} !important;
        }}

        /* 3. LES LABELS À L'INTÉRIEUR ("Recherche textuelle", "Environnement") */
        /* On force la couleur pour tout texte <p> dans un widget label DANS un expander */
        div[data-testid="stExpander"] div[data-testid="stWidgetLabel"] p {{
            color: {t['text_color']} !important;
            font-weight: 600;
            opacity: 1 !important;
        }}

        /* 4. LE PLACEHOLDER ("Ex: Dragon...") */
        /* C'est souvent lui qui est invisible (blanc sur blanc) */
        div[data-testid="stExpander"] input::placeholder {{
            color: {t['text_color']} !important;
            opacity: 0.6 !important;
            -webkit-text-fill-color: {t['text_color']} !important; /* Force pour Chrome/Safari */
        }}
        
        /* 5. LE TEXTE TAPÉ DANS L'INPUT DANS L'EXPANDER */
        div[data-testid="stExpander"] input {{
            color: {t['text_color']} !important;
        }}

        /* ============================================= */
        /* CORRECTIF MENU DÉROULANT            */
        /* ============================================= */
        
        /* Liste des options (Popup) */
        ul[data-testid="stSelectboxVirtualDropdown"] {{
            background-color: {t['card_bg']} !important;
        }}
        li[role="option"] {{
            background-color: {t['card_bg']} !important;
            color: {t['text_color']} !important;
        }}
        li[role="option"] span {{
            color: {t['text_color']} !important;
        }}
        /* Survol */
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {{
            background-color: {t['sec_bg_color']} !important;
            color: {t['accent']} !important;
        }}
        li[role="option"]:hover span {{
            color: {t['accent']} !important;
        }}

        /* --- AUTRES ELEMENTS --- */
        div[data-testid="stMetric"], div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            background-color: {t['card_bg']};
            border: 1px solid {t['border_color']};
            box-shadow: {t['shadow']};
        }}
        div[data-testid="stMetricLabel"] p {{ color: {t['text_color']}; opacity: 0.7; }}
        div[data-testid="stMetricValue"] div {{ color: {t['text_color']}; }}
        
        /* Tabs */
        button[data-baseweb="tab"] {{ background-color: transparent !important; color: {t['text_color']} !important; }}
        button[data-baseweb="tab"][aria-selected="true"] {{ color: {t['accent']} !important; border-bottom-color: {t['accent']} !important; }}
        
        /* Boutons */
        div.stButton > button {{ background-color: {t['accent']}; color: #FFFFFF !important; border-radius: 8px; border: none; font-weight: bold; }}
        
        .client-avatar {{ border: 3px solid {t['accent']}; }}
        .price-tag {{ color: {t['text_color']}; }}
        .badge {{ padding: 4px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; display: inline-block; margin-bottom: 8px; }}
        .badge-green {{ background-color: #D4EDDA; color: #155724; border: 1px solid #C3E6CB; }}
        .badge-yellow {{ background-color: #FFF3CD; color: #856404; border: 1px solid #FFEEBA; }}
        .badge-red {{ background-color: #F8D7DA; color: #721C24; border: 1px solid #F5C6CB; }}
        .badge-grey {{ background-color: #E2E3E5; color: #383D41; border: 1px solid #D6D8DB; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

if 'system' not in st.session_state:
    storage = StorageManager("data.json")
    st.session_state.system = storage.load_system()
    st.session_state.storage = storage

    st.session_state.lottie_cache = {}
    try:
        with open("assets/car.json") as f: st.session_state.lottie_cache["Voiture"] = json.load(f)
        with open("assets/truck.json") as f: st.session_state.lottie_cache["Camion"] = json.load(f)
        with open("assets/boat.json") as f: st.session_state.lottie_cache["Bateau"] = json.load(f)
        with open("assets/eagle.json") as f: st.session_state.lottie_cache["Aigle"] = json.load(f)
        with open("assets/dragon.json") as f: st.session_state.lottie_cache["Dragon"] = json.load(f)
        with open("assets/horse.json") as f: st.session_state.lottie_cache["Cheval"] = json.load(f)
        with open("assets/default.json") as f: st.session_state.lottie_cache["default"] = json.load(f)
    except: pass

system = st.session_state.system
storage = st.session_state.storage

def save_data():
    storage.save_system(system)
    st.toast("Données synchronisées.", icon="☁️")

with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/car.png", width=150)
    st.title("Rent-A-Dream")
    st.caption("La location sans limites.")

    st.markdown("---")

    current_theme = st.session_state.get('current_theme', "☀️ Clair (Rent-A-Car)")
    t = THEMES[current_theme]

    default_idx = 0
    if 'navigate_to' in st.session_state:
        pages_map = {"Accueil":0, "Notre Flotte":1, "Clients":2, "Réservations":3, "Atelier":4, "Administration":5}
        default_idx = pages_map.get(st.session_state.navigate_to, 0)
        del st.session_state.navigate_to

    selected = option_menu(
        menu_title=None,
        options=["Accueil", "Notre Flotte", "Clients", "Réservations", "Atelier", "Administration"],
        icons=["house", "grid", "people", "calendar-check", "tools", "gear"],
        menu_icon="cast",
        default_index=default_idx,
        styles={
            "container": {
                "padding": "0!important", 
                "background-color": t['sec_bg_color']
            },
            "icon": {
                "color": t['accent'], 
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "color": t['sidebar_text'],
                "--hover-color": t['card_bg']
            },
            "nav-link-selected": {
                "background-color": t['accent'], 
                "color": "#FFFFFF"
            },
        }
    )

    st.markdown("---")
    st.write("🎨 **Apparence**")

    def change_theme():
        st.session_state.current_theme = st.session_state.theme_key

    theme_choice = st.selectbox(
        "Style", 
        list(THEMES.keys()), 
        index=list(THEMES.keys()).index(current_theme),
        key="theme_key",
        on_change=change_theme,
        label_visibility="collapsed"
    )

    apply_theme(current_theme)

# =========================================================
# PAGE : ACCUEIL (Hero Section)
# =========================================================

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

    team1, team2, team3 = st.columns(3)

    with team1:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Maxence", width=100)
        st.markdown("**Maxence PARISSE**")
        st.caption("PDG & Fondateur")

    with team3:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Clémence", width=100)
        st.markdown("**Clémence CHARLES**")
        st.caption("Directeur Vétérinaire")

    with team2:
        st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Frédéric", width=100)
        st.markdown("**Frédéric ALLERON**")
        st.caption("Cheffe de la Sécurité & Responsable Flotte Marine")

    st.markdown("---")

    st.markdown("### 📈 Performance en temps réel")
    st.info("Voici les indicateurs en temps réel de votre agence.")

    total_revenue = sum(r.total_price for r in system.rentals)
    nb_maintenance = len([v for v in system.fleet if v.status == VehicleStatus.UNDER_MAINTENANCE])

    total_fleet = len(system.fleet)
    occupancy_rate = 0
    if total_fleet > 0:
        nb_rented = len([v for v in system.fleet if v.status == VehicleStatus.RENTED])
        occupancy_rate = nb_rented / total_fleet

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(label="💰 Chiffre d'Affaires", value=f"{total_revenue}€", delta="Cumul")
    
    with k2:
        st.metric(label="📊 Taux d'Occupation", value=f"{occupancy_rate*100:.1f}%", delta=f"{len(system.rentals)} contrats total")
        st.progress(occupancy_rate)

    with k3:
        delta_m = "- Danger" if nb_maintenance > 0 else "OK"
        color_m = "inverse" if nb_maintenance > 0 else "normal"
        st.metric(label="🔧 En Maintenance", value=str(nb_maintenance), delta=delta_m, delta_color=color_m)

        
    with k4:
        st.metric(label="👥 Base Clients", value=str(len(system.customers)), delta="Actifs")

    st.markdown("---")

    c_chart1, c_chart2 = st.columns(2)

    with c_chart1:
        st.markdown("**Répartition de la Flotte**")
        if system.fleet:
            type_counts = {}
            for v in system.fleet:
                t_name = v.__class__.__name__
                type_counts[t_name] = type_counts.get(t_name, 0) + 1
            st.bar_chart(pd.DataFrame(list(type_counts.items()), columns=["Type", "Nombre"]).set_index("Type"), color="#457B9D")
        else:
            st.warning("Pas assez de données.")

    with c_chart2:
        st.markdown("**État de Santé du Parc**")
        if system.fleet:
            status_counts = {"Dispo": 0, "Loué": 0, "Maintenance": 0, "HS": 0}
            for v in system.fleet:
                if v.status == VehicleStatus.AVAILABLE: status_counts["Dispo"] += 1
                elif v.status == VehicleStatus.RENTED: status_counts["Loué"] += 1
                elif v.status == VehicleStatus.UNDER_MAINTENANCE: status_counts["Maintenance"] += 1
                else: status_counts["HS"] += 1
            st.bar_chart(pd.DataFrame(list(status_counts.items()), columns=["Statut", "Nombre"]).set_index("Statut"), color="#E63946")
        else:
            st.warning("Pas assez de données.")

# =========================================================
# PAGE : NOTRE FLOTTE (Catalogue)
# =========================================================

elif selected == "Notre Flotte":
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
# =========================================================
# PAGE : RÉSERVATIONS (Anciennement Locations)
# =========================================================
elif selected == "Réservations":
    st.title("📝 Comptoir de Réservation")
    
    tab_new, tab_return = st.tabs(["Nouvelle Location", "Retour Véhicule"])
    
    with tab_new:
        if not system.customers:
            st.error("Veuillez d'abord créer un client dans l'onglet 'Clients'.")
        else:
            c1, c2 = st.columns(2)
            
            # Sélection Client
            client_dict = {f"{c.name}": c.id for c in system.customers}
            c_name = c1.selectbox("Client", list(client_dict.keys()))
            
            # Sélection Véhicule (Pré-sélection si clic depuis le catalogue)
            avail = [v for v in system.fleet if v.status == VehicleStatus.AVAILABLE]

            if avail:
                veh_dict = {}
                for v in avail:
                    nom_principal = getattr(v, 'brand', None) or getattr(v, 'name', 'Véhicule')
                    modele_secondaire = getattr(v, 'model', getattr(v, 'breed', ''))

                    label = f"#{v.id} - {nom_principal} {modele_secondaire} ({v.daily_rate}€/j)"
                    veh_dict[label] = v.id

                
                default_idx = 0
                if 'selected_vehicle_id' in st.session_state:
                    for idx, vid in enumerate(veh_dict.values()):
                        if vid == st.session_state.selected_vehicle_id:
                            default_idx = idx
                            break
                
                v_label = c2.selectbox("Véhicule", list(veh_dict.keys()), index=default_idx)
                
                days = st.slider("Durée (jours)", 1, 30, 3)
                
                if st.button("Valider le contrat", type="primary"):
                    cid = client_dict[c_name]
                    vid = veh_dict[v_label]
                    rental = system.create_rental(cid, vid, date.today(), date.today()+timedelta(days=days))
                    if rental:
                        save_data()
                        st.balloons()
                        st.success(f"Contrat signé ! Montant : {rental.total_price}€")
                        if 'selected_vehicle_id' in st.session_state: del st.session_state.selected_vehicle_id
                        time.sleep(1)
                        st.rerun()
            else:
                st.warning("Aucun véhicule disponible.")

    with tab_return:
        actives = [r for r in system.rentals if r.is_active]
        if not actives:
            st.info("Aucun retour en attente.")
        else:
            r_opts = {}
            for r in actives:
                v = r.vehicle
                nom_v = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))
                r_opts[f"Contrat #{r.id} ({r.customer.name}) -> {nom_v}"] = r.id

            choice = st.selectbox("Sélectionner contrat", list(r_opts.keys()))
            if st.button("Confirmer le retour"):
                system.return_vehicle(r_opts[choice])
                save_data()
                st.success("Retour effectué.")
                time.sleep(1)
                st.rerun()

# =========================================================
# PAGE : GESTION CLIENTS
# =========================================================

elif selected == "Clients":
    st.title("👥 Base Clients & CRM")
    
    # Navigation interne par Onglets
    tab_list, tab_create, tab_edit, tab_history = st.tabs([
        "📇 Annuaire", "➕ Nouveau Client", "✏️ Modifier / Supprimer", "📜 Historique Locations"
    ])

    # -----------------------------------------------------
    # ONGLET 1 : ANNUAIRE (CARTES DE VISITE)
    # -----------------------------------------------------
    with tab_list:
        search_q = st.text_input("🔍 Rechercher un client (Nom, Permis, Email)...")
        
        # Filtrage
        filtered_clients = system.customers
        if search_q:
            q = search_q.lower()
            filtered_clients = [c for c in system.customers if q in c.name.lower() or q in c.driver_license.lower()]

        st.caption(f"{len(filtered_clients)} clients trouvés")
        st.markdown("---")

        if not filtered_clients:
            st.info("Aucun client trouvé. Utilisez l'onglet 'Nouveau Client'.")
        else:
            cols = st.columns(3)
            for i, c in enumerate(filtered_clients):
                with cols[i % 3]:
                    with st.container(border=True):
                        safe_name = c.name.replace(" ", "%20")
                        avatar_url = f"https://api.dicebear.com/7.x/initials/svg?seed={safe_name}&backgroundColor=E63946"

                        st.markdown(f"""
                            <img src="{avatar_url}" class="client-avatar">
                            <div class="client-info">
                                <h4 style="margin:0; padding-top:5px; color:inherit;">{c.name}</h4>
                                <small style="opacity:0.7">ID: {c.id}</small>
                            </div>
                        """, unsafe_allow_html=True)

                        st.markdown("---")

                        st.markdown(f"🪪 **{c.driver_license}**")
                        st.markdown(f"📧 {c.email}")
                        st.markdown(f"📞 {c.phone}")

                        if st.button("Voir dossier", key=f"v_{c.id}", use_container_width=True):
                            st.toast(f"Dossier de {c.name} chargé.", icon="📂")

    # -----------------------------------------------------
    # ONGLET 2 : CRÉATION (FORMULAIRE PRO)
    # -----------------------------------------------------
    
    with tab_create:
        st.subheader("Enregistrer un nouveau client")
        with st.form("new_client_form"):
            c1, c2 = st.columns(2)
            n = c1.text_input("Nom Prénom *")
            p = c2.text_input("Numéro Permis *")
            e = c1.text_input("Email")
            t = c2.text_input("Téléphone")

            if st.form_submit_button("Valider l'inscription", type="primary"):
                if n and p:
                    nid = 1 if not system.customers else max(c.id for c in system.customers) + 1
                    system.add_customer(Customer(nid, n, p, e, t))
                    save_data()
                    st.success(f"Client **{n}** ajouté !")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Nom et Permis requis.")

    # -----------------------------------------------------
    # ONGLET 3 : MODIFICATION / SUPPRESSION
    # -----------------------------------------------------
    
    with tab_edit:
        st.subheader("Mise à jour dossier")
        if not system.customers:
            st.warning("Aucun client dans la base.")
        else:
            opts = {f"{c.name} ({c.driver_license})": c for c in system.customers}
            sel = st.selectbox("Rechercher client", list(opts.keys()))
            target = opts[sel]

            with st.form("edit_client"):
                c1, c2 = st.columns(2)
                en = c1.text_input("Nom", value=target.name)
                ep = c2.text_input("Permis", value=target.driver_license)
                ee = c1.text_input("Email", value=target.email)
                et = c2.text_input("Téléphone", value=target.phone)

                if st.form_submit_button("Sauvegarder modifications"):
                    target.name = en; target.driver_license = ep; target.email = ee; target.phone = et
                    save_data()
                    st.success("Modifications enregistrées.")
                    st.rerun()

            st.markdown("---")
            if st.button("🗑️ Supprimer ce client"):
                system.customers.remove(target)
                save_data()
                st.warning("Client supprimé.")
                st.rerun()

    # -----------------------------------------------------
    # ONGLET 4 : HISTORIQUE (NOUVEAU !)
    # -----------------------------------------------------
    with tab_history:
        st.subheader("Historique des locations")
        if not system.customers:
            st.info("Base vide.")
        else:
            opts = {f"{c.name}": c for c in system.customers}
            sel = st.selectbox("Voir historique de :", list(opts.keys()))
            client = opts[sel]
            
            # Filtre les locations du client
            history = [r for r in system.rentals if r.customer.id == client.id]
            
            if history:
                data_hist = []
                for r in history:
                    # Nom du véhicule intelligent
                    vname = getattr(r.vehicle, 'brand', getattr(r.vehicle, 'name', 'Véhicule'))
                    vmod = getattr(r.vehicle, 'model', getattr(r.vehicle, 'breed', ''))
                    
                    data_hist.append({
                        "Début": r.start_date,
                        "Fin": r.end_date,
                        "Véhicule": f"{vname} {vmod}",
                        "Montant": f"{r.total_price}€",
                        "Statut": "En cours" if r.is_active else "Terminé"
                    })
                st.dataframe(pd.DataFrame(data_hist), use_container_width=True)
            else:
                st.info(f"{client.name} n'a aucune location enregistrée.")

# =========================================================
# PAGE : ADMINISTRATION (GESTION DU PARC)
# =========================================================
elif selected == "Administration":
    st.title("⚙️ Administration du Parc")
    
    # Sous-menu local pour ne pas surcharger la page
    sub_action = st.radio("Action requise :", ["✨ Ajouter un élément", "🗑️ Retirer un élément"], horizontal=True)
    st.markdown("---")

    # -----------------------------------------------------
    # 1. AJOUTER UN VÉHICULE OU ANIMAL
    # -----------------------------------------------------
    if sub_action == "✨ Ajouter un élément":
        st.subheader("Nouvelle Acquisition")
        
        # A. FILTRES DE SÉLECTION
        c_filter1, c_filter2, c_filter3 = st.columns(3)
        
        # 1. Nature (Machine vs Vivant)
        nature = c_filter1.radio("Nature", ["🏎️ Véhicule / Machine", "🐉 Animal Vivant"], label_visibility="collapsed")
        
        # 2. Environnement
        env = c_filter2.selectbox("Environnement", ["Terre", "Mer", "Air"])
        
        # 3. Type précis (Dynamique)
        type_options = []
        if nature == "🏎️ Véhicule / Machine":
            if env == "Terre": type_options = ["Voiture", "Camion", "Moto", "Corbillard", "Karting", "Calèche", "Charrette"]
            elif env == "Mer": type_options = ["Bateau", "Sous-Marin"]
            elif env == "Air": type_options = ["Avion", "Hélicoptère"]
        else: # Animal
            if env == "Terre": type_options = ["Cheval", "Âne", "Chameau"]
            elif env == "Mer": type_options = ["Baleine", "Dauphin"]
            elif env == "Air": type_options = ["Aigle", "Dragon"]

        v_type = c_filter3.selectbox("Type d'élément", type_options)
        
        # Prix par défaut intelligent
        default_price = PRICE_MAP.get(v_type, 50.0)

        # B. FORMULAIRE
        with st.form("admin_add_form"):
            st.info(f"Configuration : **{v_type}** ({env})")
            c1, c2 = st.columns(2)
            
            # Champ commun : Tarif
            rate = c1.number_input("Tarif Journalier (€)", value=default_price, step=10.0)
            
            # --- LOGIQUE VÉHICULES ---
            if nature == "🏎️ Véhicule / Machine":
                if v_type not in ["Calèche", "Charrette"]:
                    # Labels dynamiques
                    lbl_id = "Plaque"
                    if v_type in ["Bateau", "Sous-Marin"]: lbl_id = "N° Coque / Nom"
                    if v_type == "Avion": lbl_id = "Immatriculation (F-XXXX)"
                    if v_type == "Karting": lbl_id = "N° Kart"

                    brand = c1.text_input("Marque / Constructeur")
                    model = c2.text_input("Modèle")
                    plate = c1.text_input(lbl_id)
                    year = c2.number_input("Année", value=2024, step=1)

                    # Spécifiques Moteurs
                    c_spec1, c_spec2 = st.columns(2)
                    arg_a = 0; arg_b = False; arg_c = ""

                    if v_type == "Voiture":
                        arg_a = c_spec1.number_input("Nb Portes", 3, 5, 5)
                        arg_b = c_spec2.checkbox("Climatisation ?", True)
                    elif v_type == "Camion":
                        arg_a = c_spec1.number_input("Volume (m3)", value=20.0)
                        arg_c = c_spec2.number_input("Poids Max (T)", value=10.0)
                    elif v_type == "Moto":
                        arg_a = c_spec1.number_input("Cylindrée (cc)", value=500)
                        arg_b = c_spec2.checkbox("TopCase ?", False)
                    elif v_type == "Sous-Marin":
                        arg_a = c_spec1.number_input("Prof. Max (m)", value=500.0)
                        arg_b = c_spec2.checkbox("Propulsion Nucléaire ?", True)
                    # (Ajoutez ici les autres types si nécessaire : Avion, Hélico, Bateau...)
                    elif v_type == "Avion":
                        arg_a = c_spec1.number_input("Envergure (m)", value=15.0)
                        arg_c = c_spec2.number_input("Nb Moteurs", 1, 4, 1)
                    elif v_type == "Hélicoptère":
                        arg_a = c_spec1.number_input("Nb Pales", 2, 8, 4)
                        arg_c = c_spec2.number_input("Alt. Max (m)", value=3000)
                    elif v_type == "Bateau":
                        arg_a = c_spec1.number_input("Longueur (m)", value=10.0)
                        arg_c = c_spec2.number_input("Puissance (cv)", value=150.0)
                    elif v_type == "Corbillard":
                        arg_a = c_spec1.number_input("Long. Cercueil (m)", value=2.2)
                        arg_b = c_spec2.checkbox("Réfrigéré ?", True)
                    elif v_type == "Karting":
                        arg_c = c_spec1.text_input("Moteur", "4T Honda")
                        arg_b = c_spec2.checkbox("Indoor ?", True)

                # Cas Attelages
                else:
                    seats = c1.number_input("Nb Places", 1, 10, 2)
                    c_spec1, c_spec2 = st.columns(2)
                    arg_a = 0; arg_b = False
                    if v_type == "Calèche": arg_b = c_spec1.checkbox("Toit ?", True)
                    elif v_type == "Charrette": arg_a = c_spec1.number_input("Charge Max (kg)", value=200.0)

            # --- LOGIQUE ANIMAUX ---
            else:
                name = c1.text_input("Nom")
                breed = c2.text_input("Race / Espèce")
                age = c1.number_input("Âge (ans)", 1, 500, 5)
                
                c_spec1, c_spec2 = st.columns(2)
                arg_a = 0; arg_b = False; arg_c = 0

                if v_type == "Cheval":
                    arg_a = c_spec1.number_input("Taille (cm)", value=160)
                    arg_c = c_spec2.number_input("Fers (mm)", value=100)
                elif v_type == "Dragon":
                    arg_a = c_spec1.number_input("Portée Feu (m)", value=100.0)
                    arg_c = c_spec2.text_input("Couleur", "Rouge")
                elif v_type == "Âne":
                    arg_a = c_spec1.number_input("Capacité (kg)", value=50.0)
                    arg_b = c_spec2.checkbox("Têtu ?", True)
                # (Ajoutez les autres animaux ici : Baleine, Aigle...)
                elif v_type == "Aigle":
                    arg_a = c_spec1.number_input("Envergure (cm)", value=200)
                    arg_c = c_spec2.number_input("Alt. Max (m)", value=2000)
                elif v_type == "Baleine":
                    arg_a = c_spec1.number_input("Poids (T)", value=100.0)
                    arg_b = c_spec2.checkbox("Chante ?", True)
                elif v_type == "Dauphin":
                    arg_a = c_spec1.number_input("Vitesse (km/h)", value=40.0)
                    arg_b = c_spec2.checkbox("Connaît des tours ?", True)
                elif v_type == "Chameau":
                    arg_a = c_spec1.number_input("Nb Bosses", 1, 2, 2)
                    arg_c = c_spec2.number_input("Eau (L)", value=100.0)

            # --- VALIDATION ---
            if st.form_submit_button("💾 Enregistrer dans le parc", type="primary"):
                # Calcul ID
                new_id = 1 if not system.fleet else max(v.id for v in system.fleet) + 1
                obj = None

                # Instanciation (Mapping)
                if v_type == "Voiture": obj = Car(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Camion": obj = Truck(new_id, rate, brand, model, plate, year, arg_a, arg_c)
                elif v_type == "Moto": obj = Motorcycle(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Sous-Marin": obj = Submarine(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Bateau": obj = Boat(new_id, rate, brand, model, plate, year, arg_a, arg_c)
                elif v_type == "Avion": obj = Plane(new_id, rate, brand, model, plate, year, arg_a, int(arg_c))
                elif v_type == "Hélicoptère": obj = Helicopter(new_id, rate, brand, model, plate, year, int(arg_a), int(arg_c))
                elif v_type == "Corbillard": obj = Hearse(new_id, rate, brand, model, plate, year, arg_a, arg_b)
                elif v_type == "Karting": obj = GoKart(new_id, rate, brand, model, plate, year, arg_c, arg_b)
                
                elif v_type == "Cheval": obj = Horse(new_id, rate, name, breed, age, arg_a, arg_c, arg_c)
                elif v_type == "Dragon": obj = Dragon(new_id, rate, name, breed, age, arg_a, arg_c)
                elif v_type == "Âne": obj = Donkey(new_id, rate, name, breed, age, arg_a, arg_b)
                elif v_type == "Aigle": obj = Eagle(new_id, rate, name, breed, age, arg_a, int(arg_c))
                elif v_type == "Baleine": obj = Whale(new_id, rate, name, breed, age, arg_a, arg_b)
                elif v_type == "Dauphin": obj = Dolphin(new_id, rate, name, breed, age, arg_a, arg_b)
                elif v_type == "Chameau": obj = Camel(new_id, rate, name, breed, age, arg_a, arg_c)
                
                elif v_type == "Calèche": obj = Carriage(new_id, rate, seats, arg_b)
                elif v_type == "Charrette": obj = Cart(new_id, rate, seats, arg_a)

                if obj:
                    system.add_vehicle(obj)
                    save_data()
                    
                    # Animation Lottie (Si disponible)
                    anim_name = "Voiture" if nature.startswith("🏎️") else "Dragon" # Simple fallback
                    # Essai de trouver l'anim précise
                    if v_type in st.session_state.lottie_cache:
                        st_lottie(st.session_state.lottie_cache[v_type], height=200, key=f"anim_{new_id}")
                    elif "default" in st.session_state.lottie_cache:
                        st_lottie(st.session_state.lottie_cache["default"], height=200, key=f"anim_{new_id}")
                    
                    st.success(f"✅ **{v_type}** ajouté avec succès !")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Erreur technique : Type non reconnu.")

    # -----------------------------------------------------
    # 2. SUPPRIMER UN ÉLÉMENT
    # -----------------------------------------------------
    elif sub_action == "🗑️ Retirer un élément":
        st.subheader("Sortie d'inventaire")
        
        if not system.fleet:
            st.info("Le parc est vide.")
        else:
            # Création d'une liste lisible pour la suppression
            del_opts = {}
            for v in system.fleet:
                # Nom intelligent
                nom = getattr(v, 'brand', getattr(v, 'name', 'Inconnu'))
                model = getattr(v, 'model', getattr(v, 'breed', ''))
                label = f"#{v.id} - {nom} {model} ({v.__class__.__name__})"
                del_opts[label] = v

            sel_del = st.selectbox("Sélectionner l'élément à supprimer", list(del_opts.keys()))
            
            col_d1, col_d2 = st.columns([1, 4])
            if col_d1.button("🗑️ Supprimer", type="primary"):
                obj_to_del = del_opts[sel_del]
                system.fleet.remove(obj_to_del)
                save_data()
                st.success("Élément retiré du parc.")
                time.sleep(1)
                st.rerun()

# =========================================================
# PAGE : ATELIER (MAINTENANCE INTELLIGENTE)
# =========================================================
elif selected == "Atelier":
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