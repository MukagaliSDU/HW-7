import json
from jose import jwt

from fastapi import Cookie, FastAPI, Form, Request, Response, templating, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()


@app.get("/")
def root(request: Request):
    pass


def encode(user_id: str) -> str:
    json_user = {"user_id": user_id}
    encode_user = jwt.encode(json_user, "nfactorial", "HS256")
    return encode_user


def decode(token: str) -> int:
    data = jwt.decode(token, "nfactorial", "HS256")
    return data["user_id"]


@app.post("/signup")
def post_sign_up(
    email: str = Form(),
    full_name: str = Form(),
    password: str = Form(),
):
    user = User(email=email, full_name=full_name, password=password)
    users_repository.save(user)
    return Response(status_code=200)


@app.post('/login')
def post_login(username: str = Form(), password: str = Form()):
    user = users_repository.get_by_email(username)
    if user.password == password:
        token = encode(user.id)
        return{
            "access_token": token,
            "type": "bearer",
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")


@app.get("/profile")
def get_profile(token: str = Depends(oauth2_schema)):
    user_id = decode(token)
    user = users_repository.get_by_id(user_id)
    return {
        "user_id": user.id,
        "email": user.email,
        "fullname": user.full_name,
    }


@app.get("/flowers")
def get_flowers():
    return flowers_repository.get_all()


@app.post("/flowers")
def post_flowers(name: str = Form(), count: int = Form(), cost: int = Form()):
    flower = Flower(name=name, count=count, cost=cost)
    flower = flowers_repository.save(flower)

    return{
        "id": flower.id
    }


@app.post("/cart/items")
def post_items(flower_id: int = Form(), token: str = Depends(oauth2_schema), cart: str = Cookie(default='[]')):
    cart_json = json.loads(cart)
    response = Response(status_code=200)
    if flower_id != None:
        cart_json.append(flower_id)
        new_cart = json.dumps(cart_json)
        response.set_cookie(key=token, value=new_cart)
    return response


@app.get("/cart/items")
def get_carts(request: Request, token: str = Depends(oauth2_schema)):
    cart = request.cookies.get(token)

    print(f"get : {cart}")
    flowers = flowers_repository.get_list(cart)
    total = 0
    for i in flowers:
        total += i.cost

    return None
