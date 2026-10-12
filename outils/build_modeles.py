#!/usr/bin/env python3
"""Génère les modèles métier de PYLOMAE à partir d'un gabarit commun.

Usage : python3 outils/build_modeles.py
Chaque métier produit modeles/<slug>/index.html. Pour ajouter un métier,
ajoute une entrée dans METIERS puis relance le script.
Les pages acceptent ?nom=...&ville=...&tel=... pour créer un aperçu personnalisé.
"""
import html, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THEMES = {
    "robuste": {
        "fonts": "family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700;800",
        "head": '"Barlow Condensed","Arial Narrow",system-ui,sans-serif',
        "body": '"Barlow",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "800", "head_transform": "uppercase", "head_spacing": ".005em",
        "radius": "10px", "btn_radius": "8px",
    },
    "elegant": {
        "fonts": "family=Cormorant+Garamond:ital,wght@0,600;1,600&family=Jost:wght@400;500;600",
        "head": '"Cormorant Garamond",Georgia,"Times New Roman",serif',
        "body": '"Jost",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "600", "head_transform": "none", "head_spacing": "0",
        "radius": "4px", "btn_radius": "999px",
    },
    "chaleureux": {
        "fonts": "family=Figtree:wght@400;500;600;700&family=Young+Serif",
        "head": '"Young Serif",Georgia,"Times New Roman",serif',
        "body": '"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif',
        "head_weight": "400", "head_transform": "none", "head_spacing": "0",
        "radius": "16px", "btn_radius": "999px",
    },
}

ICONS = {
    "cle": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5z"/>',
    "eclat": '<path d="M12 3l1.8 4.6L18 9.4l-4.2 1.5L12 16l-1.8-5.1L6 9.4l4.2-1.8z"/><path d="M19 15l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
    "carton": '<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/>',
    "ciseaux": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.2 8.2L20 20"/><path d="M8.2 15.8L20 4"/>',
    "couverts": '<path d="M7 3v8a2 2 0 0 0 2 2v8"/><path d="M5 3v6a2 2 0 0 0 2 2"/><path d="M11 3v6a2 2 0 0 1-2 2"/><path d="M17 21V3c-2.5 2-3 6-3 9h3"/>',
    "epi": '<path d="M12 21V8"/><path d="M12 9c-3 0-4.5-2.5-4.5-5 2.5 0 4.5 1.5 4.5 5z"/><path d="M12 9c3 0 4.5-2.5 4.5-5-2.5 0-4.5 1.5-4.5 5z"/><path d="M12 15c-3 0-4.5-2.5-4.5-5 2.5 0 4.5 1.5 4.5 5z"/><path d="M12 15c3 0 4.5-2.5 4.5-5-2.5 0-4.5 1.5-4.5 5z"/>',
    "fleur": '<circle cx="12" cy="9" r="2"/><path d="M12 7a2.5 2.5 0 1 1 2.4-3.2A2.5 2.5 0 1 1 14 9a2.5 2.5 0 1 1-2 4 2.5 2.5 0 1 1-2-4 2.5 2.5 0 1 1-.4-5.2A2.5 2.5 0 0 1 12 7z"/><path d="M12 13v8"/><path d="M12 18c-2 0-3.5-1.5-3.5-3.5 2 0 3.5 1.5 3.5 3.5z"/>',
    "lotus": '<path d="M12 20c-5 0-8.5-3-8.5-8 4.5 0 8.5 3 8.5 8z"/><path d="M12 20c5 0 8.5-3 8.5-8-4.5 0-8.5 3-8.5 8z"/><path d="M12 20c-2.2-3.2-2.2-9.5 0-15 2.2 5.5 2.2 11.8 0 15z"/>',
}

