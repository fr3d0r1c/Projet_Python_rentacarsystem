import os

def generer_arbre_epure(dossier_racine=".", fichier_sortie="structure_projet.txt"):
    IGNORE_DIRS = {
        '.git', '.vscode', '.idea', '__pycache__',
        '.venv', 'venv', 'env', 'VirtualEnv',
        'Lib', 'Scripts', 'Include', 'share', 'etc',
        'dist', 'build', 'egg-info',
        'site-packages', '__pypackages__',
        '.streamlit'
    }

    IGNORE_FILES = {
        '.DS_Store', 'Thumbs.db',
        '.gitignore', '.python-version',
        '__init__.py'
    }

    IGNORE_EXT = (
        '.pyc', '.pyo', '.pyd',
        '.dll', '.so', '.exe',
        '.dist-info', '.egg-info',
        '.css.map', '.js.map'
    )

    with open(fichier_sortie, "w", encoding="utf-8") as f:
        nom_projet = os.path.basename(os.path.abspath(dossier_racine))
        f.write(f"📂 PROJET : {nom_projet}\n")
        f.write("=" * 50 + "\n")

        for root, dirs, files in os.walk(dossier_racine):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS
                       and not d.endswith('.dist-info') 
                       and not d.endswith('.egg-info')]
            
            niveau = root.replace(dossier_racine, '').count(os.sep)
            indent = '│   ' * niveau

            if root != dossier_racine:
                nom_dossier = os.path.basename(root)
                f.write(f"{indent}├── 📁 {nom_dossier}/\n")
                sub_indent = indent + "│   "
            else:
                sub_indent = ""

            for fichier in sorted(files):
                if fichier not in IGNORE_FILES and not fichier.endswith(IGNORE_EXT):
                    f.write(f"{sub_indent}├── 📄 {fichier}\n")

    print(f"✅ Arborescence propre générée dans : {fichier_sortie}")

if __name__ == "__main__":
    generer_arbre_epure()