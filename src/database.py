from create_bot import redis
     
class Users:
    def __init__(self, user_id: int):
        self.id = user_id

    async def get_user_balance(self):
        try:
            balance = await redis.get(f"{self.id}:balance")
            balance = int(balance.decode("utf-8"))
            return balance
        except:
            await redis.set(f"{self.id}:balance", 1000)
            return 1000
        
    async def get_user_token_ca(self):
        token_ca = await redis.get(f"{self.id}:token_ca")
        token_ca = token_ca.decode("utf-8") if token_ca else None
        return token_ca
    
    async def get_user_buy_usd_supply(self):
        buy_usd_sum = await redis.get(f"{self.id}:buy_usd_supply")
        buy_usd_sum = int(buy_usd_sum.decode("utf-8")) if buy_usd_sum else None
        return buy_usd_sum
    
    async def get_user_buy_token_supply(self):
        buy_token_supply = await redis.get(f"{self.id}:buy_token_supply")
        buy_token_supply = int(buy_token_supply.decode("utf-8")) if buy_token_supply else None
        return buy_token_supply

    async def set_token_ca(self, token_ca: str):
        await redis.set(f"{self.id}:token_ca", token_ca)
    
    async def buying_token(self, buy_dollars_quantity: int | float, buy_token_quantity: int | float):
        await redis.incrby(f"{self.id}:balance", -buy_dollars_quantity)
        await redis.incrby(f"{self.id}:buy_usd_supply", buy_dollars_quantity)
        await redis.incrby(f"{self.id}:buy_token_supply", buy_token_quantity)
    
    async def selling_token(self, buy_token_supply: int | float, price: int | float):
        await redis.incrby(f"{self.id}:balance", int(round(buy_token_supply*price, 0)))

        await redis.delete(f"{self.id}:token_ca")
        await redis.delete(f"{self.id}:buy_usd_supply")
        await redis.delete(f"{self.id}:buy_token_supply")