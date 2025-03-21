import streamlit as st
import plotly.graph_objects as go

# Заголовок приложения
st.title("Визуализация оконного профиля с импостами и водоотливными отверстиями")

# Ввод данных
L = 3.0  # Длина профиля
num_points = st.number_input("Введите количество точек (импостов):", min_value=1, value=4, step=1)
min_drain_dist = st.number_input("Минимальное расстояние между водоотливными точками (м):", min_value=0.1, value=0.45, step=0.01)
max_drain_dist = st.number_input("Максимальное расстояние между водоотливными точками (м):", min_value=0.1, value=0.65, step=0.01)
min_distance_to_impost = st.number_input("Минимальное расстояние от водоотливной точки до импоста (м):", min_value=0.04, value=0.04, step=0.01)

# Равномерное распределение точек (импостов)
points_imposts = [L * (i + 1) / (num_points + 1) for i in range(num_points)]

# Добавление водоотливных отверстий
points_drain = [0.16, L - 0.16]  # Крайние точки
if num_points % 2 == 0:  # Если количество импостов четное, добавляем точку по середине
    points_drain.append(L / 2)

# Функция для корректировки положения точек
def adjust_point_position(point, points_imposts, min_distance=0.04):
    for impost in points_imposts:
        if abs(point - impost) < min_distance:
            # Корректируем положение точки
            if point < impost:
                point = impost - min_distance
            else:
                point = impost + min_distance
    return point

# Функция для добавления дополнительных водоотливных точек
def add_additional_drain_points(points, points_imposts, min_dist=0.45, max_dist=0.65, min_distance_to_impost=0.04):
    points.sort()  # Сортируем точки
    new_points = []
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        distance = end - start
        if distance > max_dist:
            # Добавляем точки симметрично
            num_new_points = int(distance // max_dist)
            spacing = distance / (num_new_points + 1)
            for j in range(1, num_new_points + 1):
                new_point = start + j * spacing
                # Корректируем положение точки, если она слишком близко к импосту
                new_point = adjust_point_position(new_point, points_imposts, min_distance_to_impost)
                new_points.append(new_point)
    # Добавляем новые точки в общий список и сортируем
    points.extend(new_points)
    points.sort()

# Добавляем дополнительные водоотливные точки
add_additional_drain_points(points_drain, points_imposts, min_drain_dist, max_drain_dist, min_distance_to_impost)

# Создание графика
fig = go.Figure()

# Добавление линии профиля
fig.add_trace(go.Scatter(
    x=[0, L], y=[0, 0],
    mode='lines',
    line=dict(color='blue', width=2),
    name='Оконный профиль'
))

# Добавление линий высотой 1.0 м от точек импостов
for point in points_imposts:
    fig.add_trace(go.Scatter(
        x=[point, point], y=[0, 0.5],
        mode='lines',
        line=dict(color='red', width=2),
        name='Линия от импоста'
    ))

# Добавление точек (импостов)
for point in points_imposts:
    fig.add_trace(go.Scatter(
        x=[point], y=[0],
        mode='markers+text',
        marker=dict(color='red', size=10),
        text=[f"({point:.2f}, 0)"],
        textposition="top center",
        name='Импост'
    ))

# Добавление водоотливных отверстий
for point in points_drain:
    fig.add_trace(go.Scatter(
        x=[point], y=[0],
        mode='markers+text',
        marker=dict(color='blue', size=10),
        text=[f"({point:.2f}, 0)"],
        textposition="bottom center",
        name='Водоотливное отверстие'
    ))

# Добавление подписей расстояний между водоотливными точками
for i in range(len(points_drain) - 1):
    start = points_drain[i]
    end = points_drain[i + 1]
    distance = end - start
    midpoint = (start + end) / 2
    fig.add_annotation(
        x=midpoint, y=0.1,
        text=f"{distance:.2f} м",
        showarrow=False,
        font=dict(size=12, color="black")
    )

# Настройка внешнего вида графика
fig.update_layout(
    xaxis=dict(range=[-0.1, L + 0.1], showgrid=False),
    yaxis=dict(range=[-0.2, 1.2], showgrid=False, zeroline=True),
    showlegend=False,
    height=500,
    margin=dict(l=20, r=20, t=40, b=20)
)

# Отображение графика
st.plotly_chart(fig)
