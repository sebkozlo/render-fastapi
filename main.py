from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

origin = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextPayload(BaseModel):
    content: str

@app.post("/check")
async def check_ai_content(payload: TextPayload):
    # zapytanie do modelu
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # możesz użyć "gpt-4o" jeśli chcesz większą dokładność
        messages=[
            {"role": "system", "content": "Oszacuj w ilu procentach podany tekst został wygenerowany przez AI. Odpowiadaj tylko jedną liczbą całkowitą od 0 do 100 bez żadnego opisu."},
            {"role": "user", "content": payload.content},
        ]
    )

    # wyciągnięcie odpowiedzi
    raw = completion.choices[0].message.content.strip()
    # upewnij się, że jest liczba
    try:
        percent = int("".join([c for c in raw if c.isdigit()]))
    except:
        percent = 0

    return {"probability": f"{percent}%"}
