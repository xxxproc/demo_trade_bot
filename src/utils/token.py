import aiohttp
from create_bot import blockchain

async def get_token_info(address, network=blockchain):
    url = f"https://api.geckoterminal.com/api/v2/networks/{network}/tokens/{address}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return await r.json() if r.status == 200 else False