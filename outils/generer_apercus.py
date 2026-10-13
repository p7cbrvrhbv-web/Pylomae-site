#!/usr/bin/env python3
"""Génère les aperçus métier de PYLOMAE (modeles/<slug>/index.html) à partir d'un gabarit commun.

Usage : python3 outils/generer_apercus.py
Pour ajouter un métier : ajouter une entrée dans METIERS, puis relancer le script.
Les pages acceptent ?nom=…&ville=…&tel=…&note=…&avis=… pour créer un aperçu personnalisé.
Photos : Unsplash (licence libre, usage commercial autorisé), servies par images.unsplash.com.
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THEMES = {
    # Bâtiment, auto, déménagement : capitales condensées, franches.
    "robuste": {
        "fonts": "family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700;800",
        "head": '"Barlow Condensed","Arial Narrow",system-ui,sans-serif',
        "body": '"Barlow",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "700", "name_weight": "800", "name_case": "uppercase", "name_track": "0",
        "name_size": "clamp(3rem,12.5vw,6.6rem)", "radius": "6px", "btn_radius": "6px",
        "muted": "#55595F", "line": "rgba(0,0,0,.12)",
    },
    # Services techniques : grotesque nette et dense.
    "net": {
        "fonts": "family=Schibsted+Grotesk:wght@400;500;600;700;800",
        "head": '"Schibsted Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif',
        "body": '"Schibsted Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "700", "name_weight": "800", "name_case": "none", "name_track": "-.03em",
        "name_size": "clamp(2.8rem,11vw,6rem)", "radius": "10px", "btn_radius": "10px",
        "muted": "#525A5C", "line": "rgba(0,0,0,.11)",
    },
    # Beauté, fleurs : serif fine et lumineuse.
    "elegant": {
        "fonts": "family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Jost:wght@400;500;600",
        "head": '"Cormorant Garamond",Georgia,"Times New Roman",serif',
        "body": '"Jost",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "600", "name_weight": "600", "name_case": "none", "name_track": "-.01em",
        "name_size": "clamp(3.1rem,12.5vw,6.8rem)", "radius": "2px", "btn_radius": "999px",
        "muted": "#5E5860", "line": "rgba(0,0,0,.1)",
    },
    # Bouche, jardin : serif ronde et chaleureuse.
    "chaleureux": {
        "fonts": "family=Figtree:wght@400;500;600;700&family=Young+Serif",
        "head": '"Young Serif",Georgia,"Times New Roman",serif',
        "body": '"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "400", "name_weight": "400", "name_case": "none", "name_track": "-.01em",
        "name_size": "clamp(2.7rem,10.5vw,5.8rem)", "radius": "14px", "btn_radius": "999px",
        "muted": "#5F5752", "line": "rgba(0,0,0,.1)",
    },
}

ICONS = {
    "goutte": '<path d="M12 3c3 4.2 6 7.4 6 11a6 6 0 0 1-12 0c0-3.6 3-6.8 6-11z"/>',
    "eclair": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "feuille": '<path d="M5 19c0-8 5-14 15-14 0 10-6 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
    "cle": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5z"/>',
    "eclat": '<path d="M12 3l1.8 4.6L18 9.4l-4.2 1.5L12 16l-1.8-5.1L6 9.4l4.2-1.8z"/><path d="M19 15l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    "carton": '<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/>',
    "ciseaux": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.2 8.2L20 20"/><path d="M8.2 15.8L20 4"/>',
    "couverts": '<path d="M7 3v8a2 2 0 0 0 2 2v8"/><path d="M5 3v6a2 2 0 0 0 2 2"/><path d="M11 3v6a2 2 0 0 1-2 2"/><path d="M17 21V3c-2.5 2-3 6-3 9h3"/>',
    "epi": '<path d="M12 21V8"/><path d="M12 9c-3 0-4.5-2.5-4.5-5 2.5 0 4.5 1.5 4.5 5z"/><path d="M12 9c3 0 4.5-2.5 4.5-5-2.5 0-4.5 1.5-4.5 5z"/><path d="M12 15c-3 0-4.5-2.5-4.5-5 2.5 0 4.5 1.5 4.5 5z"/><path d="M12 15c3 0 4.5-2.5 4.5-5-2.5 0-4.5 1.5-4.5 5z"/>',
    "fleur": '<circle cx="12" cy="9" r="2"/><path d="M12 7a2.5 2.5 0 1 1 2.4-3.2A2.5 2.5 0 1 1 14 9a2.5 2.5 0 1 1-2 4 2.5 2.5 0 1 1-2-4 2.5 2.5 0 1 1-.4-5.2A2.5 2.5 0 0 1 12 7z"/><path d="M12 13v8"/>',
    "lotus": '<path d="M12 20c-5 0-8.5-3-8.5-8 4.5 0 8.5 3 8.5 8z"/><path d="M12 20c5 0 8.5-3 8.5-8-4.5 0-8.5 3-8.5 8z"/><path d="M12 20c-2.2-3.2-2.2-9.5 0-15 2.2 5.5 2.2 11.8 0 15z"/>',
}

WA_PYLOMAE = "33651603705"  # WhatsApp d'Adrien : boutons « Ce site me plaît » et « Demander une modification »

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M8 12.3l2.6 2.6L16 9.5"/></svg>'

H = ["Lundi au vendredi", "Samedi", "Dimanche", "Dimanche et lundi", "Lundi"]

METIERS = [
    {
        "slug": "plombier", "label": "Plombier", "phrase": "un plombier", "theme": "robuste", "icon": "goutte",
        "nom": "Martin Plomberie", "tel": "06 39 98 12 34",
        "colors": {"brand": "#1F5FBF", "deep": "#0C2346", "soft": "#EEF3FA", "ink": "#0D1B2E", "cta": "#E8542E"},
        "tagline": "Une fuite, une panne ? On intervient vite, avec un prix annoncé avant les travaux.",
        "about_title": "Votre plombier à {ville}",
        "about": "{nom} intervient chez les particuliers et les professionnels de {ville} et des communes voisines. Dépannage, chauffe-eau, salle de bain : chaque intervention commence par un diagnostic clair et un prix annoncé avant de commencer.",
        "trust": ["Intervention rapide", "Devis gratuit et détaillé", "Prix annoncé avant travaux"],
        "services_h2": "Tout ce qui touche à l’eau",
        "services": [
            ["Recherche de fuite", "Fuite visible ou cachée, tuyau percé, joint usé : on localise et on répare."],
            ["Débouchage", "Évier, WC, douche ou canalisation bouchée, avec le matériel adapté."],
            ["Chauffe-eau", "Panne, entretien ou remplacement de votre ballon d’eau chaude."],
            ["Salle de bain", "Rénovation complète ou remplacement de douche, baignoire et meuble vasque."],
            ["Robinetterie", "Robinet qui goutte, mitigeur à changer, chasse d’eau qui coule en continu."],
            ["Chauffage", "Radiateurs, circuit de chauffage et raccordements, en neuf comme en rénovation."],
        ],
        "special_h2": "En cas de fuite, les bons réflexes", "special_p": "Quelques gestes simples limitent les dégâts en attendant notre arrivée.", "special_style": "steps",
        "special": [
            ["Coupez l’arrivée d’eau générale", "Le robinet se trouve souvent près du compteur, sous l’évier ou à la cave."],
            ["Coupez l’électricité si l’eau approche des prises", "Au tableau électrique, par sécurité."],
            ["Photographiez les dégâts", "Ces photos serviront pour votre déclaration à l’assurance."],
            ["Appelez-nous", "Nous vous indiquons le délai et le prix avant de nous déplacer."],
        ],
        "gallery_title": "Nos interventions en images", "gallery_note": "vos propres photos de chantier",
        "place_title": "Zone d’intervention", "place_text": "{ville} et les communes alentour, dans un rayon d’environ 30 km.",
        "hours": [["Lundi au vendredi", "8 h – 19 h"], ["Samedi", "9 h – 12 h"], ["Urgences", "Sur appel"]],
        "faq": [
            ["Intervenez-vous en urgence ?", "Oui, pour les fuites et les pannes d’eau chaude, nous intervenons le jour même dans la mesure du possible. Appelez-nous pour connaître le délai."],
            ["Le devis est-il gratuit ?", "Oui. Pour des travaux, le devis est gratuit et détaillé. Pour un dépannage, le prix vous est annoncé avant toute intervention."],
            ["Quelles communes couvrez-vous ?", "{ville} et les communes situées à environ 30 km autour."],
        ],
        "contact_h2": "Un devis ? Une urgence ?", "contact_p": "Appelez-nous ou envoyez un SMS avec une photo du problème : nous vous répondons rapidement avec un délai et un prix.",
        "cta": "Demander un devis", "sms": "Envoyer un SMS",
        "photos": [
            ["1749532125405-70950966b0e5", "Plombier réparant une installation dans une salle de bain"],
            ["1676210134190-3f2c0d5cf58d", "Intervention sur un chauffe-eau"],
            ["1676210133055-eab6ef033ce3", "Réparation d’une canalisation sous un évier"],
            ["1521207418485-99c705420785", "Robinet de cuisine"],
        ],
    },
    {
        "slug": "electricien", "label": "Électricien", "phrase": "un électricien", "theme": "net", "icon": "eclair",
        "nom": "Lefort Électricité", "tel": "06 39 98 12 35",
        "colors": {"brand": "#F4C21B", "brand_ink": "#17140A", "brand_text": "#7D6000", "deep": "#14161B", "soft": "#F5F4EE", "ink": "#15171C", "cta": "#F4C21B", "cta_ink": "#17140A"},
        "tagline": "Dépannage, mise aux normes et rénovation électrique, pour une installation sûre et conforme.",
        "about_title": "Votre électricien à {ville}",
        "about": "{nom} intervient chez les particuliers et les professionnels de {ville} et des environs. Panne, tableau électrique, rénovation : nous expliquons ce qui doit être fait, pourquoi, et combien cela coûte, avant de commencer.",
        "trust": ["Devis gratuit et détaillé", "Travail propre et soigné", "Installation aux normes"],
        "services_h2": "Votre installation, du tableau à la prise",
        "services": [
            ["Dépannage électrique", "Panne de courant, disjoncteur qui saute, prise ou éclairage qui ne fonctionne plus."],
            ["Mise aux normes", "Remise en conformité selon la norme NF C 15-100, avant une vente ou une location."],
            ["Tableau électrique", "Remplacement d’un ancien tableau à fusibles par un tableau moderne et protégé."],
            ["Rénovation complète", "Refaire l’électricité d’une maison ou d’un appartement, pièce par pièce."],
            ["Éclairage", "Éclairage intérieur, extérieur et spots LED pour réduire votre consommation."],
            ["Interphone et motorisation", "Interphone, visiophone, volets roulants et portails motorisés."],
        ],
        "special_h2": "Les signes qui doivent vous alerter", "special_p": "Si vous reconnaissez l’un de ces cas, faites vérifier votre installation.", "special_style": "points",
        "special": [
            ["Le disjoncteur saute souvent", "Un circuit surchargé ou un défaut d’isolement est souvent en cause."],
            ["Une prise ou un interrupteur chauffe", "Traces noires, odeur de brûlé ou grésillement : coupez le circuit et appelez."],
            ["Votre tableau a encore des fusibles", "Il n’a probablement pas de protection différentielle 30 mA."],
            ["L’installation a plus de 15 ans", "Un diagnostic électrique est alors obligatoire pour vendre ou louer."],
        ],
        "gallery_title": "Nos chantiers en images", "gallery_note": "vos propres photos de chantier",
        "place_title": "Zone d’intervention", "place_text": "{ville} et les environs, dans un rayon d’environ 30 km.",
        "hours": [["Lundi au vendredi", "8 h – 18 h"], ["Samedi", "Sur rendez-vous"]],
        "faq": [
            ["Faut-il tout refaire pour être aux normes ?", "Pas forcément. Après un diagnostic, nous vous indiquons ce qui est vraiment nécessaire pour votre sécurité, et ce qui peut attendre."],
            ["Intervenez-vous pour une simple panne ?", "Oui, du disjoncteur qui saute à la prise qui ne fonctionne plus. Le prix est annoncé avant l’intervention."],
            ["Le devis est-il gratuit ?", "Oui, le devis est gratuit et chaque poste y est détaillé."],
        ],
        "contact_h2": "Parlons de votre projet", "contact_p": "Appelez ou envoyez un SMS avec une photo de votre tableau électrique : vous recevez une première estimation rapidement.",
        "cta": "Demander un devis", "sms": "Envoyer un SMS",
        "photos": [
            ["1621905251189-08b45d6a269e", "Électricien installant un câblage"],
            ["1758101755915-462eddc23f57", "Contrôle d’un tableau électrique au multimètre"],
            ["1544724569-5f546fd6f2b5", "Tableau électrique avec ses disjoncteurs"],
            ["1507494924047-60b8ee826ca9", "Ampoules allumées"],
        ],
    },
    {
        "slug": "paysagiste", "label": "Paysagiste", "phrase": "un paysagiste", "theme": "chaleureux", "icon": "feuille",
        "nom": "Jardins Vasseur", "tel": "06 39 98 12 36",
        "colors": {"brand": "#2F6B2A", "deep": "#17301A", "soft": "#F1F5EC", "ink": "#18261A"},
        "tagline": "Création et entretien de jardins, pour profiter d’un extérieur soigné toute l’année.",
        "about_title": "Votre paysagiste à {ville}",
        "about": "{nom} crée et entretient les jardins des particuliers et des copropriétés autour de {ville}. Tonte, taille, plantations ou aménagement complet : nous choisissons des végétaux adaptés à votre sol et au climat local.",
        "trust": ["Devis sur photo", "Entretien à l’année", "Déchets verts évacués"],
        "services_h2": "De la création à l’entretien",
        "services": [
            ["Création de jardin", "Plan, choix des végétaux adaptés à votre sol et plantation."],
            ["Entretien régulier", "Passage à la fréquence de votre choix pour un jardin toujours net."],
            ["Taille de haies", "Taille de formation et d’entretien, évacuation des déchets verts."],
            ["Tonte et pelouse", "Tonte, scarification, regarnissage et création de gazon."],
            ["Élagage", "Taille des arbres et arbustes, en toute sécurité."],
            ["Terrasses et allées", "Pavage, gravier, bordures et petits aménagements extérieurs."],
        ],
        "special_h2": "Votre jardin au fil des saisons", "special_p": "Chaque saison a ses travaux. Nous les planifions pour vous.", "special_style": "points",
        "special": [
            ["Printemps", "Reprise de la tonte, plantations et scarification du gazon."],
            ["Été", "Tonte régulière, taille des haies et arrosage raisonné."],
            ["Automne", "Ramassage des feuilles, plantation des arbres et dernière tonte."],
            ["Hiver", "Élagage, taille des fruitiers et préparation des massifs."],
        ],
        "gallery_title": "Nos jardins en images", "gallery_note": "vos propres photos de réalisations",
        "place_title": "Zone d’intervention", "place_text": "{ville} et les communes voisines, dans un rayon d’environ 25 km.",
        "hours": [["Lundi au vendredi", "8 h – 18 h"], ["Samedi", "8 h – 12 h"]],
        "faq": [
            ["Faut-il un contrat d’entretien ?", "Non. Nous intervenons aussi ponctuellement, par exemple pour une taille de haie ou un nettoyage de printemps."],
            ["Comment obtenir un devis ?", "Envoyez quelques photos de votre jardin par SMS : vous recevez une première estimation sans déplacement."],
            ["Les déchets verts sont-ils évacués ?", "Oui, nous repartons avec les déchets verts après chaque intervention."],
        ],
        "contact_h2": "Parlons de votre jardin", "contact_p": "Création, entretien ou simple coup de propre avant l’été : décrivez votre projet, nous vous répondons rapidement.",
        "cta": "Demander un devis", "sms": "Envoyer des photos",
        "photos": [
            ["1700689807667-82630348b301", "Allée en briques bordée de massifs fleuris"],
            ["1734303023491-db8037a21f09", "Tonte d’une pelouse"],
            ["1734079692079-aae7e24a7035", "Pose de gazon en rouleaux"],
            ["1617850687395-620757feb1f3", "Terrasse en bois entourée de plantes"],
        ],
    },
    {
        "slug": "garage", "label": "Garagiste", "phrase": "un garage", "theme": "robuste", "icon": "cle",
        "nom": "Garage Moreau", "tel": "06 39 98 12 37", "kicker": "Garage automobile",
        "colors": {"brand": "#C8102E", "deep": "#141418", "soft": "#F5F3F2", "ink": "#16161A", "cta": "#C8102E"},
        "tagline": "Entretien et réparation toutes marques, avec un devis clair avant chaque intervention.",
        "about_title": "Votre garage à {ville}",
        "about": "{nom} entretient et répare les voitures de toutes marques à {ville}. Vidange, freins, pneus ou diagnostic : vous savez ce qui va être fait et combien cela coûte avant que nous commencions.",
        "trust": ["Toutes marques", "Devis avant travaux", "Pièces de qualité"],
        "services_h2": "Tout pour votre voiture",
        "services": [
            ["Révision et vidange", "Entretien en respectant les préconisations du constructeur."],
            ["Freinage", "Plaquettes, disques et liquide de frein contrôlés et remplacés."],
            ["Pneus", "Montage, équilibrage et parallélisme."],
            ["Diagnostic électronique", "Lecture des codes défaut et recherche de panne."],
            ["Climatisation", "Recharge et entretien de votre climatisation."],
            ["Avant le contrôle technique", "Vérification des points contrôlés avant votre passage."],
        ],
        "special_h2": "Les voyants à ne pas ignorer", "special_p": "Si l’un d’eux s’allume, faites vérifier votre véhicule sans attendre.", "special_style": "points",
        "special": [
            ["Voyant moteur", "Un défaut a été détecté : faites établir un diagnostic rapidement."],
            ["Voyant de freinage rouge", "Arrêtez-vous et faites contrôler avant de reprendre la route."],
            ["Voyant de batterie", "Le circuit de charge ne fonctionne plus correctement."],
            ["Voyant de température", "Arrêtez le moteur pour éviter une casse."],
        ],
        "gallery_title": "L’atelier en images", "gallery_note": "vos propres photos de l’atelier",
        "place_title": "L’atelier", "place_text": "Accueil sur rendez-vous à {ville}. Véhicule de prêt selon disponibilité.",
        "hours": [["Lundi au vendredi", "8 h – 12 h, 14 h – 18 h 30"], ["Samedi", "8 h – 12 h"]],
        "faq": [
            ["Est-ce que je garde la garantie constructeur ?", "Oui. L’entretien chez un garage indépendant ne fait pas perdre la garantie, à condition de suivre le carnet d’entretien du constructeur."],
            ["Faut-il prendre rendez-vous ?", "C’est préférable pour que votre véhicule soit pris en charge rapidement. Envoyez-nous un SMS avec le modèle et le problème constaté."],
            ["Le devis est-il gratuit ?", "Oui, le devis est gratuit et aucune réparation n’est faite sans votre accord."],
        ],
        "contact_h2": "Un devis, un rendez-vous ?", "contact_p": "Envoyez par SMS le modèle de votre voiture et le problème constaté : nous vous répondons avec un devis.",
        "cta": "Prendre rendez-vous", "sms": "Envoyer un SMS",
        "photos": [
            ["1625047509248-ec889cbff17f", "Mécanicien inspectant un moteur"],
            ["1645445522156-9ac06bc7a767", "Changement d’un pneu à l’atelier"],
            ["1487754180451-c456f719a1fc", "Remise à niveau de l’huile moteur"],
            ["1619642751034-765dfdf7c58e", "Réparation d’un moteur à la clé"],
        ],
    },
    {
        "slug": "nettoyage", "label": "Entreprise de nettoyage", "phrase": "une entreprise de nettoyage", "theme": "net", "icon": "eclat",
        "nom": "Net & Clair", "tel": "06 39 98 12 38", "kicker": "Nettoyage professionnel",
        "colors": {"brand": "#0E7C86", "deep": "#0B3539", "soft": "#EDF6F6", "ink": "#10282B", "cta": "#FFFFFF"},
        "tagline": "Des locaux impeccables, sans que vous ayez à y penser.",
        "about_title": "Le nettoyage de vos locaux à {ville}",
        "about": "{nom} assure le nettoyage des bureaux, commerces, copropriétés et logements de {ville} et des alentours. En contrat régulier ou en intervention ponctuelle, nous nous adaptons à vos horaires pour ne pas gêner votre activité.",
        "trust": ["Devis gratuit", "Produits adaptés à chaque surface", "Planning sur mesure"],
        "services_h2": "Nos interventions",
        "services": [
            ["Bureaux et commerces", "Entretien régulier, avant ou après vos horaires d’ouverture."],
            ["Parties communes", "Halls, escaliers et ascenseurs de copropriétés."],
            ["Fin de chantier", "Remise au propre après travaux, prête à l’emploi."],
            ["Vitres", "Vitres, baies et vitrines, à l’intérieur comme à l’extérieur."],
            ["Remise en état", "Nettoyage complet avant un état des lieux."],
            ["Interventions ponctuelles", "Grand ménage, événement ou besoin urgent."],
        ],
        "special_h2": "Du devis au suivi, un service simple", "special_p": "Vous avez un interlocuteur unique du début à la fin.", "special_style": "steps",
        "special": [
            ["Photos ou visite", "Vous nous montrez les locaux et vos attentes."],
            ["Devis détaillé", "Surface, fréquence et prestations chiffrées."],
            ["Planning fixé ensemble", "Aux horaires qui ne gênent pas votre activité."],
            ["Contrôle régulier", "Nous vérifions la qualité et ajustons si besoin."],
        ],
        "gallery_title": "Nos interventions en images", "gallery_note": "vos propres photos",
        "place_title": "Zone d’intervention", "place_text": "{ville} et les communes alentour, dans un rayon d’environ 30 km.",
        "hours": [["Bureau", "Lundi au vendredi, 8 h – 18 h"], ["Interventions", "Selon votre planning"]],
        "faq": [
            ["Intervenez-vous en dehors des heures d’ouverture ?", "Oui, tôt le matin, en soirée ou le week-end, selon ce qui gêne le moins votre activité."],
            ["Fournissez-vous les produits et le matériel ?", "Oui, nous venons avec nos produits et notre matériel, adaptés à chaque surface."],
            ["Peut-on faire un essai avant un contrat ?", "Oui, une première intervention ponctuelle permet de vérifier que la prestation vous convient."],
        ],
        "contact_h2": "Parlons de vos locaux", "contact_p": "Indiquez la surface et la fréquence souhaitée : vous recevez un devis rapidement.",
        "cta": "Demander un devis", "sms": "Envoyer un SMS",
        "photos": [
            ["1577412647305-991150c7d163", "Bureaux lumineux et rangés"],
            ["1627905646269-7f034dcc5738", "Nettoyage d’un bureau avec des gants"],
            ["1628177142898-93e36e4e3a50", "Vaporisateur de produit nettoyant"],
            ["1504297050568-910d24c426d3", "Couloir de bureaux aux parois vitrées"],
        ],
    },
    {
        "slug": "demenageur", "label": "Déménageur", "phrase": "un déménageur", "theme": "robuste", "icon": "carton",
        "nom": "Déménagements Roux", "tel": "06 39 98 12 39",
        "colors": {"brand": "#E2701B", "brand_text": "#A9500F", "deep": "#16223B", "soft": "#F4F5F8", "ink": "#121A2B", "cta": "#E2701B"},
        "tagline": "Votre déménagement organisé de A à Z, de l’emballage à l’installation.",
        "about_title": "Votre déménageur à {ville}",
        "about": "{nom} déménage les particuliers et les professionnels depuis {ville}, partout en France. Nous estimons le volume, protégeons votre mobilier et l’installons pièce par pièce à l’arrivée.",
        "trust": ["Devis gratuit", "Mobilier protégé", "Équipe expérimentée"],
        "services_h2": "Une formule pour chaque déménagement",
        "services": [
            ["Déménagement local", "Dans {ville} et les communes voisines."],
            ["Longue distance", "Partout en France, avec un suivi de bout en bout."],
            ["Emballage", "Cartons, protection des objets fragiles et étiquetage."],
            ["Démontage et remontage", "Meubles démontés au départ, remontés à l’arrivée."],
            ["Garde-meubles", "Stockage sécurisé entre deux logements."],
            ["Monte-meubles", "Pour les étages sans ascenseur adapté."],
        ],
        "special_h2": "Votre déménagement en 4 étapes", "special_p": "Vous savez à l’avance ce qui se passe et combien cela coûte.", "special_style": "steps",
        "special": [
            ["Estimation du volume", "Par visite ou par vidéo de votre logement."],
            ["Devis détaillé", "Volume, distance, options : tout est chiffré."],
            ["Emballage et chargement", "Votre mobilier est protégé et chargé avec soin."],
            ["Livraison et installation", "Chaque meuble est posé dans la bonne pièce."],
        ],
        "gallery_title": "Nos déménagements en images", "gallery_note": "vos propres photos",
        "place_title": "Destinations", "place_text": "Départs de {ville} et alentour, vers toute la France.",
        "hours": [["Lundi au samedi", "8 h – 19 h"], ["Devis", "Réponse sous 24 h"]],
        "faq": [
            ["Combien de temps à l’avance faut-il réserver ?", "Idéalement un mois avant, surtout en fin de mois et en été. Pour une date proche, contactez-nous : nous faisons notre possible."],
            ["Pouvez-vous emballer mes affaires ?", "Oui, nous fournissons les cartons et pouvons tout emballer, ou seulement les objets fragiles."],
            ["Comment le prix est-il calculé ?", "Il dépend du volume, de la distance, des étages et des options choisies. Le devis détaille chaque poste."],
        ],
        "contact_h2": "Estimez votre déménagement", "contact_p": "Envoyez par SMS vos adresses de départ et d’arrivée, la date souhaitée et le nombre de pièces.",
        "cta": "Demander un devis", "sms": "Envoyer un SMS",
        "photos": [
            ["1730154838368-c37b1fdebcf6", "Pièce remplie de cartons de déménagement"],
            ["1566576721346-d4a3b4eaeb55", "Remise d’un carton"],
            ["1714647211902-bb711d643a17", "Cartons dans un salon"],
            ["1586781383963-8e66f88077ec", "Cartons prêts au chargement"],
        ],
    },
    {
        "slug": "coiffeur", "label": "Coiffeur", "phrase": "un coiffeur", "theme": "elegant", "icon": "ciseaux",
        "nom": "Atelier Lise", "tel": "06 39 98 12 40", "kicker": "Salon de coiffure",
        "colors": {"brand": "#9A6556", "deep": "#1C1917", "soft": "#F7F2EF", "ink": "#1C1917", "cta": "#FFFFFF"},
        "tagline": "Une coiffure qui vous ressemble, au cœur de {ville}.",
        "about_title": "Le salon",
        "about": "{nom} vous accueille pour la coupe, la couleur et le coiffage, femmes, hommes et enfants. Chaque rendez-vous commence par un temps d’écoute pour comprendre ce que vous voulez vraiment.",
        "trust": ["Sur rendez-vous", "Produits professionnels", "Conseils personnalisés"],
        "services_h2": "Nos prestations",
        "services": [
            ["Coupe femme", "Shampoing, coupe et coiffage adaptés à votre visage."],
            ["Coupe homme et barbe", "Coupe aux ciseaux ou à la tondeuse, taille de barbe."],
            ["Couleur", "Couleur, racines et patine pour un résultat naturel."],
            ["Mèches et balayage", "Lumière et relief, sur mesure."],
            ["Brushing et chignon", "Pour le quotidien comme pour les grandes occasions."],
            ["Soins du cheveu", "Soins profonds pour cheveux secs, fins ou abîmés."],
        ],
        "special_h2": "Prendre le temps de bien faire", "special_p": "Chaque rendez-vous commence par une vraie discussion.", "special_style": "points",
        "special": [
            ["Écoute", "Nous prenons le temps de comprendre ce que vous voulez."],
            ["Diagnostic", "Votre cheveu, votre visage et votre quotidien."],
            ["Savoir-faire", "Des techniques actuelles et des gestes précis."],
            ["Suivi", "Des conseils pour entretenir votre coiffure à la maison."],
        ],
        "gallery_title": "L’ambiance du salon", "gallery_note": "vos propres photos du salon et de vos réalisations",
        "place_title": "Le salon", "place_text": "Au cœur de {ville}, sur rendez-vous.",
        "hours": [["Mardi au vendredi", "9 h – 19 h"], ["Samedi", "8 h 30 – 17 h"], ["Dimanche et lundi", "Fermé"]],
        "faq": [
            ["Prenez-vous sans rendez-vous ?", "Selon les disponibilités du jour. Pour être sûr d’être reçu, prenez rendez-vous par téléphone ou par message."],
            ["Combien de temps dure une couleur ?", "Comptez environ 1 h 30 à 2 h, selon la longueur de vos cheveux et la technique choisie."],
            ["Coiffez-vous les enfants ?", "Oui, nous accueillons les enfants pour la coupe."],
        ],
        "contact_h2": "Prenez rendez-vous", "contact_p": "Appelez ou envoyez un message avec la prestation souhaitée et vos disponibilités.",
        "cta": "Prendre rendez-vous", "sms": "Envoyer un message",
        "photos": [
            ["1633681926022-84c23e8cb2d6", "Salon de coiffure aux miroirs ronds"],
            ["1580618672591-eb180b1a973f", "Brushing au sèche-cheveux et à la brosse ronde"],
            ["1634449571010-02389ed0f9b0", "Coupe de cheveux au salon"],
            ["1595475884562-073c30d45670", "Ciseaux, brosses et pinceau de coloration"],
        ],
    },
    {
        "slug": "institut", "label": "Institut de beauté", "phrase": "un institut de beauté", "theme": "elegant", "icon": "lotus",
        "nom": "Institut Éclat", "tel": "06 39 98 12 44",
        "colors": {"brand": "#7A5683", "deep": "#2B1E30", "soft": "#F6F1F7", "ink": "#24192A", "cta": "#FFFFFF"},
        "tagline": "Prendre soin de vous, en toute sérénité.",
        "about_title": "L’institut",
        "about": "{nom} vous accueille à {ville} pour vos soins du visage, épilations, manucure et massages bien-être. Des cabines au calme, des produits professionnels et des conseils pour prolonger les effets à la maison.",
        "trust": ["Sur rendez-vous", "Produits professionnels", "Cabines au calme"],
        "services_h2": "Nos soins",
        "services": [
            ["Soins du visage", "Nettoyage, hydratation et éclat, selon votre peau."],
            ["Épilations", "Cire ou méthode adaptée, pour toutes les zones."],
            ["Manucure", "Soin des mains, vernis classique ou semi-permanent."],
            ["Beauté des pieds", "Soin complet et pose de vernis."],
            ["Massages bien-être", "Un moment de détente, du dos au corps entier."],
            ["Maquillage", "Pour un événement, un mariage ou une séance photo."],
        ],
        "special_h2": "Un moment rien que pour vous", "special_p": "Dès votre arrivée, tout est pensé pour votre confort.", "special_style": "points",
        "special": [
            ["Accueil", "Nous faisons le point sur vos attentes avant chaque soin."],
            ["Hygiène", "Matériel désinfecté et linge changé à chaque cliente."],
            ["Produits", "Des gammes professionnelles choisies avec soin."],
            ["Conseils", "Les bons gestes pour prolonger les effets à la maison."],
        ],
        "gallery_title": "L’institut en images", "gallery_note": "vos propres photos de l’institut",
        "place_title": "L’institut", "place_text": "À {ville}, sur rendez-vous.",
        "hours": [["Mardi au vendredi", "9 h 30 – 19 h"], ["Samedi", "9 h – 17 h"], ["Dimanche et lundi", "Fermé"]],
        "faq": [
            ["Faut-il prendre rendez-vous ?", "Oui, tous les soins se font sur rendez-vous, par téléphone ou par message."],
            ["Quels produits utilisez-vous ?", "Des gammes professionnelles choisies pour leur efficacité et leur tolérance, adaptées à chaque type de peau."],
            ["Combien de temps dure un soin du visage ?", "Entre 45 minutes et 1 h 15 selon le soin choisi."],
        ],
        "contact_h2": "Prenez rendez-vous", "contact_p": "Appelez ou envoyez un message avec le soin souhaité et vos disponibilités.",
        "cta": "Prendre rendez-vous", "sms": "Envoyer un message",
        "photos": [
            ["1570172619644-dfd03ed5d881", "Soin du visage en cabine"],
            ["1632345031435-8727f6897d53", "Manucure"],
            ["1589710751893-f9a6770ad71b", "Pose d’extensions de cils"],
            ["1512496015851-a90fb38ba796", "Produits de beauté"],
        ],
    },
    {
        "slug": "restaurant", "label": "Restaurant", "phrase": "un restaurant", "theme": "chaleureux", "icon": "couverts",
        "nom": "Le Comptoir", "tel": "06 39 98 12 41",
        "colors": {"brand": "#7A1E2C", "deep": "#2E0D13", "soft": "#F8F2EE", "ink": "#2A1A1C", "cta": "#FFFFFF"},
        "tagline": "Une cuisine de saison, faite maison, à deux pas de chez vous.",
        "about_title": "La maison",
        "about": "{nom} vous accueille à {ville} midi et soir. Une carte courte qui change au fil des saisons, des produits frais travaillés en cuisine et une formule du midi en semaine.",
        "trust": ["Fait maison", "Produits frais", "Formule du midi"],
        "services_h2": "Ce que nous servons",
        "services": [
            ["Entrées du moment", "Selon le marché et la saison."],
            ["Plat du jour", "Une recette différente chaque jour, en semaine."],
            ["Viandes et poissons", "Cuisinés simplement, servis généreusement."],
            ["Assiettes végétariennes", "Des légumes de saison mis en valeur."],
            ["Desserts maison", "Préparés chaque matin en cuisine."],
            ["Vins et boissons", "Une sélection courte et choisie."],
        ],
        "special_h2": "Avant de venir", "special_p": "Tout ce qu’il faut savoir pour votre visite.", "special_style": "points",
        "special": [
            ["Réservation", "Conseillée le week-end, par téléphone ou par message."],
            ["Formule du midi", "Entrée et plat, ou plat et dessert, en semaine."],
            ["Groupes", "Menus sur demande pour vos repas de groupe et anniversaires."],
            ["Allergies", "Signalez-les à la réservation : nous adaptons les plats."],
        ],
        "gallery_title": "La salle et l’assiette", "gallery_note": "vos propres photos de plats et de la salle",
        "place_title": "Nous trouver", "place_text": "Au centre de {ville}.",
        "hours": [["Mardi au samedi", "12 h – 14 h, 19 h – 22 h"], ["Dimanche", "12 h – 14 h"], ["Lundi", "Fermé"]],
        "faq": [
            ["Faut-il réserver ?", "C’est conseillé le week-end. En semaine, vous pouvez aussi venir sans réservation, selon les places disponibles."],
            ["Proposez-vous des plats végétariens ?", "Oui, la carte propose toujours au moins une assiette végétarienne."],
            ["Peut-on privatiser la salle ?", "Oui, pour vos repas de groupe et vos fêtes de famille, sur demande."],
        ],
        "contact_h2": "Réservez votre table", "contact_p": "Appelez ou envoyez un SMS avec le jour, l’heure et le nombre de couverts.",
        "cta": "Réserver une table", "sms": "Réserver par SMS",
        "photos": [
            ["1555396273-367ea4eb4db5", "Salle de restaurant chaleureuse aux tables en bois"],
            ["1564758564527-b97d79cb27c1", "Assiette servie en salle"],
            ["1569096651661-820d0de8b4ab", "Terrasse du restaurant"],
            ["1525193612562-0ec53b0e5d7c", "Table en bois prête pour le service"],
        ],
    },
    {
        "slug": "boulangerie", "label": "Boulangerie", "phrase": "une boulangerie", "theme": "chaleureux", "icon": "epi",
        "nom": "Maison Lefèvre", "tel": "06 39 98 12 42", "kicker": "Boulangerie pâtisserie",
        "colors": {"brand": "#8A4B1F", "deep": "#33200F", "soft": "#FBF5EA", "ink": "#2B1D12", "cta": "#FFFFFF"},
        "tagline": "Du bon pain, cuit chaque matin à {ville}.",
        "about_title": "La boulangerie",
        "about": "{nom} pétrit et cuit sur place pains, viennoiseries et pâtisseries, chaque matin. Pour vos fêtes et vos anniversaires, nous préparons des gâteaux sur commande.",
        "trust": ["Fait sur place", "Cuit chaque matin", "Gâteaux sur commande"],
        "services_h2": "Nos fabrications",
        "services": [
            ["Pains de tradition", "Baguettes et pains au levain, longue fermentation."],
            ["Pains spéciaux", "Céréales, seigle, complet, campagne."],
            ["Viennoiseries", "Croissants et pains au chocolat pur beurre."],
            ["Pâtisseries", "Tartes, éclairs et entremets du moment."],
            ["Gâteaux sur commande", "Anniversaires, baptêmes et fêtes de famille."],
            ["Le midi", "Sandwichs, quiches et formules à emporter."],
        ],
        "special_h2": "Commander un gâteau", "special_p": "Simple et rapide, sans vous déplacer deux fois.", "special_style": "steps",
        "special": [
            ["Choisissez", "Le gâteau, le parfum et le nombre de parts."],
            ["Envoyez votre commande", "Par SMS, idéalement 48 h à l’avance."],
            ["Nous confirmons", "Le prix et l’heure de retrait."],
            ["Retirez en boutique", "Votre gâteau est prêt à l’heure prévue."],
        ],
        "gallery_title": "Nos fabrications en images", "gallery_note": "vos propres photos",
        "place_title": "La boutique", "place_text": "Au cœur de {ville}.",
        "hours": [["Mardi au samedi", "6 h 30 – 19 h 30"], ["Dimanche", "7 h – 13 h"], ["Lundi", "Fermé"]],
        "faq": [
            ["Peut-on commander à l’avance ?", "Oui, pains, viennoiseries et gâteaux se commandent par téléphone ou par SMS, idéalement 48 h avant."],
            ["Faites-vous des gâteaux personnalisés ?", "Oui, pour les anniversaires et les fêtes de famille : dites-nous le parfum, le nombre de parts et le message à écrire."],
            ["Êtes-vous ouverts le dimanche ?", "Oui, le dimanche matin."],
        ],
        "contact_h2": "Une commande, une question ?", "contact_p": "Envoyez un SMS avec votre commande et la date souhaitée, nous vous confirmons rapidement.",
        "cta": "Commander", "sms": "Commander par SMS",
        "photos": [
            ["1568254183919-78a4f43a2877", "Pains en vitrine"],
            ["1555507036-ab1f4038808a", "Croissants"],
            ["1517686469429-8bdb88b9f907", "Préparation de la pâte au rouleau"],
            ["1583338917451-face2751d8d5", "Tartes et gâteaux en vitrine"],
        ],
    },
    {
        "slug": "fleuriste", "label": "Fleuriste", "phrase": "un fleuriste", "theme": "elegant", "icon": "fleur",
        "nom": "Fleurs d’Iris", "tel": "06 39 98 12 43", "kicker": "Artisan fleuriste",
        "colors": {"brand": "#3F6B4F", "deep": "#1C2E22", "soft": "#F7F1F2", "ink": "#1F2A22", "cta": "#FFFFFF"},
        "tagline": "Des fleurs fraîches pour chaque moment de la vie.",
        "about_title": "La boutique",
        "about": "{nom} compose des bouquets et des créations florales à {ville}, avec des fleurs choisies chaque semaine. Anniversaire, mariage, deuil ou simple envie de fleurs : nous imaginons la composition avec vous.",
        "trust": ["Fleurs fraîches", "Compositions sur mesure", "Livraison locale"],
        "services_h2": "Pour toutes les occasions",
        "services": [
            ["Bouquets du jour", "Composés chaque matin avec les fleurs de saison."],
            ["Mariages", "Bouquet de mariée, boutonnières et décoration."],
            ["Deuil", "Gerbes, couronnes et compositions, avec délicatesse."],
            ["Plantes", "Plantes vertes et fleuries, conseils d’entretien."],
            ["Entreprises et événements", "Décoration florale pour vos espaces et réceptions."],
            ["Livraison", "À {ville} et dans les communes voisines."],
        ],
        "special_h2": "Commander un bouquet", "special_p": "Dites-nous l’occasion, nous imaginons la composition.", "special_style": "steps",
        "special": [
            ["L’occasion", "Anniversaire, remerciement, naissance, deuil…"],
            ["Votre budget", "Nous composons avec ce que vous souhaitez dépenser."],
            ["La date", "Retrait en boutique ou livraison."],
            ["La confirmation", "Nous vous envoyons la proposition avant de préparer."],
        ],
        "gallery_title": "Nos créations", "gallery_note": "vos propres photos de bouquets",
        "place_title": "La boutique", "place_text": "À {ville}, retrait sur place ou livraison.",
        "hours": [["Mardi au samedi", "9 h – 19 h"], ["Dimanche", "9 h – 13 h"], ["Lundi", "Fermé"]],
        "faq": [
            ["Livrez-vous ?", "Oui, à {ville} et dans les communes voisines. Indiquez l’adresse et la date à la commande."],
            ["Peut-on commander sans se déplacer ?", "Oui, par téléphone ou par message : nous vous envoyons une proposition avant de préparer."],
            ["Faites-vous les fleurs de mariage ?", "Oui, du bouquet de la mariée à la décoration de la salle. Contactez-nous quelques mois avant la date."],
        ],
        "contact_h2": "Commandez votre bouquet", "contact_p": "Indiquez l’occasion, votre budget et la date : nous vous proposons une composition.",
        "cta": "Commander un bouquet", "sms": "Envoyer un message",
        "photos": [
            ["1487070183336-b863922373d4", "Bouquets devant une boutique de fleurs"],
            ["1709294728779-6be509d45255", "Fleuriste composant un bouquet"],
            ["1587317997383-2e6c1b24040f", "Bouquet rose, vert et blanc"],
            ["1491994336086-44f5d76dd8f2", "Bouquet de tulipes"],
        ],
    },
]


# ---------------------------------------------------------------------------------------------
# Modules propres à chaque métier : réservation de créneau, commande ou demande de devis
# (la demande part par SMS au commerce), et grille de tarifs d'exemple.
# Jours : 0 = dimanche … 6 = samedi. Créneaux toutes les 30 minutes entre les heures données.

def week(days, ranges):
    return {d: ranges for d in days}

NOM = {"id": "nom", "label": "Votre nom", "type": "text", "optional": True, "placeholder": "Votre nom"}
COMMUNE = {"id": "commune", "label": "Commune", "type": "text", "placeholder": "Votre commune"}

WIDGETS = {
    "plombier": {
        "title": "Demander une intervention", "intro": "Décrivez le problème en quelques clics : nous vous répondons rapidement avec un délai et un prix.",
        "note": "La demande part par SMS. Vous pourrez y ajouter une photo du problème.", "short": "Demander", "submit": "Envoyer la demande par SMS",
        "smsIntro": "Bonjour, j’ai besoin d’un plombier :",
        "fields": [
            {"id": "probleme", "label": "Problème", "type": "chips", "options": ["Fuite", "Canalisation bouchée", "Chauffe-eau", "Salle de bain", "Robinetterie", "Autre"]},
            {"id": "delai", "label": "Délai souhaité", "type": "chips", "options": ["Urgent, aujourd’hui", "Cette semaine", "Pas pressé"]},
            COMMUNE, {"id": "details", "label": "Précisions", "type": "textarea", "optional": True, "placeholder": "Ex. : fuite sous l’évier de la cuisine"}, NOM,
        ],
    },
    "electricien": {
        "title": "Demander un devis", "intro": "Quelques clics suffisent : nous revenons vers vous avec une estimation.",
        "note": "La demande part par SMS. Vous pourrez y ajouter une photo de votre tableau électrique.", "short": "Devis", "submit": "Envoyer la demande par SMS",
        "smsIntro": "Bonjour, je souhaite un devis d’électricité :",
        "fields": [
            {"id": "besoin", "label": "Besoin", "type": "chips", "options": ["Panne", "Mise aux normes", "Tableau électrique", "Rénovation", "Éclairage", "Autre"]},
            {"id": "delai", "label": "Délai souhaité", "type": "chips", "options": ["Urgent", "Dans le mois", "Pas pressé"]},
            COMMUNE, {"id": "details", "label": "Précisions", "type": "textarea", "optional": True, "placeholder": "Ex. : le disjoncteur saute quand le four est allumé"}, NOM,
        ],
    },
    "paysagiste": {
        "title": "Demander un devis", "intro": "Choisissez les travaux et la taille du jardin : nous vous envoyons une première estimation.",
        "note": "Ajoutez quelques photos de votre jardin au SMS pour un chiffrage plus précis.", "short": "Devis", "submit": "Envoyer la demande par SMS",
        "smsIntro": "Bonjour, je souhaite un devis pour mon jardin :",
        "fields": [
            {"id": "travaux", "label": "Travaux", "type": "multi", "options": ["Entretien régulier", "Tonte", "Taille de haies", "Élagage", "Création de jardin", "Terrasse ou allée"]},
            {"id": "surface", "label": "Surface du jardin", "type": "chips", "options": ["Moins de 200 m²", "200 à 500 m²", "Plus de 500 m²"]},
            COMMUNE, {"id": "details", "label": "Précisions", "type": "textarea", "optional": True, "placeholder": "Ex. : haie de 20 m à tailler avant l’été"}, NOM,
        ],
    },
    "garage": {
        "title": "Prendre rendez-vous à l’atelier", "intro": "Choisissez la prestation, le jour et l’heure de dépose de votre véhicule : nous vous confirmons par SMS.",
        "note": "Les créneaux suivent les horaires de l’atelier. Le rendez-vous est confirmé par SMS.", "short": "Rendez-vous", "submit": "Envoyer ma demande par SMS",
        "smsIntro": "Bonjour, je souhaite prendre rendez-vous à l’atelier :",
        "schedule": {**week([1, 2, 3, 4, 5], [["08:00", "11:30"], ["14:00", "17:30"]]), 6: [["08:00", "11:30"]]},
        "fields": [
            {"id": "presta", "label": "Prestation", "type": "chips", "options": ["Révision", "Freins", "Pneus", "Diagnostic", "Climatisation", "Pré-contrôle technique"]},
            {"id": "vehicule", "label": "Véhicule", "type": "text", "placeholder": "Ex. : Peugeot 208 de 2019"},
            {"id": "jour", "label": "Jour", "type": "days"}, {"id": "heure", "label": "Heure de dépose", "type": "slots"}, NOM,
        ],
    },
    "nettoyage": {
        "title": "Demander un devis", "intro": "Indiquez le type de locaux, la surface et la fréquence : vous recevez un devis rapidement.",
        "note": "La demande part par SMS. Nous pouvons ensuite passer voir les locaux.", "short": "Devis", "submit": "Envoyer la demande par SMS",
        "smsIntro": "Bonjour, je souhaite un devis de nettoyage :",
        "fields": [
            {"id": "locaux", "label": "Type de locaux", "type": "chips", "options": ["Bureaux", "Commerce", "Copropriété", "Logement", "Fin de chantier"]},
            {"id": "surface", "label": "Surface", "type": "chips", "options": ["Moins de 100 m²", "100 à 300 m²", "Plus de 300 m²"]},
            {"id": "frequence", "label": "Fréquence", "type": "chips", "options": ["Ponctuelle", "Chaque semaine", "Plusieurs fois par semaine"]},
            COMMUNE, {"id": "nom", "label": "Nom ou entreprise", "type": "text", "optional": True, "placeholder": "Votre nom ou votre entreprise"},
        ],
    },
    "demenageur": {
        "title": "Estimer votre déménagement", "intro": "Quelques informations suffisent pour un premier devis, sans visite.",
        "note": "Le volume affiché est une estimation. Le devis précis vous est envoyé par SMS.", "short": "Devis", "submit": "Envoyer la demande par SMS",
        "smsIntro": "Bonjour, je souhaite un devis de déménagement :",
        "fields": [
            {"id": "depart", "label": "Ville de départ", "type": "text", "placeholder": "Ex. : Commercy"},
            {"id": "arrivee", "label": "Ville d’arrivée", "type": "text", "placeholder": "Ex. : Nancy"},
            {"id": "date", "label": "Date souhaitée", "type": "date"},
            {"id": "logement", "label": "Logement", "type": "chips", "options": [
                {"label": "Studio", "info": "Volume estimé : 10 à 15 m³"}, {"label": "2 pièces", "info": "Volume estimé : 20 à 25 m³"},
                {"label": "3 pièces", "info": "Volume estimé : 30 à 40 m³"}, {"label": "4 pièces et plus", "info": "Volume estimé : 45 m³ et plus"}]},
            {"id": "options", "label": "Options", "type": "multi", "optional": True, "options": ["Emballage", "Démontage des meubles", "Garde-meubles", "Monte-meubles"]},
            NOM,
        ],
    },
    "coiffeur": {
        "title": "Prendre rendez-vous", "intro": "Choisissez votre prestation et un créneau : nous vous confirmons le rendez-vous par SMS.",
        "note": "Les créneaux suivent les horaires du salon. Le rendez-vous est confirmé par SMS.", "short": "Réserver", "submit": "Envoyer ma demande par SMS",
        "smsIntro": "Bonjour, je souhaite prendre rendez-vous :",
        "schedule": {**week([2, 3, 4, 5], [["09:00", "18:30"]]), 6: [["08:30", "16:30"]]},
        "fields": [
            {"id": "presta", "label": "Prestation", "type": "chips", "options": ["Coupe femme", "Coupe homme", "Coupe enfant", "Couleur", "Balayage", "Brushing"]},
            {"id": "jour", "label": "Jour", "type": "days"}, {"id": "heure", "label": "Heure", "type": "slots"},
            {"id": "nom", "label": "Votre prénom", "type": "text", "optional": True, "placeholder": "Votre prénom"},
        ],
    },
    "institut": {
        "title": "Prendre rendez-vous", "intro": "Choisissez votre soin et un créneau : nous vous confirmons le rendez-vous par SMS.",
        "note": "Les créneaux suivent les horaires de l’institut. Le rendez-vous est confirmé par SMS.", "short": "Réserver", "submit": "Envoyer ma demande par SMS",
        "smsIntro": "Bonjour, je souhaite prendre rendez-vous :",
        "schedule": {**week([2, 3, 4, 5], [["09:30", "18:00"]]), 6: [["09:00", "16:00"]]},
        "fields": [
            {"id": "soin", "label": "Soin", "type": "chips", "options": ["Soin du visage", "Épilation", "Manucure", "Beauté des pieds", "Massage"]},
            {"id": "jour", "label": "Jour", "type": "days"}, {"id": "heure", "label": "Heure", "type": "slots"},
            {"id": "nom", "label": "Votre prénom", "type": "text", "optional": True, "placeholder": "Votre prénom"},
        ],
    },
    "restaurant": {
        "title": "Réserver une table", "intro": "Indiquez le nombre de personnes, le jour et l’heure : nous vous confirmons la réservation par SMS.",
        "note": "Les horaires proposés sont ceux du service. La réservation est confirmée par SMS.", "short": "Réserver", "submit": "Envoyer ma réservation par SMS",
        "smsIntro": "Bonjour, je souhaite réserver une table :", "lead": 60,
        "schedule": {**week([2, 3, 4, 5, 6], [["12:00", "13:30"], ["19:00", "21:30"]]), 0: [["12:00", "13:30"]]},
        "fields": [
            {"id": "couverts", "label": "Nombre de personnes", "type": "stepper", "min": 1, "max": 12, "value": 2, "suffix": " personnes"},
            {"id": "jour", "label": "Jour", "type": "days"}, {"id": "heure", "label": "Heure", "type": "slots"},
            {"id": "nom", "label": "Nom de la réservation", "type": "text", "placeholder": "Votre nom"},
        ],
    },
    "boulangerie": {
        "title": "Commander un gâteau", "intro": "Choisissez votre gâteau, le nombre de parts et le jour de retrait : nous vous confirmons la commande par SMS.",
        "note": "Commande au moins 48 h à l’avance. Le prix est confirmé par SMS.", "short": "Commander", "submit": "Envoyer ma commande par SMS",
        "smsIntro": "Bonjour, je souhaite commander un gâteau :",
        "schedule": {**week([2, 3, 4, 5, 6], [["07:00", "19:00"]]), 0: [["07:00", "12:30"]]},
        "estimate": {"option": "gateau", "qty": "parts"},
        "fields": [
            {"id": "gateau", "label": "Gâteau", "type": "chips", "options": [
                {"label": "Fraisier", "unit": 4.8}, {"label": "Forêt-noire", "unit": 4.5}, {"label": "Tarte aux fruits", "unit": 3.9},
                {"label": "Entremets chocolat", "unit": 4.5}, {"label": "Paris-brest", "unit": 4.6}]},
            {"id": "parts", "label": "Nombre de parts", "type": "stepper", "min": 4, "max": 30, "step": 2, "value": 8, "suffix": " parts"},
            {"id": "jour", "label": "Jour de retrait", "type": "days", "ahead": 2},
            {"id": "moment", "label": "Heure de retrait", "type": "chips", "options": ["Matin", "Midi", "Après-midi"]},
            {"id": "inscription", "label": "Inscription sur le gâteau", "type": "text", "optional": True, "placeholder": "Ex. : Joyeux anniversaire Léa"},
            NOM,
        ],
    },
    "fleuriste": {
        "title": "Commander un bouquet", "intro": "Dites-nous l’occasion, votre budget et la date : nous vous proposons une composition par SMS.",
        "note": "Nous vous envoyons la proposition avant de préparer le bouquet.", "short": "Commander", "submit": "Envoyer ma commande par SMS",
        "smsIntro": "Bonjour, je souhaite commander un bouquet :",
        "schedule": {**week([2, 3, 4, 5, 6], [["09:00", "19:00"]]), 0: [["09:00", "13:00"]]},
        "fields": [
            {"id": "occasion", "label": "Occasion", "type": "chips", "options": ["Anniversaire", "Remerciement", "Naissance", "Mariage", "Deuil", "Juste comme ça"]},
            {"id": "budget", "label": "Budget", "type": "chips", "options": ["30 €", "50 €", "80 €", "Plus de 80 €"]},
            {"id": "jour", "label": "Pour quel jour ?", "type": "days"},
            {"id": "mode", "label": "Retrait ou livraison", "type": "chips", "options": ["Retrait en boutique", "Livraison"]},
            {"id": "carte", "label": "Message de la carte", "type": "text", "optional": True, "placeholder": "Ex. : Merci pour tout !"},
            NOM,
        ],
    },
}

TARIFS = {
    "coiffeur": {
        "title": "Tarifs", "note": "Tarifs d’exemple : vos propres prestations et tarifs les remplaceront.",
        "groups": [
            ["Femmes", [["Coupe, shampoing et brushing", "45 min", "38 €"], ["Brushing", "30 min", "25 €"], ["Chignon", "45 min", "dès 45 €"]]],
            ["Hommes et enfants", [["Coupe homme", "30 min", "22 €"], ["Coupe et barbe", "45 min", "30 €"], ["Coupe enfant, moins de 12 ans", "20 min", "15 €"]]],
            ["Couleur et soins", [["Couleur racines", "1 h 15", "35 €"], ["Balayage", "2 h", "dès 65 €"], ["Soin profond", "15 min", "12 €"]]],
        ],
    },
    "institut": {
        "title": "Tarifs", "note": "Tarifs d’exemple : vos propres soins et tarifs les remplaceront.",
        "groups": [
            ["Visage", [["Soin éclat", "1 h", "55 €"], ["Soin express", "30 min", "35 €"], ["Restructuration des sourcils", "15 min", "12 €"]]],
            ["Épilations", [["Sourcils", "10 min", "10 €"], ["Demi-jambes", "20 min", "20 €"], ["Jambes entières", "40 min", "32 €"]]],
            ["Mains et pieds", [["Manucure", "30 min", "25 €"], ["Vernis semi-permanent", "45 min", "35 €"], ["Beauté des pieds", "45 min", "35 €"]]],
            ["Massages", [["Massage du dos", "30 min", "35 €"], ["Massage du corps", "1 h", "65 €"]]],
        ],
    },
    "restaurant": {
        "title": "La carte", "note": "Carte d’exemple : vos plats et vos prix la remplaceront.",
        "highlight": ["Formule du midi", "Entrée et plat, ou plat et dessert, du mardi au samedi midi.", "18 €"],
        "groups": [
            ["Entrées", [["Velouté de saison", "", "7 €"], ["Œuf parfait, crème de champignons", "", "9 €"], ["Terrine maison et pickles", "", "8 €"]]],
            ["Plats", [["Plat du jour", "En semaine", "14 €"], ["Suprême de volaille, purée maison", "", "18 €"], ["Poisson du marché, légumes de saison", "", "19 €"], ["Assiette végétarienne de saison", "", "15 €"]]],
            ["Desserts", [["Dessert du jour", "", "6 €"], ["Mousse au chocolat", "", "7 €"], ["Tarte fine aux pommes", "", "7 €"]]],
        ],
    },
    "garage": {
        "title": "Tarifs indicatifs", "note": "Tarifs d’exemple : vos propres tarifs les remplaceront. Un devis précis est établi pour chaque véhicule.",
        "groups": [
            ["Entretien", [["Vidange et filtre à huile", "Selon le véhicule", "dès 89 €"], ["Révision constructeur", "Selon le carnet d’entretien", "dès 149 €"], ["Recharge de climatisation", "", "79 €"]]],
            ["Réparation", [["Plaquettes de frein avant", "Pièces et main-d’œuvre", "dès 129 €"], ["Montage et équilibrage de 4 pneus", "Hors pneus", "50 €"], ["Diagnostic électronique", "", "49 €"]]],
        ],
    },
    "boulangerie": {
        "title": "Nos gâteaux", "note": "Tarifs d’exemple : vos propres gâteaux et tarifs les remplaceront.",
        "groups": [
            ["Gâteaux", [["Fraisier", "La part", "4,80 €"], ["Forêt-noire", "La part", "4,50 €"], ["Tarte aux fruits", "La part", "3,90 €"]]],
            ["Entremets", [["Entremets chocolat", "La part", "4,50 €"], ["Paris-brest", "La part", "4,60 €"], ["Pièce montée", "Pour vos fêtes", "Sur devis"]]],
        ],
    },
}


def tarifs_html(t, cls):
    groups = []
    for name, items in t["groups"]:
        rows = "".join(
            f'<div class="pitem"><b>{html.escape(a)}</b>{f"<span class=d>{html.escape(d)}</span>" if d else ""}<span class="p">{html.escape(p)}</span></div>'
            for a, d, p in items)
        groups.append(f'        <div class="pgroup"><h3>{html.escape(name)}</h3>{rows}</div>')
    hl = ""
    if t.get("highlight"):
        a, b, p = t["highlight"]
        hl = f'      <div class="formule"><div><h3>{html.escape(a)}</h3><p>{html.escape(b)}</p></div><span class="p">{html.escape(p)}</span></div>\n'
    return (f'\n  <section class="s {cls}" id="tarifs">\n    <div class="wrap">\n      <h2>{html.escape(t["title"])}</h2>\n{hl}'
            f'      <div class="prices">\n' + "\n".join(groups) + f'\n      </div>\n      <p class="note">{html.escape(t["note"])}</p>\n    </div>\n  </section>\n')


def img(pid, w, h=None, q=70):
    url = f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&q={q}&w={w}"
    if h:
        url += f"&h={h}&crop=entropy"
    return url


def srcset(pid, sizes):
    return ", ".join(f"{img(pid, w, h)} {w}w" for w, h in sizes)


def rgba(hex_color, a):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"


def fill(text):
    """Échappe le texte puis remplace {nom} et {ville} par des zones personnalisées par l'adresse de la page."""
    t = html.escape(text, quote=False)
    return t.replace("{nom}", '<span data-f="nom"></span>').replace("{ville}", '<span data-f="ville"></span>')