METIERS = [
    {
        "slug": "garage", "label": "Garagiste", "phrase": "un garage", "theme": "robuste", "icon": "cle",
        "nom": "Garage Moreau", "tel": "06 39 98 12 37", "kicker": "Garage automobile",
        "colors": {"brand": "#C8102E", "brand_deep": "#8E0B20", "soft": "#F6F3F3", "ink": "#16161A", "hero": "dark"},
        "h1": "Entretien et réparation de votre voiture, au juste prix.",
        "lead": "{nom} entretient et répare toutes marques à {ville} : vidange, freins, pneus, diagnostic. Devis clair avant chaque intervention.",
        "trust": ["Toutes marques", "Devis avant travaux", "Pièces de qualité"],
        "services_title": "Nos prestations", "services_h2": "Tout pour votre voiture",
        "services": [
            ["Révision et vidange", "Entretien en respectant les préconisations du constructeur."],
            ["Freinage", "Plaquettes, disques et liquide de frein contrôlés et remplacés."],
            ["Pneus", "Montage, équilibrage et parallélisme."],
            ["Diagnostic électronique", "Lecture des codes défaut et recherche de panne."],
            ["Climatisation", "Recharge et entretien de votre climatisation."],
            ["Avant le contrôle technique", "Vérification des points contrôlés avant votre passage."],
        ],
        "special_eb": "Sécurité", "special_h2": "Les voyants à ne pas ignorer", "special_p": "Si l’un d’eux s’allume, faites vérifier votre véhicule sans attendre.",
        "special_style": "points",
        "special": [
            ["Voyant moteur", "Un défaut a été détecté : faites établir un diagnostic rapidement."],
            ["Voyant de freinage rouge", "Arrêtez-vous et faites contrôler avant de reprendre la route."],
            ["Voyant de batterie", "Le circuit de charge ne fonctionne plus correctement."],
            ["Voyant de température", "Arrêtez le moteur pour éviter une casse."],
        ],
        "place_title": "L’atelier", "place_text": "Accueil sur rendez-vous à {ville}. Véhicule de prêt selon disponibilité.",
        "hours": [["Lundi au vendredi", "8 h – 12 h · 14 h – 18 h 30"], ["Samedi", "8 h – 12 h"]],
        "contact_h2": "Un devis, un rendez-vous ?", "contact_p": "Envoyez par SMS le modèle de votre voiture et le problème constaté : nous vous répondons avec un devis.",
        "cta": "Prendre rendez-vous", "sms": "Envoyer un SMS",
    },
    {
        "slug": "nettoyage", "label": "Entreprise de nettoyage", "phrase": "une entreprise de nettoyage", "theme": "robuste", "icon": "eclat",
        "nom": "Net & Clair", "tel": "06 39 98 12 38", "kicker": "Nettoyage professionnel",
        "colors": {"brand": "#0E7C86", "brand_deep": "#095A61", "soft": "#EEF6F6", "ink": "#10282B", "hero": "brand"},
        "h1": "Des locaux impeccables, sans que vous ayez à y penser.",
        "lead": "{nom} assure le nettoyage de bureaux, commerces, copropriétés et logements à {ville} et alentour, en ponctuel ou en contrat régulier.",
        "trust": ["Devis gratuit", "Produits adaptés", "Planning sur mesure"],
        "services_title": "Prestations", "services_h2": "Nos interventions",
        "services": [
            ["Bureaux et commerces", "Entretien régulier, avant ou après vos horaires d’ouverture."],
            ["Parties communes", "Halls, escaliers et ascenseurs de copropriétés."],
            ["Fin de chantier", "Remise au propre après travaux, prête à l’emploi."],
            ["Vitres", "Vitres, baies et vitrines, intérieur et extérieur."],
            ["Remise en état", "Nettoyage complet avant un état des lieux."],
            ["Interventions ponctuelles", "Grand ménage, événement ou besoin urgent."],
        ],
        "special_eb": "Fonctionnement", "special_h2": "Un service simple, du devis au suivi", "special_p": "Vous avez un interlocuteur unique du début à la fin.",
        "special_style": "steps",
        "special": [
            ["Photos ou visite", "Vous nous montrez les locaux et vos attentes."],
            ["Devis détaillé", "Surface, fréquence et prestations chiffrées."],
            ["Planning fixé ensemble", "Aux horaires qui ne gênent pas votre activité."],
            ["Contrôle régulier", "Nous vérifions la qualité et ajustons si besoin."],
        ],
        "place_title": "Zone d’intervention", "place_text": "{ville} et les communes alentour, dans un rayon d’environ 30 km.",
        "hours": [["Lundi au samedi", "Selon votre planning"], ["Bureau", "8 h – 18 h"]],
        "contact_h2": "Parlons de vos locaux", "contact_p": "Indiquez la surface et la fréquence souhaitée : vous recevez un devis rapidement.",
        "cta": "Demander un devis", "sms": "Envoyer un SMS",
    },
    {
        "slug": "demenageur", "label": "Déménageur", "phrase": "un déménageur", "theme": "robuste", "icon": "carton",
        "nom": "Déménagements Roux", "tel": "06 39 98 12 39", "kicker": "Déménagement",
        "colors": {"brand": "#E2701B", "brand_deep": "#1C2B4A", "soft": "#F4F5F8", "ink": "#121A2B", "hero": "deep"},
        "h1": "Votre déménagement, organisé de A à Z.",
        "lead": "{nom} déménage particuliers et professionnels depuis {ville}, partout en France : emballage, transport et installation du mobilier.",
        "trust": ["Devis gratuit", "Mobilier protégé", "Équipe expérimentée"],
        "services_title": "Prestations", "services_h2": "Une formule pour chaque déménagement",
        "services": [
            ["Déménagement local", "Dans {ville} et les communes voisines."],
            ["Longue distance", "Partout en France, avec un suivi de bout en bout."],
            ["Emballage", "Cartons, protection du fragile et étiquetage."],
            ["Démontage et remontage", "Meubles démontés au départ, remontés à l’arrivée."],
            ["Garde-meubles", "Stockage sécurisé entre deux logements."],
            ["Monte-meubles", "Pour les étages sans ascenseur adapté."],
        ],
        "special_eb": "Déroulement", "special_h2": "Votre déménagement en 4 étapes", "special_p": "Vous savez à l’avance ce qui se passe et combien cela coûte.",
        "special_style": "steps",
        "special": [
            ["Estimation du volume", "Par visite ou par vidéo de votre logement."],
            ["Devis détaillé", "Volume, distance, options : tout est chiffré."],
            ["Emballage et chargement", "Votre mobilier est protégé et chargé avec soin."],
            ["Livraison et installation", "Chaque meuble est posé dans la bonne pièce."],
        ],
        "place_title": "Destinations", "place_text": "Départs de {ville} et alentour, vers toute la France.",
        "hours": [["Lundi au samedi", "8 h – 19 h"], ["Devis", "Réponse sous 24 h"]],
        "contact_h2": "Estimez votre déménagement", "contact_p": "Envoyez par SMS vos adresses de départ et d’arrivée, la date souhaitée et le nombre de pièces.",
        "cta": "Demander un devis", "sms": "Envoyer un SMS",
    },
    {
        "slug": "coiffeur", "label": "Coiffeur", "phrase": "un coiffeur", "theme": "elegant", "icon": "ciseaux",
        "nom": "Atelier Lise", "tel": "06 39 98 12 40", "kicker": "Salon de coiffure",
        "colors": {"brand": "#9A6556", "brand_deep": "#1C1917", "soft": "#F7F2EF", "ink": "#1C1917", "hero": "soft"},
        "h1": "Une coiffure qui vous ressemble, au cœur de {ville}.",
        "lead": "{nom} vous accueille pour la coupe, la couleur et le coiffage, femmes, hommes et enfants. Prenez rendez-vous en un message.",
        "trust": ["Sur rendez-vous", "Produits professionnels", "Conseils personnalisés"],
        "services_title": "Prestations", "services_h2": "Nos prestations",
        "services": [
            ["Coupe femme", "Shampoing, coupe et coiffage adaptés à votre visage."],
            ["Coupe homme et barbe", "Coupe aux ciseaux ou à la tondeuse, taille de barbe."],
            ["Couleur", "Couleur, racines et patine pour un résultat naturel."],
            ["Mèches et balayage", "Lumière et relief, sur mesure."],
            ["Brushing et chignon", "Pour le quotidien comme pour les grandes occasions."],
            ["Soins du cheveu", "Soins profonds pour cheveux secs, fins ou abîmés."],
        ],
        "special_eb": "L’esprit du salon", "special_h2": "Prendre le temps de bien faire", "special_p": "Chaque rendez-vous commence par une vraie discussion.",
        "special_style": "points",
        "special": [
            ["Écoute", "Nous prenons le temps de comprendre ce que vous voulez."],
            ["Diagnostic", "Votre cheveu, votre visage et votre quotidien."],
            ["Savoir-faire", "Des techniques actuelles et des gestes précis."],
            ["Suivi", "Des conseils pour entretenir votre coiffure à la maison."],
        ],
        "place_title": "Le salon", "place_text": "Au cœur de {ville}, sur rendez-vous.",
        "hours": [["Mardi au vendredi", "9 h – 19 h"], ["Samedi", "8 h 30 – 17 h"], ["Dimanche et lundi", "Fermé"]],
        "contact_h2": "Prenez rendez-vous", "contact_p": "Appelez ou envoyez un message avec la prestation souhaitée et vos disponibilités.",
        "cta": "Prendre rendez-vous", "sms": "Envoyer un message",
    },
    {
        "slug": "restaurant", "label": "Restaurant", "phrase": "un restaurant", "theme": "chaleureux", "icon": "couverts",
        "nom": "Le Comptoir", "tel": "06 39 98 12 41", "kicker": "Restaurant",
        "colors": {"brand": "#7A1E2C", "brand_deep": "#4E111B", "soft": "#F8F2EE", "ink": "#2A1A1C", "hero": "deep"},
        "h1": "Une cuisine de saison, à deux pas de chez vous.",
        "lead": "{nom} vous accueille à {ville} midi et soir : produits frais, plats faits maison et formule du midi en semaine.",
        "trust": ["Fait maison", "Produits frais", "Formule du midi"],
        "services_title": "La carte", "services_h2": "Ce que nous servons",
        "services": [
            ["Entrées du moment", "Selon le marché et la saison."],
            ["Plat du jour", "Une recette différente chaque jour, en semaine."],
            ["Viandes et poissons", "Cuisinés simplement, servis généreusement."],
            ["Assiettes végétariennes", "Des légumes de saison mis en valeur."],
            ["Desserts maison", "Préparés chaque matin par la cuisine."],
            ["Vins et boissons", "Une sélection courte et choisie."],
        ],
        "special_eb": "Infos pratiques", "special_h2": "Avant de venir", "special_p": "Tout ce qu’il faut savoir pour votre visite.",
        "special_style": "points",
        "special": [
            ["Réservation", "Conseillée le week-end, par téléphone ou par message."],
            ["Formule du midi", "Entrée et plat, ou plat et dessert, en semaine."],
            ["Groupes", "Menus sur demande pour vos repas de groupe et anniversaires."],
            ["Allergies", "Signalez-les à la réservation : nous adaptons les plats."],
        ],
        "place_title": "Nous trouver", "place_text": "Au centre de {ville}.",
        "hours": [["Mardi au samedi", "12 h – 14 h · 19 h – 22 h"], ["Dimanche", "12 h – 14 h"], ["Lundi", "Fermé"]],
        "contact_h2": "Réservez votre table", "contact_p": "Appelez ou envoyez un SMS avec le jour, l’heure et le nombre de couverts.",
        "cta": "Réserver une table", "sms": "Réserver par SMS",
    },
    {
        "slug": "boulangerie", "label": "Boulangerie", "phrase": "une boulangerie", "theme": "chaleureux", "icon": "epi",
        "nom": "Maison Lefèvre", "tel": "06 39 98 12 42", "kicker": "Boulangerie · Pâtisserie",
        "colors": {"brand": "#8A4B1F", "brand_deep": "#5C3013", "soft": "#FBF5EA", "ink": "#2B1D12", "hero": "soft"},
        "h1": "Du bon pain, cuit chaque matin à {ville}.",
        "lead": "{nom} pétrit et cuit sur place pains, viennoiseries et pâtisseries. Commandez vos gâteaux pour toutes vos occasions.",
        "trust": ["Fait sur place", "Cuit chaque matin", "Gâteaux sur commande"],
        "services_title": "En boutique", "services_h2": "Nos fabrications",
        "services": [
            ["Pains de tradition", "Baguettes et pains au levain, longue fermentation."],
            ["Pains spéciaux", "Céréales, seigle, complet, campagne."],
            ["Viennoiseries", "Croissants et pains au chocolat pur beurre."],
            ["Pâtisseries", "Tartes, éclairs et entremets du moment."],
            ["Gâteaux sur commande", "Anniversaires, baptêmes et fêtes de famille."],
            ["Le midi", "Sandwichs, quiches et formules à emporter."],
        ],
        "special_eb": "Commandes", "special_h2": "Commander un gâteau", "special_p": "Simple et rapide, sans vous déplacer deux fois.",
        "special_style": "steps",
        "special": [
            ["Choisissez", "Le gâteau, le parfum et le nombre de parts."],
            ["Envoyez votre commande", "Par SMS, idéalement 48 h à l’avance."],
            ["Nous confirmons", "Le prix et l’heure de retrait."],
            ["Retirez en boutique", "Votre gâteau est prêt à l’heure prévue."],
        ],
        "place_title": "La boutique", "place_text": "Au cœur de {ville}.",
        "hours": [["Mardi au samedi", "6 h 30 – 19 h 30"], ["Dimanche", "7 h – 13 h"], ["Lundi", "Fermé"]],
        "contact_h2": "Une commande, une question ?", "contact_p": "Envoyez un SMS avec votre commande et la date souhaitée, nous vous confirmons rapidement.",
        "cta": "Commander", "sms": "Commander par SMS",
    },
    {
        "slug": "fleuriste", "label": "Fleuriste", "phrase": "un fleuriste", "theme": "elegant", "icon": "fleur",
        "nom": "Fleurs d’Iris", "tel": "06 39 98 12 43", "kicker": "Artisan fleuriste",
        "colors": {"brand": "#3F6B4F", "brand_deep": "#24402F", "soft": "#F7F1F2", "ink": "#1F2A22", "hero": "soft"},
        "h1": "Des fleurs fraîches pour chaque moment de la vie.",
        "lead": "{nom} compose bouquets et créations florales à {ville} : anniversaires, mariages, deuils, plantes et livraison locale.",
        "trust": ["Fleurs fraîches", "Compositions sur mesure", "Livraison locale"],
        "services_title": "Créations", "services_h2": "Pour toutes les occasions",
        "services": [
            ["Bouquets du jour", "Composés chaque matin avec les fleurs de saison."],
            ["Mariages", "Bouquet de mariée, boutonnières et décoration."],
            ["Deuil", "Gerbes, couronnes et compositions, avec délicatesse."],
            ["Plantes", "Plantes vertes et fleuries, conseils d’entretien."],
            ["Entreprises et événements", "Décoration florale pour vos espaces et réceptions."],
            ["Livraison", "À {ville} et dans les communes voisines."],
        ],
        "special_eb": "Commande", "special_h2": "Commander un bouquet", "special_p": "Dites-nous l’occasion, nous imaginons la composition.",
        "special_style": "steps",
        "special": [
            ["L’occasion", "Anniversaire, remerciement, naissance, deuil…"],
            ["Votre budget", "Nous composons avec ce que vous souhaitez dépenser."],
            ["La date", "Retrait en boutique ou livraison."],
            ["La confirmation", "Nous vous envoyons la proposition avant de préparer."],
        ],
        "place_title": "La boutique", "place_text": "À {ville}, retrait sur place ou livraison.",
        "hours": [["Mardi au samedi", "9 h – 19 h"], ["Dimanche", "9 h – 13 h"], ["Lundi", "Fermé"]],
        "contact_h2": "Commandez votre bouquet", "contact_p": "Indiquez l’occasion, votre budget et la date : nous vous proposons une composition.",
        "cta": "Commander un bouquet", "sms": "Envoyer un message",
    },
    {
        "slug": "institut", "label": "Institut de beauté", "phrase": "un institut de beauté", "theme": "elegant", "icon": "lotus",
        "nom": "Institut Éclat", "tel": "06 39 98 12 44", "kicker": "Institut de beauté",
        "colors": {"brand": "#7A5683", "brand_deep": "#3E2A44", "soft": "#F6F1F7", "ink": "#24192A", "hero": "soft"},
        "h1": "Prendre soin de vous, en toute sérénité.",
        "lead": "{nom} vous accueille à {ville} pour vos soins du visage, épilations, manucure et massages bien-être.",
        "trust": ["Sur rendez-vous", "Produits professionnels", "Cabines privées"],
        "services_title": "Soins", "services_h2": "Nos soins",
        "services": [
            ["Soins du visage", "Nettoyage, hydratation et éclat, selon votre peau."],
            ["Épilations", "Cire ou méthode adaptée, pour toutes les zones."],
            ["Manucure", "Soin des mains, vernis classique ou semi-permanent."],
            ["Beauté des pieds", "Soin complet et pose de vernis."],
            ["Massages bien-être", "Un moment de détente, du dos au corps entier."],
            ["Maquillage", "Pour un événement, un mariage ou une séance photo."],
        ],
        "special_eb": "L’institut", "special_h2": "Un moment rien que pour vous", "special_p": "Dès votre arrivée, tout est pensé pour votre confort.",
        "special_style": "points",
        "special": [
            ["Accueil", "Nous faisons le point sur vos attentes avant chaque soin."],
            ["Hygiène", "Matériel désinfecté et linge changé à chaque cliente."],
            ["Produits", "Des gammes professionnelles choisies avec soin."],
            ["Conseils", "Les bons gestes pour prolonger les effets à la maison."],
        ],
        "place_title": "L’institut", "place_text": "À {ville}, sur rendez-vous.",
        "hours": [["Mardi au vendredi", "9 h 30 – 19 h"], ["Samedi", "9 h – 17 h"], ["Dimanche et lundi", "Fermé"]],
        "contact_h2": "Prenez rendez-vous", "contact_p": "Appelez ou envoyez un message avec le soin souhaité et vos disponibilités.",
        "cta": "Prendre rendez-vous", "sms": "Envoyer un message",
    },
]


