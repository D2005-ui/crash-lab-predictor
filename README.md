# Crash Lab Predictor

Version améliorée de Crash Lab avec :
- interface de type Predictor et bouton START ;
- analyse statistique des multiplicateurs historiques ;
- valeurs initiales recopiées de la capture Aviator envoyée à 08:34 ;
- modification manuelle des données et import/export CSV ;
- simulation théorique de bankroll.

## Lancer localement
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Déployer sur Streamlit Community Cloud
1. Décompresse ce dossier.
2. Ajoute `app.py`, `requirements.txt` et `README.md` à ton dépôt GitHub.
3. Dans Streamlit Community Cloud, choisis le dépôt et le fichier `app.py`.

## Important
Le bouton START analyse l'historique chargé. Il ne prédit pas le prochain multiplicateur et ne garantit pas de gain. Cette application n'est pas connectée en direct à Paryaj Lakay. Un flux direct nécessite une API ou un WebSocket officiel, documenté et autorisé. Ne saisis jamais de mots de passe, cookies ou jetons de session.
