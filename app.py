import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import io

# Importation sécurisée de la base de données isolée
try:
    from donnees import PANAFRICAN_DATABASE, GENERIC_AFRICA_DATA
except ImportError:
    # Base de secours si le fichier donnees.py n'est pas lu
    PANAFRICAN_DATABASE = {
        "Cameroun": {
            "Devise": "FCFA (XAF)",
            "Communes": {
                "Commune d'Obala": {
                    "G": {"details": "Groupes Facebook/WhatsApp communautaires actifs.", "score": 3.0},
                    "R1": {"details": "Pas de permanence WhatsApp Business.", "score": 2.5},
                    "R2": {"details": "Données budgétaires partagées uniquement sur affichage physique.", "score": 1.5},
                    "E": {"details": "Fiche Google Maps existante mais non revendiquée.", "score": 3.5},
                    "C": {"details": "Page Facebook officielle active.", "score": 3.0},
                    "D": {"details": "Mobile money omniprésent, aucun annuaire pro.", "score": 2.0},
                    "S": {"details": "Processus d'état civil 100% physiques.", "score": 1.0}
                }
            }
        }
    }
    GENERIC_AFRICA_DATA = {
        "G": {"details": "Moyenne.", "score": 2.0}, "R1": {"details": "Moyenne.", "score": 2.0},
        "R2": {"details": "Moyenne.", "score": 1.5}, "E": {"details": "Moyenne.", "score": 2.0},
        "C": {"details": "Moyenne.", "score": 2.0}, "D": {"details": "Moyenne.", "score": 2.0},
        "S": {"details": "Moyenne.", "score": 1.0}
    }