TEMPLATE = open(os.path.join(ROOT, "outils", "gabarit_apercu.html"), encoding="utf-8").read()


def build(m):
    th = THEMES[m["theme"]]
    c = m["colors"]
    brand_ink = c.get("brand_ink", "#FFFFFF")
    cta = c.get("cta", c["brand"])
    cta_ink = c.get("cta_ink", c["deep"] if cta.upper() == "#FFFFFF" else "#FFFFFF")
    hero, *gallery = m["photos"]
    digits = "".join(ch for ch in m["tel"] if ch.isdigit())

    trust = "\n".join(f"    <li>{CHECK}{html.escape(t)}</li>" for t in m["trust"])
    services = "\n".join(
        f'        <div class="svc"><h3>{fill(t)}</h3><p>{fill(d)}</p></div>' for t, d in m["services"])
    special = "\n".join(f"        <li><div><b>{fill(t)}</b><span>{fill(d)}</span></div></li>" for t, d in m["special"])
    gal = []
    for i, (pid, alt) in enumerate(gallery):
        sizes = [(800, 900), (1200, 1350)] if i == 0 else [(600, 600), (900, 900)]
        gal.append(
            f'        <figure><img src="{img(pid, sizes[0][0], sizes[0][1])}" srcset="{srcset(pid, sizes)}" '
            f'sizes="(min-width: 760px) {"60vw" if i == 0 else "35vw"}, {"100vw" if i == 0 else "50vw"}" alt="{html.escape(alt)}" loading="lazy"></figure>')
    hours = "".join(f"<dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd>" for a, b in m["hours"])
    faq = "\n".join(f"        <details><summary>{fill(q)}</summary><p>{fill(a)}</p></details>" for q, a in m["faq"])
    defaults = json.dumps({"nom": m["nom"], "ville": "Villeneuve", "tel": m["tel"], "metier": m["label"]}, ensure_ascii=False)
    w = dict(WIDGETS[m["slug"]])
    w.setdefault("schedule", {})
    order = ["services"] + (["tarifs"] if m["slug"] in TARIFS else []) + ["booking", "special", "gallery", "info", "faq"]
    cls = {name: ("s-soft" if i % 2 == 0 else "") for i, name in enumerate(order)}
    tarifs = tarifs_html(TARIFS[m["slug"]], cls["tarifs"]) if m["slug"] in TARIFS else ""
    widget_json = json.dumps({k: v for k, v in w.items() if k in ("fields", "schedule", "smsIntro", "estimate", "lead")}, ensure_ascii=False).replace("</", "<\\/")

    rep = {
        "FONTS": th["fonts"], "F_HEAD": th["head"], "F_BODY": th["body"],
        "HEAD_WEIGHT": th["head_weight"], "NAME_WEIGHT": th["name_weight"], "NAME_CASE": th["name_case"],
        "NAME_TRACK": th["name_track"], "NAME_SIZE": th["name_size"], "RADIUS": th["radius"], "BTN_RADIUS": th["btn_radius"],
        "MUTED": th["muted"], "LINE": th["line"],
        "BRAND": c["brand"], "BRAND_INK": brand_ink, "BRAND_TEXT": c.get("brand_text", c["brand"]),
        "DEEP": c["deep"], "SOFT": c["soft"], "INK": c["ink"], "CTA_BG": cta, "CTA_INK": cta_ink,
        "SHADE_STRONG": rgba(c["deep"], 0.94), "SHADE_MID": rgba(c["deep"], 0.5),
        "TITLE": html.escape(f'{m["nom"]} · {m["label"]} à Villeneuve'),
        "LABEL_LOWER": html.escape(m["label"].lower()), "KICKER": html.escape(m.get("kicker", m["label"])),
        "ICON": ICONS[m["icon"]],
        "HERO_SRC": img(hero[0], 900, 1350),
        "HERO_TALL": srcset(hero[0], [(600, 900), (900, 1350), (1200, 1800)]),
        "HERO_WIDE": srcset(hero[0], [(1400, 875), (2000, 1250), (2600, 1625)]),
        "HERO_ALT": html.escape(hero[1]),
        "TAGLINE": fill(m["tagline"]), "TRUST": trust,
        "ABOUT_TITLE": fill(m["about_title"]), "ABOUT": fill(m["about"]),
        "SERVICES_H2": html.escape(m["services_h2"]), "SERVICES": services,
        "SPECIAL_H2": html.escape(m["special_h2"]), "SPECIAL_P": html.escape(m["special_p"]),
        "SPECIAL_TAG": "ol" if m["special_style"] == "steps" else "ul", "SPECIAL_CLASS": m["special_style"], "SPECIAL": special,
        "GALLERY_TITLE": html.escape(m["gallery_title"]), "GALLERY": "\n".join(gal), "GALLERY_NOTE": html.escape(m["gallery_note"]),
        "PLACE_TITLE": html.escape(m["place_title"]), "PLACE_TEXT": fill(m["place_text"]), "HOURS": hours,
        "FAQ": faq, "CONTACT_H2": html.escape(m["contact_h2"]), "CONTACT_P": html.escape(m["contact_p"]),
        "CTA": html.escape(m["cta"]), "SMS": html.escape(m["sms"]), "TEL_DIGITS": digits, "DEFAULTS": defaults,
        "CLS_SERVICES": cls["services"], "CLS_BOOKING": cls["booking"], "CLS_SPECIAL": cls["special"], "CLS_GALLERY": cls["gallery"],
        "CLS_INFO": cls["info"], "CLS_FAQ": cls["faq"], "TARIFS": tarifs,
        "W_TITLE": html.escape(w["title"]), "W_INTRO": html.escape(w["intro"]), "W_NOTE": html.escape(w["note"]),
        "W_SUBMIT": html.escape(w["submit"]), "W_SHORT": html.escape(w["short"]), "WIDGET": widget_json, "WA_PYLOMAE": WA_PYLOMAE,
    }
    out = TEMPLATE
    for k, v in rep.items():
        out = out.replace("%%" + k + "%%", v)
    assert "%%" not in out, f"Champ non remplacé dans {m['slug']}"
    d = os.path.join(ROOT, "modeles", m["slug"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)


if __name__ == "__main__":
    for m in METIERS:
        assert len(m["photos"]) == 4, m["slug"]
        build(m)
    with open(os.path.join(ROOT, "outils", "metiers.json"), "w", encoding="utf-8") as f:
        json.dump([{"slug": m["slug"], "label": m["label"], "phrase": m["phrase"],
                    "hero": img(m["photos"][0][0], 800, 560), "nom": m["nom"]} for m in METIERS],
                  f, ensure_ascii=False, indent=2)
    print(f"{len(METIERS)} aperçus générés")
