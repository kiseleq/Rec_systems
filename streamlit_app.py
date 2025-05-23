import streamlit as st 
import requests
import pandas as pd
import pydeck as pdk
from requests.exceptions import ConnectionError
from collections import namedtuple

# Настройки API
ip_api = "127.0.0.1"
port_api = "500"

# Сайдбар с вводом параметров
st.sidebar.title("🔧 Параметры поиска")

Row = namedtuple("Row", ["code", "label"])
type = st.sidebar.selectbox(
    "Выберите социальный класс клиента:",
    [
        Row(1, "Lower class"),
        Row(2, "Working class"),
        Row(3, "Middle class"),
        Row(4, "Upper middle class"),
        Row(5, "Upper class")
    ],
    format_func=lambda x: x.label
).code

run_button = st.sidebar.button("🔍 Подобрать рекомендации")

# Основной заголовок
st.title("🏠 Recommendation System")
st.markdown("Добро пожаловать в демо рекомендательной системы недвижимости! Выберите параметр в сайдбаре и получите подборку подходящих вариантов.")

# Если нажали кнопку
if run_button:
    data = {
        "type": int(type),
    }

    try:
        response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)

        if response.status_code == 200:
            predictions = response.json()

            if predictions:
                df = pd.DataFrame(predictions)

                # Добавим отформатированную цену без дробей и с пробелами
                df['formatted_price'] = df['price'].apply(lambda x: format(x, ',.0f').replace(',', ' '))

                st.success(f"🎉 Найдено {len(df)} рекомендаций")

                # Топ-3 первых вариантов
                st.subheader("🏡 Топ-3 предложения")

                top3 = df.head(3)
                for _, row in top3.iterrows():
                    st.markdown(f"""
                    **💰 Цена:** {row['formatted_price']} ₽  
                    📐 **Площадь:** {row['area']} м²  
                    🛏️ **Комнат:** {row['rooms']}  
                    📍 **Координаты:** {row['geo_lat']}, {row['geo_lon']}  
                    --- 
                    """)

                # Отображение полной таблицы
                st.subheader("📊 Все рекомендации")
                st.dataframe(df)

                # Карта с точками фиксированного размера через pydeck
                st.subheader("🗺️ Карта объектов")

                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position="[geo_lon, geo_lat]",
                    get_color="[255, 255, 0, 255]",  # Яркий жёлтый, непрозрачный
                    get_radius=30,
                    pickable=True
                )

                view_state = pdk.ViewState(
                    latitude=df['geo_lat'].mean(),
                    longitude=df['geo_lon'].mean(),
                    zoom=11,
                    pitch=0
                )

                tooltip = {
                    "html": "<b>ID:</b> {id}<br><b>Цена:</b> {formatted_price} ₽<br><b>Площадь:</b> {area} м²",
                    "style": {
                        "backgroundColor": "rgba(50, 50, 50, 0.8)",
                        "color": "white"
                    }
                }

                st.pydeck_chart(pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    tooltip=tooltip
                ))

            else:
                st.warning("😔 По заданным параметрам ничего не найдено.")
        else:
            st.error(f"Ошибка: {response.status_code}")
    except ConnectionError:
        st.error("🚨 Не удалось подключиться к серверу")

# Футер
st.markdown("---")
st.markdown("Разработано 📌 [Development team] | ITMO 2025")
