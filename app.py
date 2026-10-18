import io
import re
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Crash Lab Predictor", page_icon="🚀", layout="wide")

# Visual style
st.markdown("""
<style>
.stApp {background: radial-gradient(circle at top right, #123047 0, #08131d 38%, #070b10 100%); color:#f4f7fb;}
[data-testid="stSidebar"] {background:#101923;}
.hero {padding:1.25rem 1.4rem; border:1px solid #263a4b; border-radius:20px; background:linear-gradient(135deg,#11283a,#111820); margin-bottom:1rem;}
.hero h1 {margin:0; color:#f5f8fc; font-size:2rem;}
.hero p {color:#aebdca; margin:.35rem 0 0 0;}
.pill {display:inline-block; padding:.25rem .65rem; border-radius:999px; background:#173b2a; color:#72e6a0; font-size:.8rem; border:1px solid #276643;}
.metric-card {padding:.8rem 1rem; border-radius:14px; background:#111b25; border:1px solid #263644;}
.small-note {color:#aab7c4; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

# Full most-recent visible history from the user's 08:34 screenshot, top-to-bottom and left-to-right.
SCREENSHOT_0834 = [
    1.52, 1.77, 1.11, 24.04, 1.69, 3.27, 2.25, 1.05, 3.39,
    4.38, 1.03, 2.18, 2.19, 3.75, 1.60, 8.27, 2.18, 2.78,
    1.01, 1.46, 4.57, 11.73, 1.35, 1.17, 1.11, 9.54, 3.21,
    1.12, 1.34, 3.36, 11.86, 16.15, 1.69, 1.28, 3.68
]

def parse_multipliers(raw):
    if not raw or not raw.strip():
        return []
    parts = re.split(r"[\s,;|]+", raw.strip().replace("×", "x").replace("X", "x"))
    values = []
    for part in parts:
        part = part.strip().lower().replace("x", "")
        if not part:
            continue
        part = part.replace(",", ".") if part.count(",") == 1 and "." not in part else part
        try:
            v = float(part)
            if np.isfinite(v) and v >= 1:
                values.append(round(v, 2))
        except ValueError:
            continue
    return values

def summarize(values):
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    bands = {
        "Moins de 2x": int(np.sum(arr < 2)),
        "2x à moins de 10x": int(np.sum((arr >= 2) & (arr < 10))),
        "10x ou plus": int(np.sum(arr >= 10)),
    }
    return {
        "n": n,
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "under_1_5": int(np.sum(arr < 1.5)),
        "under_2": bands["Moins de 2x"],
        "bands": bands,
        "series": arr
    }

if "history" not in st.session_state:
    st.session_state.history = SCREENSHOT_0834.copy()
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

st.markdown("""
<div class="hero">
  <span class="pill">CRASH LAB • MODE ANALYSE</span>
  <h1>🚀 Aviator Predictor</h1>
  <p>Historique réel saisi • Analyse statistique • Interface mobile-friendly</p>
</div>
""", unsafe_allow_html=True)

st.warning("Important : le bouton START lance une analyse des données observées. Il ne connaît pas le prochain multiplicateur et ne garantit aucun gain. Aucun flux Paryaj Lakay en direct n'est connecté dans cette version.")

tab_predict, tab_data, tab_sim = st.tabs(["🚀 Predictor / START", "📥 Données historiques", "🧪 Simulation mathématique"])

with tab_predict:
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("### Tableau de bord")
        st.markdown(f"""
        <div class="metric-card">
          <div class="small-note">Plateforme sélectionnée</div>
          <h3 style="margin:.2rem 0">Paryaj Lakay • Aviator</h3>
          <div class="small-note">Mode : historique observé, sans connexion directe</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.metric("Résultats actuellement chargés", len(st.session_state.history))
        start = st.button("▶ START — Analyser l'historique", type="primary", use_container_width=True)
        if start:
            if len(st.session_state.history) < 2:
                st.error("Ajoute au moins deux multiplicateurs pour lancer l'analyse.")
            else:
                st.session_state.analysis_result = summarize(st.session_state.history)
    with right:
        st.markdown("### État")
        if st.session_state.analysis_result:
            st.success("Analyse terminée")
            st.markdown("**Résumé des données observées**")
            st.metric("Médiane historique", f"{st.session_state.analysis_result['median']:.2f}x")
            st.metric("Maximum historique", f"{st.session_state.analysis_result['max']:.2f}x")
            st.caption("Ces mesures décrivent uniquement l'historique chargé. Elles ne sont pas une prédiction du prochain tour.")
        else:
            st.info("Prêt. Appuie sur START pour analyser les données chargées.")
    if st.session_state.analysis_result:
        res = st.session_state.analysis_result
        st.markdown("### 📊 Résultats de l'analyse")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Médiane", f"{res['median']:.2f}x")
        c2.metric("Moyenne", f"{res['mean']:.2f}x")
        c3.metric("Plus bas", f"{res['min']:.2f}x")
        c4.metric("Plus haut", f"{res['max']:.2f}x")
        chart = pd.DataFrame({
            "Nombre de manches": list(res["bands"].values())
        }, index=list(res["bands"].keys()))
        st.bar_chart(chart)
        rows = []
        for label, count in res["bands"].items():
            rows.append({"Catégorie": label, "Nombre": count, "Part de l'échantillon": f"{count / res['n']:.1%}"})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.caption(f"{res['under_1_5']} résultats sur {res['n']} sont sous 1.50x. Cette fréquence historique ne donne pas la probabilité exacte du prochain résultat.")

with tab_data:
    st.markdown("### Historique des multiplicateurs")
    st.caption("La liste ci-dessous vient de la capture envoyée à 08:34, lue de gauche à droite puis de haut en bas. Vérifie les valeurs avant de les utiliser.")
    current_text = ", ".join(f"{v:.2f}" for v in st.session_state.history)
    edited = st.text_area("Valeurs en x (séparées par des virgules, espaces ou retours à la ligne)", value=current_text, height=170)
    a, b = st.columns(2)
    with a:
        if st.button("💾 Charger ces valeurs", use_container_width=True):
            parsed = parse_multipliers(edited)
            if len(parsed) < 2:
                st.error("Entre au moins deux valeurs valides (1.00 ou plus).")
            else:
                st.session_state.history = parsed
                st.session_state.analysis_result = None
                st.success(f"{len(parsed)} valeurs chargées.")
    with b:
        if st.button("↩ Réinitialiser à la capture 08:34", use_container_width=True):
            st.session_state.history = SCREENSHOT_0834.copy()
            st.session_state.analysis_result = None
            st.rerun()
    uploaded = st.file_uploader("Ou importer un CSV contenant une colonne de multiplicateurs", type=["csv"])
    if uploaded is not None:
        try:
            df_in = pd.read_csv(uploaded)
            numeric_cols = df_in.select_dtypes(include="number").columns.tolist()
            if not numeric_cols:
                st.error("Aucune colonne numérique trouvée dans le CSV.")
            else:
                col = st.selectbox("Choisir la colonne des multiplicateurs", numeric_cols)
                if st.button("Importer le CSV"):
                    parsed = [float(v) for v in df_in[col].dropna() if float(v) >= 1]
                    if parsed:
                        st.session_state.history = parsed
                        st.session_state.analysis_result = None
                        st.success(f"{len(parsed)} valeurs importées.")
        except Exception as exc:
            st.error(f"Impossible de lire ce CSV : {exc}")
    st.download_button(
        "⬇ Télécharger l'historique actuel (CSV)",
        data=pd.DataFrame({"multiplicateur_x": st.session_state.history}).to_csv(index=False).encode("utf-8"),
        file_name="crash_lab_historique.csv",
        mime="text/csv"
    )

with tab_sim:
    st.markdown("### Simulation de bankroll")
    st.caption("Simulation théorique indépendante des multiplicateurs historiques. Les résultats dépendent des hypothèses choisies.")
    c1, c2, c3 = st.columns(3)
    with c1:
        bankroll = st.number_input("Capital initial (HTG)", min_value=1.0, value=1000.0, step=100.0)
        stake = st.number_input("Mise par manche (HTG)", min_value=1.0, value=70.0, step=10.0)
    with c2:
        cashout = st.number_input("Cash-out hypothétique (x)", min_value=1.01, value=2.0, step=0.1)
        rtp = st.slider("RTP hypothétique (%)", min_value=50.0, max_value=100.0, value=97.0, step=0.5)
    with c3:
        rounds = st.select_slider("Nombre de manches simulées", options=[50, 100, 250, 500, 1000], value=100)
        seed = st.number_input("Graine aléatoire", min_value=0, value=42, step=1)
    if st.button("🧪 Lancer la simulation", use_container_width=True):
        p_win = (rtp / 100) / cashout
        rng = np.random.default_rng(int(seed))
        balance = bankroll
        track = [balance]
        ruined_at = None
        for i in range(1, int(rounds) + 1):
            if balance < stake:
                ruined_at = i
                track.extend([balance] * (int(rounds) - i + 1))
                break
            won = rng.random() < p_win
            balance += stake * (cashout - 1) if won else -stake
            track.append(balance)
        sim_df = pd.DataFrame({"Capital (HTG)": track[:int(rounds)+1]})
        st.metric("Capital final simulé", f"{track[min(int(rounds), len(track)-1)]:,.2f} HTG")
        st.metric("Espérance théorique par manche", f"{stake * ((rtp/100)-1):,.2f} HTG")
        st.line_chart(sim_df)
        if ruined_at:
            st.warning(f"Capital insuffisant pour miser à partir de la manche {ruined_at}.")
        st.caption("Une simulation n'est pas une prédiction. Les hypothèses RTP/cash-out ne sont pas une vérification du fonctionnement réel du jeu.")

st.divider()
st.markdown("**Connexion en direct : non activée.** Une API/WebSocket officielle et autorisée serait nécessaire pour afficher automatiquement les résultats du site. N'entre jamais ton mot de passe, tes cookies ou tes jetons de session ici.")
st.markdown("[Ouvrir Paryaj Lakay](https://www.paryajlakay.com/)")
st.caption("Crash Lab Predictor • Analyse d'historique observé, sans promesse de précision garantie.")
