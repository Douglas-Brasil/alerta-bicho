from fastapi.responses import FileResponse
from pathlib import Path
CONTROLLERS_DIR = Path(__file__).resolve().parent

def get_home_page():
    print(f"\033[44m REDIRECIONANDO PRA HOME PAGE \033[0m")
    
    # Subindo de /controllers para /src e depois para a /view
    html_path = CONTROLLERS_DIR.parent / "view" / "home" /"home.html"
    
    return FileResponse(html_path.resolve())