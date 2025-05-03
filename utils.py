import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.inspection import permutation_importance
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import ttest_ind
from sklearn.preprocessing import MinMaxScaler

def search_history(user_id, user_type):
    # Определяем диапазон для типа пользователя
    type_settings = {
        1: (850, 1200),
        2: (500, 4000),
        3: (5000, 7500),
        4: (7500, 8000),
        5: (7000, 9250)
    }

    # Получаем минимальное и максимальное значение для объектов
    if user_type in type_settings:
        obj_min, obj_max = type_settings[user_type]
    else:
        raise ValueError(f"Неизвестный тип пользователя: {user_type}")
    
    num_rows = random.randint(100, 150)  # Количество строк для пользователя
    
    data = []
    for _ in range(num_rows):
        action = random.choices(["view", "like"], weights=[9, 1])[0]  # Соотношение 9:1
        obj_id = random.randint(obj_min, obj_max)
        data.append([user_id, action, obj_id])

    # Создание DataFrame
    user_actions = pd.DataFrame(data, columns=["user_id", "action", "obj_id"])

    return user_actions

def make_recommendations(homes_fixed, user_actions):

    # Объединение данных по объектам
    homes_fixed.set_index('id', inplace=True)

    # Группировка действий пользователей
    user_profiles = {}
    for user, actions in user_actions.groupby('user_id'):
        interacted_obj_ids = actions['obj_id'].unique()
        interacted_objects = homes_fixed.loc[homes_fixed.index.intersection(interacted_obj_ids)]

        if not interacted_objects.empty:
            user_profiles[user] = interacted_objects.mean(axis=0)

    # Преобразование профилей пользователей в DataFrame
    user_profiles_df = pd.DataFrame.from_dict(user_profiles, orient='index')

    # Вычисление косинусного сходства между пользователем и объектами
    similarity_matrix = cosine_similarity(user_profiles_df, homes_fixed)

    # Создание DataFrame с рекомендациями
    recommendations = pd.DataFrame(similarity_matrix, index=user_profiles_df.index, columns=homes_fixed.index)

    # Выбор 10 объектов, с которыми пользователь не взаимодействовал
    final_recommendations = {}
    for user in user_profiles_df.index:
        interacted = set(user_actions[user_actions['user_id'] == user]['obj_id'])
        sorted_recs = recommendations.loc[user].drop(index=interacted).nlargest(10)
        final_recommendations[user] = sorted_recs.index.tolist()

    # Вывод рекомендаций (id)
    return final_recommendations

print("utils.py загружен")
