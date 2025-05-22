from pydantic import BaseModel

# Модель для получения данных от пользователя
class URLRequest(BaseModel):
    url: str
