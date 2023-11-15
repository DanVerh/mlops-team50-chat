### Web chat with AI-enabled message censor

# Tech spec

This is a web chat application, which

- posts all chat messages to a single public channel in a format "nickname: message"
- for every posted message, sends a async http REST call to censorship REST endpoint with the text of the message as input, and receives "Good" or "Bad" as an output.
- puts 🟢 or 🔴 near the message based on censor response, if no response is received for 1 second - puts ❓
- accepts simple nickname as a login

# Prerequisites

1. python 3.10, you can install one on Mac with `brew install python@3.10`
2. poetry, can be installed with `pipx install poetry`
3. black formatter `pipx install black`, optionally you can also install a black extenstion for you favorite IDE

## Dev Environment Setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
poetry install --no-root
cp example.env .env
```

`example.env` defaults to a fake censorship endpoint.
To use a real model locally, change `CENSOR_URL` to `http://127.0.0.1:8001/censorship_status` after launching the model's web API

## Running Locally

run `uvicorn main:app --reload` and open http://127.0.0.1:8000/ in your browser