def fill(text):
    """Échappe le texte puis remplace {nom} et {ville} par des zones personnalisables."""
    t = html.escape(text, quote=False)
    t = t.replace("{nom}", '<span data-f="nom"></span>').replace("{ville}", '<span data-f="ville"></span>')
    return t


def hero_tokens(c):
    t = _hero_tokens(c)
    if c["hero"] == "brand":
        t.update(hero_btn_bg="#FFFFFF", hero_btn_ink=c["brand_deep"])
    else:
        t.update(hero_btn_bg=c["brand"], hero_btn_ink="#FFFFFF")
    return t


def _hero_tokens(c):
    if c["hero"] == "dark":
        return dict(hero_bg="#141418", hero_ink="#FFFFFF", hero_muted="#B9BAC2", hero_kicker=c["brand"], hero_btn2="#FFFFFF")
    if c["hero"] == "brand":
        return dict(hero_bg=c["brand"], hero_ink="#FFFFFF", hero_muted="rgba(255,255,255,.82)", hero_kicker="rgba(255,255,255,.85)", hero_btn2="#FFFFFF")
    if c["hero"] == "deep":
        return dict(hero_bg=c["brand_deep"], hero_ink="#FFFFFF", hero_muted="rgba(255,255,255,.78)", hero_kicker="rgba(255,255,255,.8)", hero_btn2="#FFFFFF")
    return dict(hero_bg=c["soft"], hero_ink=c["ink"], hero_muted="#5E5B5F", hero_kicker=c["brand"], hero_btn2=c["ink"])


