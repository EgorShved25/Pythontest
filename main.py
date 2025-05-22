from fastapi import FastAPI, HTTPException, Response
from starlette.responses import RedirectResponse
from database import SessionLocal, URL
from models import URLRequest



app = FastAPI()

# Создаём короткую ссылку
@app.post("/")
async def create_short_url(item: URLRequest): # Получает данные от клиента

    db = SessionLocal()
    new_url = URL(original_url=item.url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    # Используем id как короткий код
    short_id = str(new_url.id)
    new_url.short_id = short_id
    db.commit()
    db.close()

    return Response(
        content=f'{{"short_url": "http://127.0.0.1:8000/{short_id}"}}',
        media_type="application/json",
        status_code=201
    )

# Перенаправляем по короткой ссылке
@app.get("/{short_id}")
async def redirect(short_id: str):
    db = SessionLocal()
    try:
        url_entry = db.query(URL).filter(URL.short_id == short_id).first()
    finally:
        db.close()
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL не найден")

    # Возвращаем ответ с кодом 307 и заголовком Location
    return Response(
        status_code=307,
        headers={"Location": url_entry.original_url}
    )