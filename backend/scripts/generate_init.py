"""Génère init-data.sql depuis les PNG et PDF."""
import os
from pathlib import Path
from PIL import Image
from datetime import date

# Chemins
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
PHOTOS_DIR = DATA_DIR / "concert_photos"
PDF_PATH = DATA_DIR / "programme musique contemporaine - Ensemble Vocal Squillo.pdf"
OUTPUT_SQL = DATA_DIR / "init-data.sql"

# Metadata du concert (à personnaliser)
CONCERT_TITLE = "Concert Squillo - Sacré swing"
CONCERT_DATE = "2026-02-06"  # Format YYYY-MM-DD
CONCERT_LOCATION = "TEMPLE DE PORT ROYAL, 18 BOULEVARD ARAGO 75013 PARIS"


def bytes_to_hex(data: bytes) -> str:
    """Convertit bytes en format hexadécimal pour SQL."""
    return "0x" + data.hex()


def get_image_dimensions(png_path: Path) -> tuple[int, int]:
    """Récupère les dimensions d'une image PNG."""
    with Image.open(png_path) as img:
        return img.size  # (width, height)


def generate_sql():
    """Génère le fichier SQL avec les INSERT."""
    
    print("🔍 Vérification des fichiers...")
    
    # Vérifier PDF
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF non trouvé: {PDF_PATH}")
    
    # Lister et trier les PNG
    png_files = sorted(PHOTOS_DIR.glob("*.png"))
    if not png_files:
        raise FileNotFoundError(f"Aucun PNG trouvé dans {PHOTOS_DIR}")
    
    print(f"✓ PDF trouvé: {PDF_PATH.name}")
    print(f"✓ {len(png_files)} PNG trouvés")
    
    # Lire le PDF
    print("\n📄 Lecture du PDF...")
    with open(PDF_PATH, "rb") as f:
        pdf_data = f.read()
    pdf_hex = bytes_to_hex(pdf_data)
    pdf_size = len(pdf_data)
    print(f"  Taille: {pdf_size / 1024 / 1024:.2f} MB")
    
    # Générer le SQL
    print(f"\n✍️  Génération de {OUTPUT_SQL}...")
    
    with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
        f.write("-- Auto-généré par generate_init.py\n")
        f.write("-- Ne pas éditer manuellement\n\n")
        
        f.write("USE concerts_db;\n\n")
        
        # INSERT concert
        f.write("-- Insertion du concert\n")
        f.write("INSERT INTO concerts ")
        f.write("(title, concert_date, location, is_published, pdf_full, pdf_filename, pdf_size) ")
        f.write("VALUES (\n")
        f.write(f"  '{CONCERT_TITLE}',\n")
        f.write(f"  '{CONCERT_DATE}',\n")
        f.write(f"  '{CONCERT_LOCATION}',\n")
        f.write(f"  TRUE,\n")
        f.write(f"  {pdf_hex},\n")
        f.write(f"  '{PDF_PATH.name}',\n")
        f.write(f"  {pdf_size}\n")
        f.write(");\n\n")
        
        # Récupérer l'ID du concert inséré
        f.write("SET @concert_id = LAST_INSERT_ID();\n\n")
        
        # INSERT pages
        f.write("-- Insertion des pages PNG\n")
        
        for idx, png_file in enumerate(png_files, start=1):
            print(f"  Processing {png_file.name}...")
            
            # Lire PNG
            with open(png_file, "rb") as pf:
                png_data = pf.read()
            
            png_hex = bytes_to_hex(png_data)
            png_size = len(png_data)
            width, height = get_image_dimensions(png_file)
            
            f.write(f"-- Page {idx}: {png_file.name}\n")
            f.write("INSERT INTO program_pages ")
            f.write("(concert_id, page_number, png_data, png_size, width, height) ")
            f.write("VALUES (\n")
            f.write(f"  @concert_id,\n")
            f.write(f"  {idx},\n")
            f.write(f"  {png_hex},\n")
            f.write(f"  {png_size},\n")
            f.write(f"  {width},\n")
            f.write(f"  {height}\n")
            f.write(");\n\n")
    
    print(f"\n✅ Fichier généré: {OUTPUT_SQL}")
    print(f"   Taille totale: {OUTPUT_SQL.stat().st_size / 1024 / 1024:.2f} MB")
    print("\n📋 Prochaine étape:")
    print("   python scripts/upload_to_db.py --local")


if __name__ == "__main__":
    try:
        generate_sql()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        exit(1)