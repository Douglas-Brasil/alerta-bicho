from .connection_database import *

class AuthSupaBase:
    def auth_user_login(self, user):
        try:
            response = supabase.auth.sign_in_with_password({
                "email": user.email,
                "password": user.password
            })

            return {
                "success": True,
                "user": response.user,
                "email": response.user.email,
                "id": response.user.id,
                "session": response.session
            }

        except Exception as e:
            print(f"\033[41mErro ao fazer login: {e}\033[0m")
            return {
                "success": False,
                "error": str(e)
            }

    def auth_session_user(self, token: str) -> bool:
        try:
            if not token:
                print("\033[41mToken não fornecido\033[0m")
                return False
            
            # Valida o JWT no Supabase utilizando o token
            response = supabase.auth.get_user(token)
            
            if response and response.user:
                return True
            
            print("\033[41mToken inválido\033[0m")
            return False

        except Exception as e:
            print(f"\033[41mErro ao validar token: {e}\033[0m")
            return False