# Importations pour la génération de PDF professionnel
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuration de la page
st.set_page_config(
    page_title="GRRECODYS - Système d'Audit Panafricain",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Charte graphique GRRECODYS
FOREST_GREEN = "#123524"
FOREST_GREEN_LIGHT = "#1F5C3F"
GOLD = "#D4A017"
ANTHRACITE = "#2B2E33"
GREY_LIGHT = "#F4F5F3"
WHITE = "#FFFFFF"
RED = "#B3261E"
ORANGE = "#C97A1F"
GREEN = "#1F7A3D"

# --- SYSTÈME DE CONNEXION SÉCURISÉ SIMPLIFIÉ (ANTI-BUG) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        f"""
        <div style="background-color:{FOREST_GREEN};padding:30px;border-radius:8px;border-left:8px solid {GOLD};margin-bottom:30px;text-align:center;">
            <h1 style="color:{WHITE};font-size:28px;margin:0;font-family:sans-serif;">🔒 Accès Sécurisé — Espace Expert GRRECODYS</h1>
            <p style="color:{GOLD};font-size:14px;margin-top:5px;margin-bottom:0;font-family:sans-serif;">Veuillez saisir votre mot de passe pour débloquer le tableau de bord d'audit</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        password_input = st.text_input("Mot de passe d'activation", type="password", key="login_pwd_input")
        if st.button("Se connecter au système", key="login_submit_btn"):
            if password_input == "Grrecodys2026":
                st.session_state.authenticated = True
                st.sidebar.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("❌ Mot de passe incorrect. Veuillez réessayer.")
        st.markdown("<br><center><small style='color:#777;'>Méthode GRRECODYS© — Tous droits réservés</small></center>", unsafe_allow_html=True)
    st.stop()

# --- FIN DU SYSTÈME DE CONNEXION ---

# Injection CSS globale pour harmoniser l'interface
st.markdown(
    f"""
    <style>
    .grrecodys-header {{ background-color: {FOREST_GREEN}; padding: 28px 36px; border-radius: 6px; border-left: 8px solid {GOLD}; margin-bottom: 24px; }}
    .grrecodys-header h1 {{ color: {WHITE}; font-size: 30px; margin: 0; font-weight: 700; font-family:sans-serif; }}
    .grrecodys-header p {{ color: {GOLD}; font-size: 15px; margin-top: 6px; margin-bottom: 0; font-family:sans-serif; }}
    .metric-card {{ background-color: {WHITE}; border-radius: 6px; padding: 18px 22px; border: 1px solid #E0E0E0; border-top: 5px solid {FOREST_GREEN}; }}
    .pillar-card {{ background-color: {WHITE}; border-radius: 6px; padding: 20px 24px; border: 1px solid #E0E0E0; margin-bottom: 18px; }}
    .pillar-title {{ color: {FOREST_GREEN}; font-size: 18px; font-weight: 700; margin-bottom: 2px; }}
    .pillar-subtitle {{ color: {ANTHRACITE}; font-size: 13px; font-style: italic; margin-bottom: 12px; opacity: 0.75; }}
    .plan-phase {{ background-color: {WHITE}; border-radius: 6px; padding: 18px 22px; border: 1px solid #E0E0E0; margin-bottom: 16px; }}
    .plan-phase h3 {{ color: {FOREST_GREEN}; border-bottom: 2px solid {GOLD}; padding-bottom: 8px; margin-top: 0; }}
    div.stButton > button {{ background-color: {FOREST_GREEN}; color: {WHITE}; border: none; border-radius: 4px; padding: 10px 26px; font-weight: 600; }}
    div.stDownloadButton > button {{ background-color: {GOLD}; color: {ANTHRACITE}; border: none; border-radius: 4px; padding: 10px 26px; font-weight: 700; width: 100%; }}
    </style>
    """,
    unsafe_allow_html=True
)

PILLARS = {
    "G": {"nom": "Groupes sociaux", "sous_titre": "Inclusion de la Diaspora et Civic Tech locale", "aide": "Niveau de digitalisation de la cohésion communautaire.", "alerte": "Déployer des groupes WhatsApp de quartier animés par des relais formés.", "optimisation": "Structurer une plateforme de civic tech participative (signalements).", "excellence": "Capitaliser sur l'écosystème communautaire numérique comme vitrine régionale."},
    "R1": {"nom": "Relations humaines", "sous_titre": "Hospitalité numérique et Réseau d'ambassadeurs", "aide": "Qualité de la relation humaine en ligne et réactivité aux sollicitations.", "alerte": "Mettre en place une permanence WhatsApp Business assurant une réponse sous 24h.", "optimisation": "Structurer un réseau formel d'ambassadeurs digitaux pour relayer une image accueillante.", "excellence": "Valoriser le réseau d'ambassadeurs digitaux comme argument de marketing."},
    "R2": {"nom": "Relations institutionnelles", "sous_titre": "Gouvernance, Open Data budgétaire et PPP", "aide": "Maturité de la gouvernance numérique multi-niveaux et transparence.", "alerte": "Publier un tableau de bord budgétaire simplifié en Open Data sur les canaux officiels.", "optimisation": "Formaliser un portail de budget participatif en ligne et digitaliser le suivi.", "excellence": "Institutionnaliser une gouvernance ouverte de référence avec données en continu."},
    "E": {"nom": "Esthétique urbaine", "sous_titre": "E-Réputation visuelle, Patrimoine et Google Maps", "aide": "Qualité et actualité de l'image numérique du territoire sur Google Maps.", "alerte": "Réclamer et actualiser sans délai la fiche Google Business avec photos récentes.", "optimisation": "Lancer une campagne de captation photographique et de visites virtuelles 360°.", "excellence": "Devenir une référence en matière de valorisation numérique du patrimoine."},
    "C": {"nom": "Communication territoriale et sociale", "sous_titre": "Branding territorial, Charte et Réseaux sociaux", "aide": "Présence, cohérence et régularité de l'identité numérique institutionnelle.", "alerte": "Créer sans délai une page officielle de la collectivité alimentée régulièrement.", "optimisation": "Adopter une charte graphique unifiée et structurer un calendrier éditorial.", "excellence": "Capitaliser sur une marque territoriale forte et reconnue sur plusieurs plateformes."},
    "D": {"nom": "Dynamisme économique", "sous_titre": "E-commerce local, Annuaire pro et Attractivité investisseurs", "aide": "Degré de digitalisation du tissu économique local et intégration mobile money.", "alerte": "Créer un annuaire professionnel numérique gratuit et généraliser le Mobile Money.", "optimisation": "Développer une marketplace territoriale simple pour les artisans locaux.", "excellence": "Rayonner en tant que pôle d'attractivité économique digitale."},
    "S": {"nom": "Services publics", "sous_titre": "E-administration, État civil et Connectivité infrastructurelle", "aide": "Niveau de dématérialisation des services publics essentiels.", "alerte": "Déployer un système de prise de rendez-vous et de suivi d'état civil par SMS/USSD.", "optimisation": "Développer un portail web de dématérialisation progressive des actes administratifs.", "excellence": "Ériger la collectivité en référence nationale d'e-administration territoriale."},
}

# --- BARRE LATÉRALE D'ADMINISTRATION PANAFRICAINE ---
with st.sidebar:
    st.markdown("## GRRECODYS©")
    st.markdown("Système d'Audit Panafricain")
    st.markdown("---")
    
    pays_options = list(PANAFRICAN_DATABASE.keys()) + ["Autre pays d'Afrique"]
    pays_choisi = st.selectbox("🌍 Pays d'évaluation", pays_options, index=0)
    
    if pays_choisi in PANAFRICAN_DATABASE:
        devise_pays = PANAFRICAN_DATABASE[pays_choisi]["Devise"]
        communes_disponibles = list(PANAFRICAN_DATABASE[pays_choisi]["Communes"].keys()) + ["Autre (saisie libre)"]
        ctd_choice = st.selectbox("Collectivité / Commune", communes_disponibles, index=0)
        
        if ctd_choice == "Autre (saisie libre)":
            nom_ctd = st.text_input("Nom de la collectivité", value="Commune de")
            ctd_facts = GENERIC_AFRICA_DATA
        else:
            nom_ctd = ctd_choice
            ctd_facts = PANAFRICAN_DATABASE[pays_choisi]["Communes"][ctd_choice]
    else:
        devise_pays = "FCFA"
        nom_ctd = st.text_input("Nom de la collectivité", value="Commune de")
        ctd_facts = GENERIC_AFRICA_DATA

    budget_annuel = st.number_input(f"Budget annuel ({devise_pays})", min_value=0, value=2000000000, step=10000000, format="%d")
