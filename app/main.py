import asyncio
import logging
import os
import random
import time
from uuid import uuid4

from censor import check_message_censorship
from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import CensorRequest, Message, UserName
from pydantic import ValidationError
from ws import SocketManager

load_dotenv()

CENSOR_URL = os.getenv("CENSOR_URL")

if not CENSOR_URL:
    raise EnvironmentError("CENSOR_URL should be set")

logger = logging.getLogger("uvicorn")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
manager = SocketManager()


@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/api/current_user")
def get_user(request: Request):
    return request.cookies.get("X-Authorization")


@app.get("/chat")
def get_chat(request: Request, login: str = Depends(get_user)):
    if not login:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("chat.html", {"request": request, "login": login})


@app.post("/api/register")
def register_user(user: UserName, response: Response):
    response.set_cookie(key="X-Authorization", value=user.username, httponly=True)


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
    sender = get_user(websocket)  # type: ignore
    if sender:
        await manager.connect(websocket, sender)
        try:
            while True:
                json_data = await websocket.receive_json()
                message_id = str(uuid4())
                message = Message(content=json_data.get("message"))
                try:
                    # Validate the message data using the Message model
                    # Broadcast the validated message
                    data = {
                        "sender": sender,
                        "message": message.content,
                        "message_id": message_id,
                        "censorship_status": "pending",
                    }
                    await manager.broadcast(data)
                except (ValidationError, ValueError) as e:
                    # Handle the validation or value error
                    await websocket.send_json({"error": str(e)})
                # Update the censorship mark based on the response
                start_time = time.time()
                censorship_response = await check_message_censorship(
                    message.content, CENSOR_URL
                )
                end_time = time.time()
                latency_ms = (end_time - start_time) * 1000  # Convert to milliseconds
                logger.info(f"Censorship check latency: {latency_ms:.2f} ms")
                logger.info(f"Censorship status: {censorship_response}")
                update_data = {
                    "message_id": message_id,
                    "censorship_status": censorship_response,
                }
                # Broadcast the update
                await manager.broadcast(update_data)
        except WebSocketDisconnect:
            manager.disconnect(websocket, sender)
            await manager.broadcast({"sender": sender, "content": "left"})


@app.post("/api/censor")
async def fake_censor(request: CensorRequest):
    response_choice = random.choices(
        ["Good", "Bad", "Timeout"], weights=[40, 40, 20], k=1
    )[0]

    if response_choice == "Timeout":
        # Simulate a timeout by sleeping longer than the client is willing to wait
        await asyncio.sleep(3)
        raise HTTPException(status_code=504, detail="Request timed out")
    else:
        await asyncio.sleep(0.5)
        return response_choice
