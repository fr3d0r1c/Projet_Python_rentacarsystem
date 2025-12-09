import os 

def generer_txt_arborescence(nom_fichier_sortie="structure_projet.txt"):
    dossiers_ignores = {'__pycache__', '.git', '.vscode', '.idea', 'venv', 'env', 'bin'}

    chemin_actuel = os.getcwd()
    nom_projet = os.path.basename(chemin_actuel)

    with open(nom_fichier_sortie, "w", encoding="utf-8") as f:
        f.write(f"ARBORESCENCE DU PROJET : {nom_projet}\n")
        f.write("=" * 50 + "\n\n")

        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in dossiers_ignores]

            niveau = root.count(os.sep)
            indent = "│   " * niveau

            nom_dossier = os.path.basename(root)
            if nom_dossier == ".":
                f.write(f"📁 {nom_projet}/\n")
            else:
                f.write(f"{indent}├── 📁 {nom_dossier}/\n")

            sub_indent = "│   " * (niveau + 1)
            for fichier in files:
                if fichier.endswith(('.py', '.json', '.md', '.txt')) and fichier != "generate_tree.py":
                    f.write(f"{sub_indent}├── 📄 {fichier}\n")

    print(f"✅ Succès ! L'arborescence a été sauvegardée dans : {nom_fichier_sortie}")

if __name__ == "__main__":
    generer_txt_arborescence()