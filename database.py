from surrealdb import Surreal
from datetime import datetime

async def connect():
    """Example of how to use the SurrealDB client."""
    db = Surreal("ws://localhost:8000/rpc")
    await db.connect()
    await db.signin({"user": "root", "pass": "root"})
    await db.use("python", "casio_bot")
    return db

async def get_balance(username):
    db = await connect()
    query = await db.query(f'SELECT balance FROM USER WHERE username="{username}"')
    try:
        result = int(query[0]["result"][0]["balance"])
        return result
    except Exception:
        raise Exception("No user balance found")
    
async def update_balance(username, amount):
    db = await connect()
    balance = await get_balance(username=username)
    new_balance = balance + amount if balance + amount > 0 else 0
    query = await db.query(f'UPDATE USER SET balance={new_balance} WHERE username="{username}"')
    try:
        new_balance = int(query[0]["result"][0]["balance"])
    except Exception:
        raise Exception("Error updaing the balance")
    
async def create_user(username):
    db = await connect()
    exists = await db.query(f'SELECT * FROM USER WHERE username="{username}"')
    exists = len(exists[0]["result"])
    if exists == 0:
        await db.create("USER", {
            "username":f"{username}",
            "balance": 5000,
            "created_at": str(datetime.now())
        })
    else:
        raise Exception(f"User with username {username} already exists")