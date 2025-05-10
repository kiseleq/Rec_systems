import streamlit as st 
import requests
import pandas as pd
from requests.exceptions import ConnectionError

ip_api = "127.0.0.1"
port_api = "500"

# Заголовок приложения
st.title("Recommendation system (development)")

# Ввод данных
st.write("Enter your type:")

# Выпадающее меню для выбора класса билета
type = st.selectbox("Person type", [1, 2, 3, 4, 5])

# Кнопка для отправки запроса
if st.button("Make recommendation"):
    # Подготовка данных для отправки
    data = {
        "type": int(type),
    }

    try:
        # Отправка запроса к Flask API
        response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)

        # Проверка статуса ответа
        if response.status_code == 200:
            predictions = response.json()
            df = pd.DataFrame(predictions)
            st.dataframe(df)
        else:
            st.error(f"Request failed with status code {response.status_code}")
    except ConnectionError as e:
        st.error(f"Failed to connect to the server")
