from src.models.user import User
from .connection_database import supabase  # Certifique-se de que a instância do Supabase é importada daqui

# backend/models/login.py
class Login:
     @staticmethod
     def register(user: User) -> dict:
          
          
          try:
               response = supabase.auth.sign_up({
                    "email": user.get_email(),
                    "password": user.get_password(),
                    "options": {
                         "data": {
                              "name": user.get_name()  # Ajuste o método conforme o nome no seu objeto User (ex: get_name ou name)
                         }
                    }
               })

               if response.user:
                    print(f"\033[44m CRIOU USER NOME: {user.get_name()} \033[0m")
                    
                    return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,  # Pode ser None se o e-mail exigir confirmação
                    "message": "Usuário cadastrado com sucesso!"
                    }
               

               return {"success": False, "error": "Não foi possível criar o usuário."}

          except Exception as e:
               print(f"\033[44m {str(e)} \033[0m")
               return {"success": False, "error": str(e)}
          
     @staticmethod
     def authenticate(user: User) -> dict:
          try:
               # Autentica o usuário com e-mail e senha no Supabase
               response = supabase.auth.sign_in_with_password({
                    "email": user.get_email(),
                    "password": user.get_password()
               })

               if response.user and response.session:
                    print(f"\033[42m USUÁRIO AUTENTICADO \033[0m")
                    return {
                    "success": True,
                    "user": response.user,
                    "session": response.session,
                    "message": "Login realizado com sucesso!"
                    }

               return {"success": False, "error": "Credenciais inválidas."}

          except Exception as e:
               print(f"\033[41m ERRO NO LOGIN: {str(e)} \033[0m")
               return {"success": False, "error": str(e)}
          
     @staticmethod
     def logout() -> dict:
          try:
               supabase.auth.sign_out()
               print(f"\033[43m USUÁRIO DESLOGADO \033[0m")
               return {"success": True, "message": "Logout realizado com sucesso!"}
          except Exception as e:
               print(f"\033[41m ERRO NO LOGOUT: {str(e)} \033[0m")
               return {"success": False, "error": str(e)}