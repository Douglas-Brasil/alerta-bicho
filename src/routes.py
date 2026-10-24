from fastapi import APIRouter, Depends, Request, Response, status, Form, File, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from src.controllers.home_controller import get_home_page
from src.controllers.login_controller import get_login_page, register_user, login_user, logout_user
from src.controllers.auth_controller import Controller_Auth
from src.controllers.AI_controller import classify



print("\033[42m [BOOT] Arquivo de rotas carregado na memória \033[0m")

router = APIRouter()
auth_controller = Controller_Auth()

def verify_authentication(request: Request) -> bool:
    print("\033[41m [REQUEST] Entrou na verificação de autenticação \033[0m")
    return auth_controller.auth_jwt(request)

@router.get("/")
def home(is_authenticated: bool = Depends(verify_authentication)):
    print(f"\033[44m [REQUEST] Rota Home chamada. Autenticado? {is_authenticated} \033[0m")
    if is_authenticated:
        return get_home_page()
    return RedirectResponse(url="/login", status_code=303)

@router.get("/login")
def login(is_authenticated: bool = Depends(verify_authentication)):
    print(f"\033[44m [REQUEST] Rota Login chamada. Autenticado? {is_authenticated} \033[0m")
    if is_authenticated:
        return RedirectResponse(url="/", status_code=303)

    return get_login_page()


@router.post("/register/user")
def register(email: str = Form(...), password: str = Form(...)):
    print(f"\033  \033[0m")
    return register_user(email=email, password=password)



@router.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    print("\033[41m ROTA POST DE LOGAR \033[0m")
    return login_user(email=email, password=password)

@router.post("/login/logout")
def logout():
    print("\033[41m ROTA DE DESLOGAR \033[0m")
    return logout_user()

@router.post("/model")
def model(file: UploadFile = File(...), is_authenticated: bool = Depends(verify_authentication)):
    print("\033[41m ROTA DE ENVIAR IMAGEM PRA IA \033[0m")

    if is_authenticated:
        return classify(file)
    return RedirectResponse(url="/login", status_code=303)

    
