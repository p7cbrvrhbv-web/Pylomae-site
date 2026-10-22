#!/usr/bin/env python3
"""Hooks Claude Code de PYLOMAE (réglés dans .claude/settings.json).

avant : refuse les modifications à la main des fichiers générés (modeles/, outils/metiers.json).
apres : relance outils/generer_apercus.py quand le gabarit ou le script vient d'être modifié.

Claude Code envoie sur l'entrée standard un JSON qui contient tool_input.file_path.
Code de sortie 2 = message renvoyé à Claude (refus avant, erreur de génération après).
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GENERES = re.compile(r"^(modeles/[^/]+/(index\.html|contenu\.json)|outils/metiers\.json)$")
SOURCES = {"outils/gabarit_apercu.html", "outils/generer_apercus.py"}


def chemin_relatif(data):
    chemin = (data.get("tool_input") or {}).get("file_path") or ""
    if not chemin:
        return ""
    rel = os.path.relpath(os.path.abspath(chemin), ROOT)
    return rel.replace("\\", "/")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    rel = chemin_relatif(data)

    if mode == "avant" and GENERES.match(rel):
        print(
            f"{rel} est généré par outils/generer_apercus.py : une modification à la main serait écrasée. "
            "Modifie outils/gabarit_apercu.html ou les données du script, la génération se relance toute seule.",
            file=sys.stderr,
        )
        return 2

    if mode == "apres" and rel in SOURCES:
        res = subprocess.run(
            [sys.executable, os.path.join(ROOT, "outils", "generer_apercus.py")],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )
        if res.returncode != 0:
            print("La régénération des aperçus a échoué :\n" + (res.stderr or res.stdout)[-2000:], file=sys.stderr)
            return 2
        print(res.stdout.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
