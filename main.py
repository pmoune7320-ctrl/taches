#!/usr/bin/env python3
"""Gestionnaire de tâches en ligne de commande."""
import argparse
import json
from pathlib import Path

FICHIER = Path(__file__).parent / "taches.json"


def charger(fichier=FICHIER):
    if fichier.exists():
        return json.loads(fichier.read_text(encoding="utf-8"))
    return []


def sauvegarder(taches, fichier=FICHIER):
    fichier.write_text(
        json.dumps(taches, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def ajouter(taches, texte):
    nouvel_id = max((t["id"] for t in taches), default=0) + 1
    tache = {"id": nouvel_id, "texte": texte, "faite": False}
    taches.append(tache)
    return tache


def terminer(taches, id_tache):
    for t in taches:
        if t["id"] == id_tache:
            t["faite"] = True
            return True
    return False


def supprimer(taches, id_tache):
    avant = len(taches)
    taches[:] = [t for t in taches if t["id"] != id_tache]
    return len(taches) < avant


def afficher(taches):
    if not taches:
        print("Aucune tâche.")
        return
    for t in taches:
        etat = "[x]" if t["faite"] else "[ ]"
        print(f'{t["id"]:>3} {etat} {t["texte"]}')


def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches")
    sub = parser.add_subparsers(dest="commande", required=True)

    p_add = sub.add_parser("ajouter", help="Ajouter une tâche")
    p_add.add_argument("texte", help="Description de la tâche")

    sub.add_parser("lister", help="Lister les tâches")

    p_done = sub.add_parser("terminer", help="Marquer une tâche comme faite")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("supprimer", help="Supprimer une tâche")
    p_del.add_argument("id", type=int)

    args = parser.parse_args()
    taches = charger()

    if args.commande == "ajouter":
        t = ajouter(taches, args.texte)
        sauvegarder(taches)
        print(f'Tâche {t["id"]} ajoutée.')
    elif args.commande == "lister":
        afficher(taches)
    elif args.commande == "terminer":
        if terminer(taches, args.id):
            sauvegarder(taches)
            print(f"Tâche {args.id} terminée.")
        else:
            print(f"Tâche {args.id} introuvable.")
    elif args.commande == "supprimer":
        if supprimer(taches, args.id):
            sauvegarder(taches)
            print(f"Tâche {args.id} supprimée.")
        else:
            print(f"Tâche {args.id} introuvable.")


if __name__ == "__main__":
    main()
