from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi import HTTPException
from src.models.user import User
from src.models.login import Login


def get_login_page():
    print(f"\033[44m CARREGANDO PAGINA DE LOGIN[0m")
    templates = Jinja2Templates(directory="src/view")
    return templates.TemplateResponse("login.html")

def register_user(email: str, password: str) -> RedirectResponse:
    new_user = User(email=email, password=password)
    result = Login.register(new_user)

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    # Instancia o redirecionamento
    response = RedirectResponse(url="/", status_code=303)

    # Define o cookie caso haja sessão no cadastro (auto-login)
    if result.get("session"):
        print("\033[41m CRIOU O USUARIO \033[0m")
        access_token = result["session"].access_token
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=3600,
            samesite="lax",
            secure=True
        )

    return response


def login_user(email: str, password: str) -> RedirectResponse:
    # 1. Tenta autenticar o usuário no Supabase
    user = User(email=email, password=password)
    result = Login.authenticate(user)  # Ajuste o método conforme sua classe Login

    if not result.get("success"):
        raise HTTPException(
            status_code=400, 
            detail=result.get("error", "Credenciais inválidas.")
        )

    # 2. Cria a resposta de redirecionamento
    response = RedirectResponse(url="/", status_code=303)
    print("\033[41m LOGOU O USUARIO \033[0m")
    # 3. Define o cookie de acesso na resposta de redirecionamento
    access_token = result.get("session").access_token
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=3600,
        samesite="lax",
        secure=True  # Recomendado em produção com HTTPS
    )

    return response


def logout_user() -> RedirectResponse:
    # 1. Encerra a sessão no Supabase
    Login.logout()

    # 2. Cria a resposta de redirecionamento para a página de login
    response = RedirectResponse(url="/login", status_code=303)

    # 3. Remove o cookie de acesso do navegador definindo max_age=0
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax"
    )

    return response
