import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import io

# Importations pour la génération de PDF professionnel
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuration de la page
st.set_page_config(
    page_title="GRRECODYS - Système d'Audit Panafricain de Maturité Territoriale",
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
                    st.error("❌ Mot de passe incorrect. Veuillez réessayer.")
                    
        st.markdown("<br><center><small style='color:#777;'>Méthode GRRECODYS© — Tous droits réservés</small></center>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    check_password()
    st.stop()


# --- BASE DE DONNÉES PANAFRICAINE DES CTD ---
PANAFRICAN_DATABASE = {
    "Cameroun": {
        "Devise": "FCFA (XAF)",
        "Communes": {
            "Commune d'Obala": {
                "G": {"details": "Groupes Facebook/WhatsApp communautaires actifs, pas de civic tech outillée.", "score": 3.0},
                "R1": {"details": "Pas de permanence WhatsApp Business. Diaspora active mais non centralisée.", "score": 2.5},
                "R2": {"details": "Données budgétaires partagées uniquement sur affichage physique légal.", "score": 1.5},
                "E": {"details": "Fiche Google Maps existante mais non revendiquée, avis citoyens moyens.", "score": 3.5},
                "C": {"details": "Page Facebook officielle active (publications régulières), pas de charte.", "score": 3.0},
                "D": {"details": "Mobile money omniprésent chez les commerçants, aucun annuaire pro municipal.", "score": 2.0},
                "S": {"details": "Processus d'état civil 100% physiques et manuels à la mairie.", "score": 1.0}
            },
            "Commune de Mbalmayo": {
                "G": {"details": "Dynamisme associatif fort relayé sur les réseaux sociaux.", "score": 3.5},
                "R1": {"details": "Réseau informel d'ambassadeurs locaux valorisant la ville.", "score": 3.0},
                "R2": {"details": "Partenariats PPP/RSE avec les industries du bois non centralisés.", "score": 2.0},
                "E": {"details": "Fiche Google de la mairie revendiquée, belles photos du fleuve Nyong.", "score": 4.0},
                "C": {"details": "Page Facebook officielle structurée et communication régulière.", "score": 3.5},
                "D": {"details": "Pôle commercial actif, pas de vitrine e-commerce territoriale.", "score": 2.5},
                "S": {"details": "Début de centralisation informatique des registres d'état civil.", "score": 1.5}
            },
            "Commune de Sa'a": {
                "G": {"details": "Réseaux communautaires basés sur les initiatives familiales.", "score": 2.0},
                "R1": {"details": "Pas d'accueil numérique ou d'hospitalité digitale identifiée.", "score": 1.0},
                "R2": {"details": "Transparence et dialogue institutionnel numériques inexistants.", "score": 1.0},
                "E": {"details": "Fiche Google Maps absente ou générée automatiquement sans gestion.", "score": 1.0},
                "C": {"details": "Absence de canaux officiels de communication digitale de la mairie.", "score": 1.0},
                "D": {"details": "Secteur informel dominant, paiements mobiles de proximité uniquement.", "score": 1.5},
                "S": {"details": "Services de la collectivité totalement hors-ligne.", "score": 1.0}
            }
        }
    },
    "Côte d'Ivoire": {
        "Devise": "FCFA (XOF)",
        "Communes": {
            "Mairie de Cocody (Abidjan)": {
                "G": {"details": "Civic tech dynamique (applications citoyennes), forte inclusion diasporique.", "score": 4.5},
                "R1": {"details": "Permanence numérique structurée, forte réactivité sur les canaux web.", "score": 4.0},
                "R2": {"details": "Portail open data budgétaire partiel, nombreux partenariats PPP numérisés.", "score": 3.5},
                "E": {"details": "Excellente e-réputation, visites virtuelles disponibles, fiche certifiée.", "score": 4.5},
                "C": {"details": "Identité visuelle forte, charte graphique rigoureuse, présence multi-plateforme.", "score": 4.5},
                "D": {"details": "Écosystème start-up dynamique, annuaire pro numérisé interconnecté.", "score": 4.0},
                "S": {"details": "Dématérialisation avancée de certaines pièces d'état civil.", "score": 3.5}
            },
            "Mairie de Yamoussoukro": {
                "G": {"details": "Groupes d'intérêt locaux actifs mais manque d'outils de participation.", "score": 3.0},
                "R1": {"details": "Hospitalité numérique touristique correcte, manque de suivi personnalisé.", "score": 2.5},
                "R2": {"details": "Dialogue institutionnel fluide mais peu partagé publiquement en ligne.", "score": 2.0},
                "E": {"details": "Fiche Google existante pour la Basilique, mais celle de la mairie est peu mise à jour.", "score": 3.0},
                "C": {"details": "Communication axée sur l'actualité politique du maire, peu de branding territorial.", "score": 2.5},
                "D": {"details": "Intégration du mobile money standard, pas de marketplace locale.", "score": 2.0},
                "S": {"details": "Guichets administratifs informatisés mais sans portail usager distant.", "score": 2.0}
            }
        }
    },
    "Sénégal": {
        "Devise": "FCFA (XOF)",
        "Communes": {
            "Ville de Dakar (Plateau)": {
                "G": {"details": "Forums citoyens en ligne, budgets participatifs amorcés sur les réseaux.", "score": 4.0},
                "R1": {"details": "Services de communication réactifs, ambassadeurs de la culture dakaroise actifs.", "score": 3.5},
                "R2": {"details": "Transparence budgétaire en forte progression, interactions ministérielles outillées.", "score": 3.5},
                "E": {"details": "Patrimoine historique bien répertorié sur Google Maps avec des avis nombreux.", "score": 4.0},
                "C": {"details": "Forte présence sur Twitter/X et Facebook, charte éditoriale moderne.", "score": 4.0},
                "D": {"details": "Forte concentration d'agences numériques, annuaire professionnel en cours.", "score": 3.5},
                "S": {"details": "Informatisation des registres nationaux répercutée au niveau municipal.", "score": 3.0}
            },
            "Commune de Pikine": {
                "G": {"details": "Réseaux d'entraide communautaire denses basés sur WhatsApp.", "score": 3.0},
                "R1": {"details": "Relations directes humaines fortes, peu canalisées par des outils pro.", "score": 2.0},
                "R2": {"details": "Absence de portail open data, gestion budgétaire opaque en ligne.", "score": 1.5},
                "E": {"details": "Fiche Google Maps mal gérée, visuels urbains dominés par l'informel.", "score": 1.5},
                "C": {"details": "Page Facebook officielle intermittente, pas de stratégie de marque.", "score": 2.0},
                "D": {"details": "Commerce de détail dynamique, usage intensif de Wave et Orange Money.", "score": 2.5},
                "S": {"details": "Files d'attente physiques importantes, interconnectivité faible.", "score": 1.5}
            }
        }
    }
}

GENERIC_AFRICA_DATA = {
    "G": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 2.0},
    "R1": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 1.5},
    "R2": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 1.5},
    "E": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 2.0},
    "C": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 2.0},
    "D": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 2.0},
    "S": {"details": "Données régionales moyennes d'Afrique Subsaharienne.", "score": 1.0}
}

PILLARS = {
