from pydantic import BaseModel, EmailStr

data = {
    "username": "alice",
    "email": "alice@examplo.com",
    "age": "30",
    "is_active": "TrUe"
}

# definindo o modelo com pydantic
class UserModel(BaseModel):
    username: str
    email: EmailStr
    age: int
    is_active: bool

# validação automática e conversão de tipos
try:
    user = UserModel(**data)
    print(user)
except Exception as e:
    print(f"Erro na validação: {e}")


