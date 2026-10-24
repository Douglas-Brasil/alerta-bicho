from pathlib import Path
from fastapi import Request
from src.models.auth import AuthSupaBase

base_path = Path(__file__).resolve().parent.parent.parent
env_path = base_path / '.env'

class Controller_Auth(AuthSupaBase):
    def auth_jwt(self, request: Request) -> bool:
        # Recupera o token diretamente do cookie (ex: "access_token" ou "session_id")
        token = request.cookies.get("access_token") or request.cookies.get("session_id")
        
        if not token:
            
            return False
        

        return self.auth_session_user(token)

    def auth_user(self, user, session=None):
        if session is None:
            session = {}
            
        result = self.auth_user_login(user)
        if result.get("success"):
            self.set_session(result, session)
        return result

    def set_session(self, auth_user, session):
        session["access_token"] = auth_user["session"].access_token
        session["refresh_token"] = auth_user["session"].refresh_token
        session["user_email"] = auth_user["email"]
        session["user_id"] = auth_user["id"]