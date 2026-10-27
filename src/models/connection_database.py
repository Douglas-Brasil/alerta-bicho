import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from src.models.user import User

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=False)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError(
        f"SUPABASE_URL ou SUPABASE_KEY não encontradas. "
        f"Defina como variáveis de ambiente ou crie {env_path}"
    )

supabase: Client = create_client(url, key)