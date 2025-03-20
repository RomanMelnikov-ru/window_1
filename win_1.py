import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Заголовок приложения
st.title("Распределение водоотливных отверстий и осей импостов")

# Ввод параметров через Streamlit
st.sidebar.header("Параметры")
L = st.sidebar.number_input("Длина профиля (м)", value=3.0, min_value=1.0, step=0.1)
edge_point_distance = st.sidebar.number_input("Расстояние от края профиля до водоотливного отверстия (м)", value=0.16, min_value=0.0, step=0.01)
min_distance_red = st.sidebar.number_input("Минимальное расстояние между водоотливными отверстиями (м)", value=0.45, min_value=0.0, step=0.01)
max_distance_red = st.sidebar.number_input("Максимальное расстояние между водоотливными отверстиями (м)", value=0.65, min_value=0.0, step=0.01)
min_distance_between_old_new = st.sidebar.number_input("Минимальное расстояние между водоотливными отверстиями и осью импоста (м)", value=0.04, min_value=0.0, step=0.01)
num_new_points = st.sidebar.number_input("Количество импостов", value=4, min_value=1, step=1)

# Центральная точка
center_point = L / 2

# Точки от краев
left_edge_point = edge_point_distance
right_edge_point = L - edge_point_distance

# Список для хранения всех красных точек
red_points = [left_edge_point, center_point, right_edge_point]

# Расстояние между крайней точкой и центральной
distance_between_edge_and_center = center_point - left_edge_point

# Количество дополнительных красных точек
num_additional_points = int(distance_between_edge_and_center / max_distance_red)

# Расстояние между дополнительными красными точками
additional_point_distance = distance_between_edge_and_center / (num_additional_points + 1)

# Добавление дополнительных красных точек
for i in range(1, num_additional_points + 1):
    red_points.append(left_edge_point + i * additional_point_distance)
    red_points.append(right_edge_point - i * additional_point_distance)

# Сортировка красных точек
red_points.sort()

# Округление до 0.01 м
red_points = [round(point, 2) for point in red_points]

# Равномерное распределение синих точек
blue_points = np.linspace(0, L, num_new_points + 2)[1:-1]  # Исключаем края, так как они уже есть
blue_points = [round(point, 2) for point in blue_points]

# Функция для проверки и корректировки красных точек
def adjust_red_points(red_points, blue_points, min_distance_red, max_distance_red, min_distance_between_old_new):
    # Проверка расстояния между красными и синими точками
    for blue_point in blue_points:
        for i in range(len(red_points)):
            if abs(red_points[i] - blue_point) < min_distance_between_old_new:
                # Смещаем красную точку вправо или влево
                if red_points[i] < blue_point:
                    red_points[i] = blue_point - min_distance_between_old_new
                else:
                    red_points[i] = blue_point + min_distance_between_old_new
                # Округляем до 0.01 м
                red_points[i] = round(red_points[i], 2)

    # Проверка расстояния между красными точками
    for i in range(len(red_points) - 1):
        distance = red_points[i + 1] - red_points[i]
        if distance < min_distance_red:
            # Смещаем правую точку вправо
            red_points[i + 1] = red_points[i] + min_distance_red
            red_points[i + 1] = round(red_points[i + 1], 2)
        elif distance > max_distance_red:
            # Добавляем новую точку посередине
            new_point = (red_points[i] + red_points[i + 1]) / 2
            red_points.insert(i + 1, round(new_point, 2))

    # Убедимся, что точки не выходят за пределы линии
    red_points = [max(min(point, L), 0) for point in red_points]
    return red_points

# Корректировка красных точек
red_points = adjust_red_points(red_points, blue_points, min_distance_red, max_distance_red, min_distance_between_old_new)

# Построение графика
fig, ax = plt.subplots(figsize=(10, 2))
ax.plot([0, L], [0, 0], 'k-', linewidth=2)  # Линия

# Отображение красных точек и подписей
for point in red_points:
    ax.plot(point, 0, 'ro')  # Красные точки
    ax.text(point, 0.02, f'{point:.2f}m', ha='center')  # Подписи

# Отображение синих точек и подписей
for point in blue_points:
    ax.plot(point, 0, 'bo')  # Синие точки
    ax.text(point, -0.02, f'{point:.2f}m', ha='center', color='blue')  # Подписи

# Отображение расстояний между красными точками
for i in range(len(red_points) - 1):
    distance = red_points[i + 1] - red_points[i]
    mid_point = (red_points[i] + red_points[i + 1]) / 2
    ax.text(mid_point, 0.05, f'{distance:.2f}m', ha='center', color='red')

ax.set_yticks([])
ax.set_xlabel('Длина прошиля (м)')
ax.grid(True)

# Отображение графика в Streamlit
st.pyplot(fig)

# Вывод списка точек
st.write("водоотливные отверстия:", red_points)
st.write("Оси импостов:", blue_points)
