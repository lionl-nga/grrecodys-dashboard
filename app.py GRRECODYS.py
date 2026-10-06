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
        "optimisation": "Adopter une charte graphique et éditoriale numérique unifiée et structurer un calendrier éditorial multicanal (Facebook, Instagram, radios communautaires relayées en ligne).",
        "excellence": "Capitaliser sur une marque territoriale forte et reconnue sur plusieurs plateformes, mobilisable pour des partenariats de rayonnement national et international.",
    },
    "D": {
        "nom": "Dynamisme économique",
        "sous_titre": "E-commerce local, Annuaire pro et Attractivité investisseurs",
        "aide": "Degré de digitalisation du tissu économique local : annuaire professionnel en ligne, intégration du mobile money, visibilité auprès des investisseurs.",
        "defaut": 2.0,
        "alerte": "Créer un annuaire professionnel numérique gratuit (formulaire en ligne relié à un tableur partagé) recensant les acteurs économiques locaux, et généraliser le Mobile Money (Orange Money, MTN MoMo) comme moyen de paiement de référence.",
        "optimisation": "Développer une marketplace territoriale simple pour les producteurs et artisans locaux, et structurer un programme d'accompagnement numérique à la formalisation des activités informelles.",
        "excellence": "Rayonner en tant que pôle d'attractivité économique digitale, en mesure d'exporter son modèle d'intégration du commerce local en ligne.",
    },
    "S": {
        "nom": "Services publics",
        "sous_titre": "E-administration, État civil et Connectivité infrastructurelle",
        "aide": "Niveau de dématérialisation des services publics essentiels : état civil, délivrance d'actes, connectivité numérique des infrastructures administratives.",
        "defaut": 1.0,
        "alerte": "Déployer un système de prise de rendez-vous et de suivi de dossier d'état civil par SMS/USSD, en s'appuyant sur les opérateurs mobiles locaux, pour réduire les délais sans dépendre d'une connectivité fixe.",
        "optimisation": "Développer un portail web de dématérialisation progressive des actes administratifs courants et un guichet unique numérique pour les démarches prioritaires.",
        "excellence": "Ériger la collectivité en référence nationale d'e-administration territoriale, avec des délais de traitement optimisés et mesurables.",
    },
}

CTD_OPTIONS = [
    "Commune d'Obala",
    "Commune de Bafia",
    "Commune de Mbalmayo",
    "Commune de Sa'a",
    "Commune d'Akonolinga",
    "Autre (saisie libre)",
]

if "scores" not in st.session_state:
    st.session_state.scores = {code: infos["defaut"] for code, infos in PILLARS.items()}