TEMPLATE = open(os.path.join(ROOT, "outils", "gabarit_modele.html"), encoding="utf-8").read()


def build(m):
    th = THEMES[m["theme"]]
    c = m["colors"]
    ht = hero_tokens(c)
    icon = ICONS[m["icon"]]
    services = "\n".join(
        f'        <article class="card"><span class="dot" aria-hidden="true"></span><h3>{fill(t)}</h3><p>{fill(d)}</p></article>'
        for t, d in m["services"])
    special_tag = "ol" if m["special_style"] == "steps" else "ul"
    special = "\n".join(f'        <li><div><b>{fill(t)}</b><span>{fill(d)}</span></div></li>' for t, d in m["special"])
    hours = "".join(f"<dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd>" for a, b in m["hours"])
    trust = "\n".join(f'      <li>{html.escape(t)}</li>' for t in m["trust"])
    digits = "".join(ch for ch in m["tel"] if ch.isdigit())
    defaults = json.dumps({"nom": m["nom"], "ville": "Villeneuve", "tel": m["tel"], "metier": m["label"]}, ensure_ascii=False)
    rep = {
        "FONTS": th["fonts"], "F_HEAD": th["head"], "F_BODY": th["body"],
        "HEAD_WEIGHT": th["head_weight"], "HEAD_TRANSFORM": th["head_transform"], "HEAD_SPACING": th["head_spacing"],
        "RADIUS": th["radius"], "BTN_RADIUS": th["btn_radius"],
        "BRAND": c["brand"], "BRAND_DEEP": c["brand_deep"], "SOFT": c["soft"], "INK": c["ink"],
        "HERO_BG": ht["hero_bg"], "HERO_INK": ht["hero_ink"], "HERO_MUTED": ht["hero_muted"],
        "HERO_KICKER": ht["hero_kicker"], "HERO_BTN2": ht["hero_btn2"],
        "HERO_BTN_BG": ht["hero_btn_bg"], "HERO_BTN_INK": ht["hero_btn_ink"],
        "TITLE": html.escape(f'{m["nom"]} · {m["label"]} à Villeneuve'),
        "LABEL": html.escape(m["label"]), "KICKER": html.escape(m["kicker"]),
        "ICON": icon, "H1": fill(m["h1"]), "LEAD": fill(m["lead"]), "TRUST": trust,
        "SERVICES_EB": html.escape(m["services_title"]), "SERVICES_H2": html.escape(m["services_h2"]), "SERVICES": services,
        "SPECIAL_EB": html.escape(m["special_eb"]), "SPECIAL_H2": html.escape(m["special_h2"]), "SPECIAL_P": html.escape(m["special_p"]),
        "SPECIAL_TAG": special_tag, "SPECIAL_CLASS": m["special_style"], "SPECIAL": special,
        "PLACE_TITLE": html.escape(m["place_title"]), "PLACE_TEXT": fill(m["place_text"]), "HOURS": hours,
        "CONTACT_H2": html.escape(m["contact_h2"]), "CONTACT_P": html.escape(m["contact_p"]),
        "CTA": html.escape(m["cta"]), "SMS": html.escape(m["sms"]), "TEL_DIGITS": digits, "DEFAULTS": defaults,
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
        build(m)
    with open(os.path.join(ROOT, "outils", "metiers.json"), "w", encoding="utf-8") as f:
        json.dump([{"slug": m["slug"], "label": m["label"], "phrase": m["phrase"]} for m in METIERS], f, ensure_ascii=False, indent=2)
    print(f"{len(METIERS)} modèles générés")
