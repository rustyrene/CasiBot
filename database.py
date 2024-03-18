from surrealdb import Surreal
from datetime import datetime

async def connect():
    db = Surreal("ws://localhost:8000/rpc")
    await db.connect()
    await db.signin({"user": "root", "pass": "root"})
    await db.use("python", "casio_bot")
    return db

async def get_balance(username):
    ex = await exists(username)
    if ex:
        db = await connect()
        query = await db.query(f'SELECT balance FROM USER WHERE username="{username}"')
        result = int(query[0]["result"][0]["balance"])
        return result
    else:
        raise Exception("User is not already registered")
    
async def update_balance(username, amount):
    ex = await exists(username)
    if ex:
        db = await connect()
        balance = await get_balance(username=username)
        new_balance = balance + amount if balance + amount > 0 else 0
        query = await db.query(f'UPDATE USER SET balance={new_balance} WHERE username="{username}"')
        new_balance = int(query[0]["result"][0]["balance"])
    else:
        raise Exception("Error updaing the balance")
    
async def create_user(username):
    exists = await exists()
    if exists:
        raise Exception(f"User with username {username} already exists")
    else:
        db = await connect()
        await db.create("USER", {
            "username":f"{username}",
            "balance": 5000,
            "created_at": str(datetime.now())
        })
    
async def exists(username):
    db = await connect()
    exists = await db.query(f'SELECT * FROM USER WHERE username="{username}"')
    exists = len(exists[0]["result"])
    if exists == 0:
        return False
    else:
        return True
