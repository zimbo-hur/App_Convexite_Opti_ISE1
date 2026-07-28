"""
Libellés lisibles pour les indicateurs du rapport, affichés à la place des
codes bruts (A1_probleme_sante, s03q11, etc.).

⚠️ Ce sont des libellés PLACEHOLDER, reconstruits à partir du contexte du
rapport (je n'ai pas le questionnaire EHCVM exact). Envoie-moi la liste des
vrais intitulés de questions (ex: "s03q01 = ...", modalités de "s03q11 = ...")
et je remplace les valeurs ci-dessous en gardant les mêmes clés — rien
d'autre à modifier dans le reste du code.
"""

LIBELLES_INDICATEURS = {
    "A1_probleme_sante": "A.1 — Problème de santé (30 derniers jours)",
    "A2_hospitalisation": "A.2 — Hospitalisation (12 derniers mois)",
    "A3_consultation": "A.3 — Recours à la consultation",
    "B1_distance": "B.1 — Distance au lieu de consultation",
    "B2_satisfaction": "B.2 — Satisfaction du service reçu",
    "B3_score_qualite": "B.3 — Score de qualité perçue",
    "B4_raison_non_consult": "B.4 — Raison de non-consultation",
    "C1_assurance": "C.1 — Couverture par une assurance maladie",
    "C2_moustiquaire": "C.2 — Utilisation d'une moustiquaire",
}

LIBELLES_PARTIES = {
    "Partie A — Morbidité & recours": "Morbidité et recours aux soins",
    "Partie B — Accès & qualité perçue": "Accès et qualité perçue des soins",
    "Partie C — Couverture & prévention": "Couverture et prévention",
}


def libelle(code: str) -> str:
    """Retourne le libellé lisible d'un code d'indicateur, ou le code si inconnu."""
    return LIBELLES_INDICATEURS.get(code, code)
