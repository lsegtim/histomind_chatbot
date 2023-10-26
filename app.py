import pandas as pd
from bson import ObjectId
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chatbot import initialize_bot, get_response_chatbot

from googletrans import Translator

translator = Translator()

# show all columns
pd.set_option('display.max_columns', None)

app = FastAPI()

print("Starting server...")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = initialize_bot()


def translate_message(message):
    return translator.translate(message, dest='en').text


def translate_message_back(message, dest='en'):
    return translator.translate(message, dest=dest).text


class ChatbotModel(BaseModel):
    message: str = Field(...)
    local: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

        schema_extra = {
            "example": {
                "message": "Hallo, wie geht es dir?",
                "local": "de"
            }
        }


# Chatbot
@app.post("/chatterbot")
async def get_chatterbot(chatbot_model: ChatbotModel = Body(...)):
    response = str(translate_message(get_response_chatbot(chatbot_model.message, chatbot)))
    response = translate_message_back(response, chatbot_model.local)

    return {"response": response}
