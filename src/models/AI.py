from .connection_database import *


def get_animal_by_id(id_animal: int):
    try:
        # Tenta buscar convertendo explicitamente para int
        id_num = int(id_animal)
        
        response = (
            supabase.table("animais")
            .select("*")
            .eq("id", id_num)  # Garante que vai como inteiro
            .execute()
        )
        
        print("Resposta bruta do Supabase:", response) # <- Adicione este print para depurar
        
        dados = response.data
        if not dados:
            print(f"Nenhum animal encontrado com o ID {id_num}.")
            return None
            
        animal = dados[0]
        print(f"Animal encontrado: {animal['nome_popular']}")
        return animal

    except Exception as e:
        print(f"Erro ao buscar o animal no banco de dados: {e}")
        return None