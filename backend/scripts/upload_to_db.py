"""Upload init-data.sql vers MariaDB (local ou Railway)."""
import argparse
import pymysql
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Chemins
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SQL_FILE = DATA_DIR / "init-data.sql"

# Charger .env
ENV_PATH = SCRIPT_DIR.parent / ".env"
load_dotenv(ENV_PATH)

def parse_args():
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Upload init-data.sql vers MariaDB"
    )
    
    parser.add_argument(
        "--local",
        action="store_true",
        help="Se connecter à la base de données locale (via docker-compose)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        help="Hostname MariaDB (pour Railway)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=3306,
        help="Port MariaDB (défaut: 3306)"
    )
    
    parser.add_argument(
        "--user",
        type=str,
        help="Utilisateur MariaDB"
    )
    
    parser.add_argument(
        "--password",
        type=str,
        help="Mot de passe MariaDB"
    )
    
    parser.add_argument(
        "--database",
        type=str,
        default="concerts_db",
        help="Nom de la base de données (défaut: concerts_db)"
    )
    
    return parser.parse_args()


def get_connection_params(args):
    """Retourne les paramètres de connexion selon les arguments."""
    
    if args.local:
        # Connexion locale via docker-compose
        # Utilise les valeurs par défaut du .env
        return {
            "host": "mariadb",
            "port": 3306,
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": os.getenv("MYSQL_DATABASE", "concerts_db")
        }
    
    elif args.host:
        # Connexion distante (Railway)
        if not args.user or not args.password:
            print("❌ Erreur: --user et --password requis pour connexion distante")
            sys.exit(1)
        
        return {
            "host": args.host,
            "port": args.port,
            "user": args.user,
            "password": args.password,
            "database": args.database
        }
    
    else:
        print("❌ Erreur: Utilise --local ou spécifie --host")
        sys.exit(1)


def execute_sql_file(connection, sql_file: Path):
    """Exécute un fichier SQL."""
    
    print(f"📄 Lecture de {sql_file.name}...")
    
    if not sql_file.exists():
        raise FileNotFoundError(f"Fichier SQL non trouvé: {sql_file}")
    
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_content = f.read()
    
    print("⚙️  Exécution du SQL...")
    
    try:
        with connection.cursor() as cursor:
            # Supprimer les commentaires
            lines = []
            for line in sql_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    lines.append(line)
            
            # Rejoindre et splitter sur ";\n" pour éviter les ; dans les BLOB
            cleaned_sql = ' '.join(lines)
            statements = [s.strip() for s in cleaned_sql.split(';') if s.strip()]
            
            print(f"  {len(statements)} statements à exécuter...")
            
            for idx, statement in enumerate(statements, 1):
                print(f"  Statement {idx}/{len(statements)}...", end="\r")
                cursor.execute(statement)
            
            connection.commit()
            print("\n✅ SQL exécuté avec succès!")
    
    except Exception as e:
        connection.rollback()
        print(f"\n❌ Erreur SQL: {e}")
        raise


def verify_upload(connection):
    """Vérifie que les données sont bien insérées."""
    
    print("\n🔍 Vérification de l'upload...")
    
    with connection.cursor() as cursor:
        # Compter concerts
        cursor.execute("SELECT COUNT(*) FROM concerts")
        concert_count = cursor.fetchone()[0]
        
        # Compter pages
        cursor.execute("SELECT COUNT(*) FROM program_pages")
        page_count = cursor.fetchone()[0]
        
        print(f"  ✓ {concert_count} concert(s) inséré(s)")
        print(f"  ✓ {page_count} page(s) insérée(s)")
        
        if concert_count == 0 or page_count == 0:
            print("\n⚠️  Attention: Aucune donnée insérée!")
            return False
        
        return True


def main():
    """Fonction principale."""
    args = parse_args()
    
    print("🚀 Upload vers MariaDB")
    print("=" * 50)
    
    # Paramètres de connexion
    conn_params = get_connection_params(args)
    print(f"\n🔌 Connexion à {conn_params['host']}:{conn_params['port']}")
    print(f"   Base: {conn_params['database']}")
    print(f"   User: {conn_params['user']}")
    
    try:
        # Connexion
        connection = pymysql.connect(**conn_params)
        print("✓ Connecté!\n")
        
        # Exécuter le SQL
        execute_sql_file(connection, SQL_FILE)
        
        # Vérifier
        verify_upload(connection)
        
        print("\n✅ Upload terminé avec succès!")
        
    except pymysql.Error as e:
        print(f"\n❌ Erreur de connexion MariaDB: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
    
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
            print("🔌 Connexion fermée")


if __name__ == "__main__":
    main()