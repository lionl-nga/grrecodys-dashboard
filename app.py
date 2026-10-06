import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="GRRECODYS - Tableau de Bord de Maturité Territoriale Digital",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

FOREST_GREEN = "#123524"
FOREST_GREEN_LIGHT = "#1F5C3F"
GOLD = "#D4A017"
ANTHRACITE = "#2B2E33"
GREY_LIGHT = "#F4F5F3"
WHITE = "#FFFFFF"
RED = "#B3261E"
ORANGE = "#C97A1F"
GREEN = "#1F7A3D"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {GREY_LIGHT};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {FOREST_GREEN};
    }}
    section[data-testid="stSidebar"] * {{
        color: {WHITE} !important;
    }}
    section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] select {{
        color: {ANTHRACITE} !important;
    }}
    .grrecodys-header {{
        background-color: {FOREST_GREEN};
        padding: 28px 36px;
        border-radius: 6px;
        border-left: 8px solid {GOLD};
        margin-bottom: 24px;
    }}
    .grrecodys-header h1 {{
        color: {WHITE};
        font-size: 30px;
        margin: 0;
        font-weight: 700;
    }}
    .grrecodys-header p {{
        color: {GOLD};
        font-size: 15px;
        margin-top: 6px;
        margin-bottom: 0;
        letter-spacing: 0.4px;
    }}
    .metric-card {{
        background-color: {WHITE};
        border-radius: 6px;
        padding: 18px 22px;
        border: 1px solid #E0E0E0;
        border-top: 5px solid {FOREST_GREEN};
    }}
    .pillar-card {{
        background-color: {WHITE};
        border-radius: 6px;
        padding: 20px 24px;
        border: 1px solid #E0E0E0;
        margin-bottom: 18px;
    }}
    .pillar-title {{
        color: {FOREST_GREEN};
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    .pillar-subtitle {{
        color: {ANTHRACITE};
        font-size: 13px;
        font-style: italic;
        margin-bottom: 12px;
        opacity: 0.75;
    }}
    .insight-banner {{
        border-radius: 5px;
        padding: 16px 20px;
        margin-bottom: 14px;
        border-left: 7px solid;
    }}
    .insight-banner h4 {{
        margin: 0 0 6px 0;
        font-size: 16px;
    }}
    .insight-banner p {{
        margin: 0;
        font-size: 14px;
        line-height: 1.5;
    }}
    .insight-red {{
        background-color: #FBEAE9;
        border-color: {RED};
    }}
    .insight-red h4 {{
        color: {RED};
    }}
    .insight-orange {{
        background-color: #FBF1E4;
        border-color: {ORANGE};
    }}
    .insight-orange h4 {{
        color: {ORANGE};
    }}
    .insight-green {{
        background-color: #E9F5EC;
        border-color: {GREEN};
    }}
    .insight-green h4 {{
        color: {GREEN};
    }}
    .plan-phase {{
        background-color: {WHITE};
        border-radius: 6px;
        padding: 18px 22px;
        border: 1px solid #E0E0E0;
        margin-bottom: 16px;
    }}
    .plan-phase h3 {{
        color: {FOREST_GREEN};
        border-bottom: 2px solid {GOLD};
        padding-bottom: 8px;
        margin-top: 0;
    }}
    div.stButton > button {{
        background-color: {FOREST_GREEN};
        color: {WHITE};
        border: none;
        border-radius: 4px;
        padding: 10px 26px;
        font-weight: 600;
    }}
    div.stButton > button:hover {{
        background-color: {FOREST_GREEN_LIGHT};
        color: {WHITE};
    }}
    div.stDownloadButton > button {{
        background-color: {GOLD};
        color: {ANTHRACITE};
        border: none;
        border-radius: 4px;
        padding: 10px 26px;
        font-weight: 700;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

PILLARS = {
    "G": {
        "nom": "Groupes sociaux",
        "sous_titre": "Inclusion de la Diaspora et Civic Tech locale",
        "aide": "Niveau de digitalisation de la cohésion communautaire, de l'inclusion de la diaspora et des outils de civic tech (signalement citoyen, cartographie participative).",
        "defaut": 3.0,
        "alerte": "Déployer des groupes WhatsApp de quartier animés par des relais communautaires formés (les « crieurs publics numériques ») et un canal SMS/USSD d'alerte pour couvrir les populations non connectées à internet.",
        "optimisation": "Structurer une plateforme de civic tech participative (cartographie citoyenne des conflits fonciers, signalement communautaire) et professionnaliser l'animation des groupes numériques déjà actifs.",
        "excellence": "Capitaliser sur l'écosystème communautaire numérique en place comme vitrine de bonnes pratiques réplicable auprès des communes voisines et des partenaires techniques et financiers.",
    },
    "R1": {
        "nom": "Relations humaines",
        "sous_titre": "Hospitalité numérique et Réseau d'ambassadeurs",
        "aide": "Qualité de la relation humaine prolongée en ligne : réactivité aux sollicitations, réseau d'ambassadeurs digitaux, hospitalité numérique envers visiteurs et diaspora.",
        "defaut": 2.5,
        "alerte": "Mettre en place une permanence WhatsApp Business assurant une réponse humaine sous 24 heures aux sollicitations des usagers, visiteurs et membres de la diaspora.",
        "optimisation": "Structurer un réseau formel d'ambassadeurs digitaux (leaders d'opinion locaux, diaspora active, jeunes créateurs de contenu) pour relayer une image humaine et accueillante du territoire.",
        "excellence": "Valoriser le réseau d'ambassadeurs digitaux comme argument central de marketing territorial auprès des investisseurs et partenaires internationaux.",
    },
    "R2": {
        "nom": "Relations institutionnelles",
        "sous_titre": "Gouvernance, Open Data budgétaire et PPP",
        "aide": "Maturité de la gouvernance numérique multi-niveaux : transparence budgétaire en ligne, conventions RSE/PPP digitalisées, dialogue institutionnel outillé.",
        "defaut": 1.5,
        "alerte": "Publier un tableau de bord budgétaire simplifié en Open Data sur une page Facebook officielle ou un site statique gratuit, pour amorcer sans délai la transparence financière de la collectivité.",
        "optimisation": "Formaliser un portail de budget participatif en ligne et digitaliser le suivi des conventions RSE/RSEI signées avec les partenaires privés et institutionnels.",
        "excellence": "Institutionnaliser une gouvernance ouverte de référence, avec données budgétaires actualisées en continu et accessibles à tous les partenaires.",
    },
    "E": {
        "nom": "Esthétique urbaine",
        "sous_titre": "E-Réputation visuelle, Patrimoine et Google Maps",
        "aide": "Qualité et actualité de l'image numérique du territoire : fiches Google Maps/Business, valorisation photographique du patrimoine, e-réputation visuelle globale.",
        "defaut": 2.0,
        "alerte": "Réclamer et actualiser sans délai la fiche Google Business/Google Maps de la mairie et des principaux sites patrimoniaux, avec des photographies récentes et de qualité.",
        "optimisation": "Lancer une campagne de captation photographique et de visites virtuelles à 360° des sites emblématiques, diffusées sur les plateformes numériques du territoire.",
        "excellence": "Devenir une référence régionale en matière de valorisation numérique du patrimoine et du cadre urbain, mobilisable en communication institutionnelle.",
    },
    "C": {
        "nom": "Communication territoriale et sociale",
        "sous_titre": "Branding territorial, Charte et Réseaux sociaux",
        "aide": "Présence et cohérence de l'identité numérique du territoire : page institutionnelle, charte éditoriale, régularité de publication, notoriété assistée en ligne.",
        "defaut": 2.5,
        "alerte": "Créer sans délai une page Facebook officielle de la collectivité et un compte WhatsApp Business, alimentés au minimum deux fois par semaine, pour combler l'absence de présence institutionnelle en ligne.",
        "optimisation": "Adopter une charte graphique unifiée et structurer un calendrier éditorial multicanal (Facebook, Instagram, radios communautaires relayées en ligne).",
        "excellence": "Capitaliser sur une marque territoriale forte et reconnue sur plusieurs plateformes, mobilisable pour des partenariats de rayonnement national et international.",
    },
    "D": {
        "nom": "Dynamisme économique",
        "sous_titre": "E-commerce local, Annuaire pro et Attractivité investisseurs",
        "aide": "Degré de digitalisation du tissu économique local : annuaire professionnel en ligne, intégration du mobile money, visibilité auprès des investisseurs.",
        "defaut": 2.0,
        "alerte": "Créer un annuaire professionnel numérique gratuit (formulaire en ligne relié à un tableur partagé) recensant les acteurs économiques locaux, et généraliser le Mobile Money (Orange Money, MTN MoMo) comme moyen de paiement de référence.",
        "optimisation": "Développer une marketplace territoriale simple pour les producteurs et artisans locaux, et structurer un programme d'accompagnement numérique à la formalisation des activités informelles.",
        "excellence": "Rayonner en tant que pôle d'attractivité économique digitale, en mesure d'export son modèle d'intégration du commerce local en ligne.",
    },
    "S": {
        "nom": "Services publics",
        "sous_titre": "E-administration, État civil et Connectivité infrastructurelle",
        "aide": "Niveau de dématérialisation des services publics essentiels : état civil, délivrance d'actes, connectivité numérique des infrastructures administratives.",
        "defaut": 1.0,
        "alerte": "Déployer un système de prise de rendez-vous et de suivi de dossier d'état civil par SMS/USSD, en s'appuyant sur les opérateurs mobiles locaux, pour réduire les délais sans dépendre d'une connectivité fixe.",
