from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

items = []

class Item(BaseModel):
    name: str
    description: str = None
    price: float = None
    quantity: int = None


app = FastAPI(
  title="My FastAPI",
  version="1.0.0",
  description="Exemplo de API com FastAPI"
)

# banco de dados dos usuários
users = {
    "user1":"password1",
    "user2":"password2"
}

security = HTTPBasic()

def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    if username in users and users[username] == password:
        return username
    raise HTTPException(
        status_code = status.HTTP_401_UNALTHORIZED,
        details = "Credenciais inválidas",
        headers = {"WWW-Authenticate":"Basic"},
    )

# mensagem de boas vindas
@app.get("/")
async def home():
    return "Hello, FastAPI"

# exige usuário e senha para acessar essa rota
@app.get("/hello")
async def hello(username: str = Depends(verify_password)):
    return {"message":f"Hello, {username}"}

# get para retornar os items salvos na memória
@app.get("/items")
async def get_items():
    return items

# post para incluir novos dados na lista de itens salvos
@app.post("/items", status_code=201)
async def create_item(item: Item):
    items.append(item.dict())
    return item

# put para atualizar item (tem que dar 
# o indice do item na lista de items) 
@app.put("/items/{item_id}")
async def update_item(item_id:int, item:Item):
    if 0 <= item_id <= len(items):
        items[item_id].update(item.dict())
        return items[item_id]
    raise HTTPException(status_code=404, detail="Item não encontrado")


# delete para deletar item (tem que dar 
# o indice do item na lista de items) 
@app.delete("/items/{item_id}")
async def update_item(item_id:int):
    if 0 <= item_id <= len(items):
        removed_item = items.pop(item_id)
        return removed_item
    raise HTTPException(status_code=404, detail="Item não encontrado")



