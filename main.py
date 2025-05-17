from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import zipfile

app = FastAPI()

# Healthcheck endpoint для корня
@app.get("/")
def healthcheck():
    return {"status": "ok"}

# Пример CORS (если нужен)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или укажи свой фронт
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint для загрузки изображения и генерации иконок (пример)
@app.post("/favicon")
async def generate_favicon(file: UploadFile = File(...)):
    # Сохраняем загруженный файл во временную директорию
    tmp_dir = "tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    file_path = os.path.join(tmp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Тут логика генерации favicon и иконок
    # ... (добавь свою генерацию сюда)

    # Пример: возвращаем оригинальный файл (замени на zip после генерации)
    # Если генерируешь архив icons.zip, меняй путь
    zip_path = os.path.join(tmp_dir, "icons.zip")
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(file_path, arcname=file.filename)
    return FileResponse(zip_path, media_type="application/zip", filename="icons.zip")
