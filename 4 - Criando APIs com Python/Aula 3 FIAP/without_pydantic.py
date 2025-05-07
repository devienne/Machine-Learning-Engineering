# Estudando sobre o poetry & pyvenv
# Agora vamos de pydantic

## checando um db sem pydantic

data = {
    "username": "alice",
    "email": "alice@examplo.com",
    "age": 30,
    "is_active":  False
}

#validacao manual sem pydantic
def validate_data(data):
    if not isinstance(data.get("username"), str):
        raise ValueError("username deve ser uma string.")
    if not isinstance(data.get("email"), str) or "@" not in data["email"] :
        raise ValueError("email invalido.")
    if not isinstance(data.get("age"), int):
        raise ValueError("Idade invalida")
    if not isinstance(data.get("is_active"), bool):
        raise ValueError("is_active deve ser um booleano.")
    return True

try:
    validate_data(data)
except ValueError as e:
    print(f"Erro na validação: {e}")

