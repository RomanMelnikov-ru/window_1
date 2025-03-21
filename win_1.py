import streamlit as st
import plotly.graph_objects as go

# Заголовок приложения
st.title("Визуализация оконного профиля с импостами и водоотливными отверстиями")

# Ввод исходных данных
st.sidebar.header("Исходные данные")
L = st.sidebar.number_input("Длина профиля (м):", min_value=1.0, value=3.0, step=0.1)
num_points = st.sidebar.number_input("Количество импостов:", min_value=1, value=2, step=1)
min_drainage_spacing = st.sidebar.number_input("Минимальное расстояние между водоотливными отверстиями (м):", min_value=0.1, value=0.45, step=0.05)
max_drainage_spacing = st.sidebar.number_input("Максимальное расстояние между водоотливными отверстиями (м):", min_value=0.1, value=0.65, step=0.05)
min_distance_to_impost = st.sidebar.number_input("Минимальное расстояние между импостом и водоотливным отверстием (м):", min_value=0.01, value=0.04, step=0.01)

# Фиксированные точки импостов
imposts = [i * L / (num_points + 1) for i in range(1, num_points + 1)]
imposts = [0.0] + imposts + [L]  # Добавляем начальную и конечную точки

# Функция для создания водоотливных отверстий с учётом ограничений
def create_drainage_points(imposts, L, min_drainage_spacing, max_drainage_spacing, min_distance_to_impost):
    drainage_points = []

    # Добавляем точки по краям на расстоянии 0.16 м, если они не слишком близко к импостам
    if abs(0.16 - imposts[0]) >= min_distance_to_impost:
        drainage_points.append(0.16)
    if abs(L - 0.16 - imposts[-1]) >= min_distance_to_impost:
        drainage_points.append(L - 0.16)

    # Если количество импостов чётное, добавляем точку по центру, если она не слишком близко к импостам
    if num_points % 2 == 0:
        center = L / 2
        too_close = any(abs(center - impost) < min_distance_to_impost for impost in imposts)
        if not too_close:
            drainage_points.append(center)

    # Распределяем точки на остальных участках
    for i in range(len(imposts) - 1):
        start = imposts[i] + min_distance_to_impost
        end = imposts[i + 1] - min_distance_to_impost
        segment_length = end - start

        # Если длина отрезка позволяет добавить точки
        if segment_length >= min_drainage_spacing:
            # Количество точек на отрезке
            num_drainage = int(segment_length // max_drainage_spacing)
            if num_drainage > 0:
                # Равномерное распределение точек
                spacing = segment_length / (num_drainage + 1)
                for j in range(1, num_drainage + 1):
                    point = start + j * spacing
                    # Проверяем, что точка не слишком близко к другим водоотливным отверстиям
                    if all(abs(point - dp) >= min_drainage_spacing for dp in drainage_points):
                        drainage_points.append(point)

    # Убираем дубликаты и сортируем
    drainage_points = sorted(list(set(drainage_points)))
    return drainage_points

# Создаём водоотливные отверстия
drainage_points = create_drainage_points(imposts, L, min_drainage_spacing, max_drainage_spacing, min_distance_to_impost)

# Создание графика
fig = go.Figure()

# Добавление линии (оконный профиль)
fig.add_trace(go.Scatter(
    x=imposts,
    y=[0] * len(imposts),
    mode='lines+markers',
    line=dict(color='blue'),
    marker=dict(color='red', size=10),
    name='Импосты'
))

# Добавление водоотливных отверстий
fig.add_trace(go.Scatter(
    x=drainage_points,
    y=[0] * len(drainage_points),
    mode='markers',
    marker=dict(color='green', size=10),
    name='Водоотливные отверстия'
))

# Добавление подписей координат для импостов
for i, point in enumerate(imposts):
    fig.add_annotation(
        x=point,
        y=0.2,
        text=f"{point:.2f} м",
        showarrow=False,
        font=dict(size=12, color="red"),
        yshift=10
    )

# Добавление подписей координат для водоотливных отверстий
for i, point in enumerate(drainage_points):
    fig.add_annotation(
        x=point,
        y=-0.2,
        text=f"{point:.2f} м",
        showarrow=False,
        font=dict(size=12, color="green"),
        yshift=-10
    )

# Добавление подписей расстояний между водоотливными отверстиями
for i in range(len(drainage_points) - 1):
    distance = drainage_points[i + 1] - drainage_points[i]
    midpoint = (drainage_points[i] + drainage_points[i + 1]) / 2
    fig.add_annotation(
        x=midpoint,
        y=-0.1,
        text=f"{distance:.2f} м",
        showarrow=False,
        font=dict(size=12, color="black"),
        yshift=-20
    )

# Настройка внешнего вида графика
fig.update_layout(
    title="Распределение импостов и водоотливных отверстий",
    xaxis_title="Длина, м",
    yaxis_title="",
    showlegend=True,
    yaxis=dict(showticklabels=False),
    height=600,
    margin=dict(l=40, r=40, t=40, b=40)
)

# Отображение графика в Streamlit
st.plotly_chart(fig)