import asyncio

import httpx


async def check_message_censorship(content: str, censor_url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await asyncio.wait_for(
                client.post(censor_url, json={"text": content}),
                timeout=1,
            )
            # Check the response
            if response.status_code == 200:
                return response.json()
            else:
                return "error"
        except Exception:
            return "error"
