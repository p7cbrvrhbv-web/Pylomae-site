# PYLOMAE : site pylomae.fr

Site vitrine de PYLOMAE (sites internet en abonnement pour artisans et commerçants locaux) et modèles d'aperçu envoyés aux prospects.
Adrien débute en code et travaille sous Windows : explications simples, en français.

## Mise en ligne

- Chaque envoi sur `main` est mis en ligne automatiquement sur https://pylomae.fr par Cloudflare (Worker `pylomae-site`, « Workers Builds »). Pas d'étape de build.
- Ne jamais pousser sur `main` sans l'accord d'Adrien : passer par une branche et une pull request.

## Organisation

- `index.html` : page d'accueil. Les coordonnées et les témoignages sont dans le bloc `CONFIG` en haut du fichier ; la section « Ils m'ont fait confiance » reste cachée tant que `temoignages` est vide.
- `cgv/` : conditions générales de vente. `apercu/` : outil d'aperçu manuel.
- `modeles/<métier>/index.html` et `modeles/<métier>/contenu.json` : les 11 modèles par métier. **Fichiers générés : ne jamais les modifier à la main.**
- `outils/generer_apercus.py` (thèmes, métiers, textes), `outils/gabarit_apercu.html` (gabarit commun), `outils/metiers.json` (généré lui aussi).

## Modifier un modèle ou ajouter un métier

1. Modifier `outils/gabarit_apercu.html` ou les données de `outils/generer_apercus.py` (ajouter un métier = une entrée dans `METIERS`, avec 4 photos).
2. Relancer la génération : `py outils\generer_apercus.py` sous Windows, `python3 outils/generer_apercus.py` ailleurs.
3. Envoyer ensemble le gabarit, le script et tous les fichiers régénérés.

Un hook (`.claude/settings.json`, script `.claude/hooks/garde_modeles.py`) fait l'étape 2 tout seul après chaque modification du gabarit ou du script, et refuse les modifications à la main des fichiers générés.

## Lien avec Filon (dépôt `p7cbrvrhbv-web/Filon`)

Filon, l'appli de prospection, dépend de ce site :
- elle lit `https://pylomae.fr/modeles/<métier>/` et `contenu.json` pour créer les vrais sites des clients. Renommer ou supprimer un champ de `contenu.json`, ou changer la structure du gabarit, peut casser l'onglet Sites de Filon ;
- les liens courts `pylomae.fr/a/<code>` sont servis par le Worker Cloudflare `filon`, pas par ce dépôt ;
- les aperçus sont personnalisés par l'adresse (`nom`, `ville`, `tel`, `adresse`, `h`, `note`, `avis`, `c`) : garder ces paramètres.

## Règles à toujours respecter

- Avis : uniquement des avis d'exemple, signalés comme tels. Jamais de faux avis présentés comme vrais.
- Photos : Unsplash uniquement (licence libre). Jamais de photos Google des commerces.
- Identité : noir, blanc et vert émeraude (#0E6B4E, #34B98A sur fond noir), titres Lora, texte Poppins.
- Textes en français, simples et directs, sans ton « écrit par une IA ».
- Les prix, l'offre et les conditions (49 €/mois, offre de lancement à 39 €, engagement 12 mois, garantie 30 jours) doivent rester identiques entre `index.html`, `cgv/` et les modèles.
- Aucune clé ni secret dans ce dépôt : il est public.
