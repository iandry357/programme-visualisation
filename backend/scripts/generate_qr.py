# generate_qr.py
import segno

# generate_qr.py
import os
import segno

def create_qr(url: str):
    output_dir = "/app/data"              # ← emplacement monté = dossier ./data sur l'hôte
    os.makedirs(output_dir, exist_ok=True)  # crée le dossier s'il n'existe pas

    filename_base = "qr_concert_1"
    png_path = os.path.join(output_dir, f"{filename_base}.png")
    svg_path = os.path.join(output_dir, f"{filename_base}.svg")

    print(f"Génération QR pour : {url}")
    print(f"Dossier de sortie : {output_dir}")

    qr = segno.make(url, error='h')

    # PNG
    qr.save(
        png_path,
        scale=12,
        border=4,
        dark="darkblue",
        light="white"
    )
    print(f"PNG créé → {png_path}")

    # SVG (vectoriel, idéal pour impression)
    qr.save(
        svg_path,
        scale=8,
        border=4,
        dark="darkblue",
        light="white"
    )
    print(f"SVG créé → {svg_path}")

    # Optionnel : liste les fichiers pour debug
    print("Fichiers dans /app/data :")
    print(os.listdir(output_dir))


if __name__ == "__main__":
    url = "https://frontend-programme-visualisation-production.up.railway.app/concerts/1"
    create_qr(url)