# Рекомендательные системы (недвижимость)
---
Проект по предмету "Рекоммендательные системы"

Запустим сервис apartment-reccomendation-service:

docker build -t apartment-reccomendation-service:latest .   

docker run -d --name apartment-reccomendation-service -p 500:5000 apartment-reccomendation-service:latest