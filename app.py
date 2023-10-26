import os

import motor.motor_asyncio
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

# load environment variables
from dotenv import load_dotenv

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.histomind

data_length = 100000

chatbot = initialize_bot()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# message: "message"
# local: "en"

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
    # response = str(translate_message(get_response_chatbot(chatbot_model.message, chatbot)))
    # response = translate_message_back(response, chatbot_model.local)
    response = "Hello"
    return {"response": response}


@app.get("/chatbot/{message}")
async def get_chatbot(message: str):
    # # detect language
    # # language = detect(message)
    # if language == "en" or language == "de" or language == "ta":
    #     response = str(get_response_chatbot(message, chatbot))
    # else:
    response = "Sorry, I don't understand that."
    return {"response": response}
