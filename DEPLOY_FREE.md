# Deploy gratuit avec grande limite

Ce guide donne une solution gratuite avec bonne capacite:
- Frontend: Cloudflare Pages (tres grande limite pour site statique)
- Backend API: Render Free (simple pour FastAPI)

## 1) Publier le backend sur Render

1. Pousse le projet sur GitHub.
2. Ouvre Render et cree un service "Web Service" depuis ton repo.
3. Configure:
   - Build Command:
     ```bash
     pip install -r requirements.txt
     ```
   - Start Command:
     ```bash
     python server.py
     ```
4. Ajoute la variable d'environnement:
   - `GROQ_API_KEY` = ta vraie cle Groq
5. Deploie et copie ton URL backend, par exemple:
   - `https://inzaro-api.onrender.com`

Teste:
- `https://inzaro-api.onrender.com/api/cities`

## 2) Publier le frontend sur Cloudflare Pages

1. Dans Cloudflare Pages, connecte ton repo.
2. Build settings:
   - Build command:
     ```bash
     npm run build
     ```
   - Build output directory:
     ```text
     dist
     ```
3. Ajoute une variable d'environnement de build:
   - `VITE_API_BASE_URL` = `https://inzaro-api.onrender.com/api`
4. Deploy.
5. Tu obtiens un lien public, par exemple:
   - `https://inzaro.pages.dev`

## 3) Resultat

Tu partages seulement le lien Cloudflare Pages avec les utilisateurs.
Le frontend appellera automatiquement ton backend Render.

## Notes sur les limites

- Cloudflare Pages: tres bonne capacite pour frontend statique.
- Render Free: suffisante pour demo/tests, mais peut "sleep" apres inactivite.
- Pour zero sleep, passer sur une offre payante backend plus tard.

## Option ultra-rapide (temporaire)

Si tu veux un lien aujourd'hui sans deploy permanent:
1. Lance backend local `python server.py`
2. Lance frontend `npm run dev`
3. Expose avec Cloudflare Tunnel ou ngrok.

Lien temporaire, mais rapide pour validation utilisateur.
