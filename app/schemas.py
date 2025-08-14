from pydantic import BaseModel, Field

class LoginForm(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=5, max_length=100)

class AgentConfig(BaseModel):
    name: str = Field(min_length=1)
    role: str = Field(min_length=10)
    goal: str = Field(min_length=10)
    back_story: str = Field(min_length=10)