with st.sidebar:
    st.markdown("## GRRECODYS©")
    st.markdown("Audit de maturité territoriale digitale")
    st.markdown("---")
    ctd_choice = st.selectbox("Collectivité Territoriale Décentralisée (CTD)", CTD_OPTIONS, index=0)
    if ctd_choice == "Autre (saisie libre)":
        nom_ctd = st.text_input("Nom de la CTD", value="Commune de")
    else:
        nom_ctd = ctd_choice
    budget_annuel = st.number_input(
        "Budget annuel de la commune (FCFA)",
        min_value=0,
        value=2000000000,
        step=10000000,
        format="%d",
    )
    nom_auditeur = st.text_input("Nom de l'auditeur", value="Lionel NGA")
    st.markdown("---")
    st.caption(f"Département de la Lékié, Région du Centre" if nom_ctd == "Commune d'Obala" else "")
    st.caption(f"Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

st.markdown(
    f"""
    <div class="grrecodys-header">
        <h1>GRRECODYS - Tableau de Bord de Maturité Territoriale Digital</h1>
        <p>{nom_ctd} · Budget annuel : {budget_annuel:,.0f} FCFA · Auditeur : {nom_auditeur}</p>
    </div>
    """.replace(",", " "),
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    ["📋 Formulaire d'Évaluation", "📊 Tableau de Bord Analytique", "🚀 Plan d'Action Digital National"]
)

with tab1:
    st.markdown("### Évaluation des 7 Piliers GRRECODYS©")
    st.markdown(
        "Positionnez chaque curseur de 0 (absence totale de maturité digitale) à 5 (excellence digitale) selon la situation réelle constatée sur le terrain."
    )
    col1, col2 = st.columns(2)
    ordered_codes = list(PILLARS.keys())
    for i, code in enumerate(ordered_codes):
        infos = PILLARS[code]
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            st.markdown(
                f"""
                <div class="pillar-card">
                    <div class="pillar-title">{code} — {infos['nom']}</div>
                    <div class="pillar-subtitle">{infos['sous_titre']}</div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(infos["aide"])
            st.session_state.scores[code] = st.slider(
                label=f"Score {code}",
                min_value=0.0,
                max_value=5.0,
                value=float(st.session_state.scores[code]),
                step=0.5,
                key=f"slider_{code}",
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    scores = st.session_state.scores
    codes = list(PILLARS.keys())
    values = [scores[c] for c in codes]
    labels = [f"{c} — {PILLARS[c]['nom']}" for c in codes]
    indice_global = (sum(values) / (5 * len(values))) * 100

    colm1, colm2, colm3 = st.columns(3)
    with colm1:
        st.markdown(
            f"""<div class="metric-card"><p style="margin:0;color:#555;font-size:13px;">INDICE DE MATURITÉ GRRECODYS GLOBAL</p>
            <p style="margin:4px 0 0 0;font-size:34px;font-weight:800;color:{FOREST_GREEN};">{indice_global:.1f}%</p></div>""",
            unsafe_allow_html=True,
        )
    with colm2:
        pilier_faible = codes[values.index(min(values))]
        st.markdown(
            f"""<div class="metric-card"><p style="margin:0;color:#555;font-size:13px;">PILIER LE PLUS FRAGILE</p>
            <p style="margin:4px 0 0 0;font-size:20px;font-weight:800;color:{RED};">{pilier_faible} — {PILLARS[pilier_faible]['nom']}</p></div>""",
            unsafe_allow_html=True,
        )
    with colm3:
        pilier_fort = codes[values.index(max(values))]
        st.markdown(
            f"""<div class="metric-card"><p style="margin:0;color:#555;font-size:13px;">PILIER LE PLUS AVANCÉ</p>
            <p style="margin:4px 0 0 0;font-size:20px;font-weight:800;color:{GREEN};">{pilier_fort} — {PILLARS[pilier_fort]['nom']}</p></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    colr, colb = st.columns([1.1, 1])
    with colr:
        radar = go.Figure()
        radar.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=labels + [labels[0]],
                fill="toself",
                fillcolor="rgba(18,53,36,0.35)",
                line=dict(color=FOREST_GREEN, width=3),
                marker=dict(color=GOLD, size=8),
                name=nom_ctd,
            )
        )
        radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=10), gridcolor="#D9D9D9"),
                angularaxis=dict(tickfont=dict(size=11, color=ANTHRACITE)),
                bgcolor=WHITE,
            ),
            showlegend=False,
            margin=dict(l=60, r=60, t=40, b=40),
            paper_bgcolor=WHITE,
            height=460,
            title=dict(text="Radar de Maturité Digitale par Pilier", font=dict(size=15, color=FOREST_GREEN)),
        )
        st.plotly_chart(radar, use_container_width=True)

    with colb:
        def statut_couleur(v):
            if v < 2.5:
                return RED
            if v < 4:
                return ORANGE
            return GREEN

        bar_colors = [statut_couleur(v) for v in values]
        bar = go.Figure()
        bar.add_trace(
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker=dict(color=bar_colors),
                text=[f"{v:.1f} / 5" for v in values],
                textposition="outside",
            )
        )
        bar.update_layout(
            xaxis=dict(range=[0, 5.6], title="Score", gridcolor="#EDEDED"),
            yaxis=dict(autorange="reversed"),
            margin=dict(l=10, r=40, t=40, b=40),
            paper_bgcolor=WHITE,
            plot_bgcolor=WHITE,
            height=460,
            title=dict(text="Positionnement par Pilier", font=dict(size=15, color=FOREST_GREEN)),
        )
        st.plotly_chart(bar, use_container_width=True)

    st.markdown("### Analyse et Recommandations Automatiques")
    for code in codes:
        v = scores[code]
        infos = PILLARS[code]
        if v < 2.5:
            css_class = "insight-red"
            statut = "ALERTE — Action corrective immédiate requise"
            action = infos["alerte"]
        elif v < 4:
            css_class = "insight-orange"
            statut = "OPTIMISATION — Marge de progression identifiée"
            action = infos["optimisation"]
        else:
            css_class = "insight-green"
            statut = "EXCELLENCE — Pilier à capitaliser"
            action = infos["excellence"]
        st.markdown(
            f"""
            <div class="insight-banner {css_class}">
                <h4>{code} — {infos['nom']} ({v:.1f}/5) — {statut}</h4>
                <p>{action}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    rapport_txt = f"""GRRECODYS - RAPPORT DE MATURITE TERRITORIALE DIGITALE
Collectivite : {nom_ctd}
Budget annuel : {budget_annuel:,.0f} FCFA
Auditeur : {nom_auditeur}
Date : {datetime.now().strftime('%d/%m/%Y a %H:%M')}

INDICE DE MATURITE GLOBAL : {indice_global:.1f} %

DETAIL PAR PILIER
""".replace(",", " ")
    for code in codes:
        v = scores[code]
        rapport_txt += f"- {code} ({PILLARS[code]['nom']}) : {v:.1f} / 5\n"
    rapport_txt += "\nRECOMMANDATIONS\n"
    for code in codes:
        v = scores[code]
        infos = PILLARS[code]
        if v < 2.5:
            action = infos["alerte"]
        elif v < 4:
            action = infos["optimisation"]
        else:
            action = infos["excellence"]
        rapport_txt += f"- {code} ({infos['nom']}) : {action}\n"

    colex1, colex2 = st.columns(2)
    with colex1:
        st.download_button(
            label="⬇️ Télécharger le Rapport (.txt)",
            data=rapport_txt,
            file_name=f"Rapport_GRRECODYS_{nom_ctd.replace(' ', '_')}.txt",
            mime="text/plain",
        )
    with colex2:
        st.markdown(
            """
            <button onclick="window.parent.print()" style="background-color:#D4A017;color:#2B2E33;border:none;
            border-radius:4px;padding:10px 26px;font-weight:700;cursor:pointer;width:100%;">
            🖨️ Imprimer le Rapport
            </button>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    scores = st.session_state.scores
    codes = list(PILLARS.keys())

    court_terme = [c for c in codes if scores[c] < 2.5]
    moyen_terme = [c for c in codes if 2.5 <= scores[c] < 4]
    long_terme = [c for c in codes if scores[c] >= 4]

    st.markdown("### Plan d'Action Digital National — Feuille de Route Priorisée")
    st.markdown(
        f"Ce plan d'action est généré automatiquement à partir de l'audit de maturité de **{nom_ctd}** et hiérarchise les priorités d'investissement digital selon le niveau de maturité observé sur chacun des 7 piliers GRRECODYS©."
    )

    budget_digital_recommande = budget_annuel * 0.03
    colp1, colp2 = st.columns(2)
    with colp1:
        st.markdown(
            f"""<div class="metric-card"><p style="margin:0;color:#555;font-size:13px;">ENVELOPPE DIGITALE RECOMMANDÉE (3% DU BUDGET ANNUEL)</p>
            <p style="margin:4px 0 0 0;font-size:28px;font-weight:800;color:{FOREST_GREEN};">{budget_digital_recommande:,.0f} FCFA</p></div>""".replace(",", " "),
            unsafe_allow_html=True,
        )
    with colp2:
        st.markdown(
            f"""<div class="metric-card"><p style="margin:0;color:#555;font-size:13px;">NOMBRE DE PILIERS EN ALERTE PRIORITAIRE</p>
            <p style="margin:4px 0 0 0;font-size:28px;font-weight:800;color:{RED};">{len(court_terme)} / 7</p></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="plan-phase">
            <h3>Phase 1 — Court terme (0 à 6 mois) — Actions correctives immédiates</h3>
        """,
        unsafe_allow_html=True,
    )
    if court_terme:
        for code in court_terme:
            infos = PILLARS[code]
            st.markdown(f"**{code} — {infos['nom']}** ({scores[code]:.1f}/5)")
            st.markdown(f"{infos['alerte']}")
    else:
        st.markdown("Aucun pilier en situation d'alerte critique. La collectivité peut concentrer ses efforts sur la phase d'optimisation.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="plan-phase">
            <h3>Phase 2 — Moyen terme (6 à 18 mois) — Structuration et optimisation</h3>
        """,
        unsafe_allow_html=True,
    )
    if moyen_terme:
        for code in moyen_terme:
            infos = PILLARS[code]
            st.markdown(f"**{code} — {infos['nom']}** ({scores[code]:.1f}/5)")
            st.markdown(f"{infos['optimisation']}")
    else:
        st.markdown("Aucun pilier en phase d'optimisation actuellement identifié.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="plan-phase">
            <h3>Phase 3 — Long terme (18 à 36 mois) — Capitalisation et rayonnement</h3>
        """,
        unsafe_allow_html=True,
    )
    if long_terme:
        for code in long_terme:
            infos = PILLARS[code]
            st.markdown(f"**{code} — {infos['nom']}** ({scores[code]:.1f}/5)")
            st.markdown(f"{infos['excellence']}")
    else:
        st.markdown("Aucun pilier n'a encore atteint le niveau d'excellence. Ce niveau reste l'objectif final de la feuille de route.")
    st.markdown("</div>", unsafe_allow_html=True)

    plan_txt = f"""GRRECODYS - PLAN D'ACTION DIGITAL NATIONAL
Collectivite : {nom_ctd}
Budget annuel : {budget_annuel:,.0f} FCFA
Enveloppe digitale recommandee (3%) : {budget_digital_recommande:,.0f} FCFA
Auditeur : {nom_auditeur}
Date : {datetime.now().strftime('%d/%m/%Y a %H:%M')}

PHASE 1 - COURT TERME (0-6 mois)
""".replace(",", " ")
    if court_terme:
        for code in court_terme:
            plan_txt += f"- {code} ({PILLARS[code]['nom']}) : {PILLARS[code]['alerte']}\n"
    else:
        plan_txt += "Aucun pilier en alerte critique.\n"
    plan_txt += "\nPHASE 2 - MOYEN TERME (6-18 mois)\n"
    if moyen_terme:
        for code in moyen_terme:
            plan_txt += f"- {code} ({PILLARS[code]['nom']}) : {PILLARS[code]['optimisation']}\n"
    else:
        plan_txt += "Aucun pilier en phase d'optimisation.\n"
    plan_txt += "\nPHASE 3 - LONG TERME (18-36 mois)\n"
    if long_terme:
        for code in long_terme:
            plan_txt += f"- {code} ({PILLARS[code]['nom']}) : {PILLARS[code]['excellence']}\n"
    else:
        plan_txt += "Aucun pilier au niveau d'excellence.\n"

    st.markdown("---")
    colpx1, colpx2 = st.columns(2)
    with colpx1:
        st.download_button(
            label="⬇️ Télécharger le Plan d'Action (.txt)",
            data=plan_txt,
            file_name=f"Plan_Action_GRRECODYS_{nom_ctd.replace(' ', '_')}.txt",
            mime="text/plain",
        )
    with colpx2:
        st.markdown(
            """
            <button onclick="window.parent.print()" style="background-color:#D4A017;color:#2B2E33;border:none;
            border-radius:4px;padding:10px 26px;font-weight:700;cursor:pointer;width:100%;">
            🖨️ Imprimer le Plan d'Action
            </button>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("GRRECODYS© — Méthode d'attractivité territoriale conçue par Lionel NGA. Tableau de bord de maturité digitale des Collectivités Territoriales Décentralisées.")
