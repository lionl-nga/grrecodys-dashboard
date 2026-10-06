import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import io

# Importation de la base de données isolée
from donnees import PANAFRICAN_DATABASE, GENERIC_AFRICA_DATA

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

# --- SYSTÈME DE CONNEXION SÉCURISÉ ---
PASSWORD_CORRECT = "Grrecodys2026"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    st.markdown(
        f"""
        <div style="background-color:{FOREST_GREEN};padding:30px;border-radius:8px;border-left:8px solid {GOLD};margin-bottom:30px;text-align:center;">
            <h1 style="color:{WHITE};font-size:28px;margin:0;">🔒 Accès Sécurisé — Espace Expert GRRECODYS</h1>
            <p style="color:{GOLD};font-size:14px;margin-top:5px;margin-bottom:0;">Veuillez saisir votre mot de passe pour accéder au Système d'Audit Panafricain</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.form("login_form"):
            password_input = st.text_input("Mot de passe d'activation", type="password")
            submit_button = st.form_submit_button("Se connecter au système")
            if submit_button:
                if password_input == PASSWORD_CORRECT:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Mot de passe incorrect.")
                    
        st.markdown("<br><center><small style='color:#777;'>Méthode GRRECODYS© — Tous droits réservés</small></center>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    check_password()
    st.stop()

# --- FORMULATION DES PILIERS ---
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

    budget_annuel = st.number_input(f"Budget annuel de la commune ({devise_pays})", min_value=0, value=2000000000, step=10000000, format="%d")
    nom_auditeur = st.text_input("Nom de l'auditeur", value="Lionel NGA")
    st.markdown("---")
    st.markdown("⚙️ **Mode d'Évaluation**")
    override_mode = st.checkbox("💡 Activer l'ajustement manuel", value=False)
    st.markdown("---")
    if st.button("🚪 Se déconnecter"):
        st.session_state.authenticated = False
        st.rerun()

if "scores" not in st.session_state:
    st.session_state.scores = {}

for code in ["G", "R1", "R2", "E", "C", "D", "S"]:
    if override_mode:
        if code not in st.session_state.scores:
            st.session_state.scores[code] = float(ctd_facts[code]["score"])
    else:
        st.session_state.scores[code] = float(ctd_facts[code]["score"])

st.markdown(
    f"""
    <div class="grrecodys-header">
        <h1>GRRECODYS - Système d'Audit Intégré de Maturité Territoriale</h1>
        <p><b>{nom_ctd} ({pays_choisi})</b> · Budget : {budget_annuel:,.0f} {devise_pays} · Expert : {nom_auditeur} · Mode : {'⚠️ Expert Terrain' if override_mode else '🔒 Données Systèmes Certifiées'}</p>
    </div>
    """.replace(",", " "),
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["📋 Formulaire d'Évaluation", "📊 Tableau de Bord Analytique", "🚀 Plan d'Action Digital National"])

with tab1:
    st.markdown("### Évaluation Clinique de la Collectivité")
    col1, col2 = st.columns(2)
    ordered_codes = list(PILLARS.keys())
    for i, code in enumerate(ordered_codes):
        infos = PILLARS[code]
        fact_info = ctd_facts.get(code, {"details": "Donnée non répertoriée.", "score": 2.0})
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(f'<div class="pillar-card"><div class="pillar-title">{code} — {infos["nom"]}</div><div class="pillar-subtitle">{infos["sous_titre"]}</div>', unsafe_allow_html=True)
            st.markdown(f"**Constat Système :** *{fact_info['details']}*")
            st.caption(infos["aide"])
            
            if not override_mode:
                st.slider(label=f"Score {code}", min_value=0.0, max_value=5.0, value=st.session_state.scores.get(code, 2.0), step=0.5, key=f"slider_{code}", label_visibility="collapsed", disabled=True)
                st.caption(f"🔒 Note système certifiée : **{st.session_state.scores.get(code, 2.0)}/5.0**")
            else:
                st.session_state.scores[code] = st.slider(label=f"Score {code}", min_value=0.0, max_value=5.0, value=float(st.session_state.scores.get(code, 2.0)), step=0.5, key=f"slider_{code}", label_visibility="collapsed")
                st.caption(f"✍️ Note ajustée sur preuve : **{st.session_state.scores[code]}/5.0**")
            st.markdown("</div>", unsafe_allow_html=True)

scores = st.session_state.scores
codes = list(PILLARS.keys())
values = [scores.get(c, 2.0) for c in codes]
labels = [f"{c} — {PILLARS[c]['nom']}" for c in codes]
indice_global = (sum(values) / (5 * len(values))) * 100
budget_digital_recommande = budget_annuel * 0.03

