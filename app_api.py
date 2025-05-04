'''
Давайте создадим простое API с тремя ручками: одна для предсказания выживания (/predict), 
другая для получения количества сделанных запросов (/stats), и третья для проверки работы API (/health).

Шаг 1: Установка необходимых библиотек
Убедитесь, что у вас установлены необходимые библиотеки:
pip install fastapi uvicorn pydantic scikit-learn pandas

Шаг 2: Создание app_api.py
Шаг 3: Запустите ваше приложение: python app_api.py
Шаг 4: Тестирование API
Теперь вы можете протестировать ваше API с помощью curl или любого другого инструмента для отправки HTTP-запросов.

Проверка работы API (/health)
curl -X GET http://127.0.0.1:5000/health
curl -X GET http://127.0.0.1:5000/stats
curl -X POST http://127.0.0.1:5000/predict_model -H "Content-Type: application/json" -d "{\"type\": 3}"

'''

from fastapi import FastAPI, Request, HTTPException
# import pickle
import pandas as pd
from pydantic import BaseModel

app = FastAPI()

# Загрузка модели из файла utils
from utils import rec_system

# Счетчик запросов
request_count = 0

# Модель для валидации входных данных
class PredictionInput(BaseModel):
    type: int

@app.get("/stats")
def stats():
    return {"request_count": request_count}

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict_model")
def predict_model(input_data: PredictionInput):
    global request_count
    request_count += 1
    try:
        print("Получен запрос с типом:", input_data.type)
        new_data = pd.DataFrame({
            'Type': [input_data.type]
        })
        print("DataFrame создан:", new_data)

        recommendation = rec_system(new_data)
        print("Рекомендации получены:", recommendation.head())
        
        return recommendation.to_dict(orient="records")
    except Exception as e:
        import traceback
        print("Произошла ошибка:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка: {e}")




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)