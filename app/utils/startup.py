from sqlalchemy.orm import Session
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .. import models
from ..database import Base, engine, SessionLocal
from ..ai.LLMAgent.MyAgent.utils.load_config import load_aget_config


def _insert_agent_config():
   Base.metadata.create_all(bind=engine)

   with SessionLocal() as db:
      username = "system"
      existing = db.query(models.Config).filter(models.Config.username == username).first()
      if existing:
         print("System Data already exists in db!")
         return
      config = load_aget_config()
      db.add(models.Config(
         username=username,
         name=config["agent"]["name"],
         role=config["agent"]["goal"],
         goal=config["agent"]["goal"],
         back_story=config["agent"]["back_story"]
      ))
      db.commit()
      print("Added system data to config table")
         


@asynccontextmanager
async def lifespan(app: FastAPI):
   _insert_agent_config()
   yield
