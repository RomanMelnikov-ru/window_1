import streamlit as st
import plotly.graph_objects as go

# Функция для построения графика
def plot_graph(L, edge_distance, min_distance, max_distance, num_new_points, min_distance_to_new_points):
    # Центр линии
    center = L / 2

    # Новая группа точек
    new_points = [round(i * L / (num_new_points + 1), 2) for i in range(1, num_new_points + 1)]

    # Блок для четного количества новых точек
    if num_new_points % 2 == 0:
        points = [edge_distance, center, L - edge_distance]
        distance_between_edge_and_center = center - edge_distance
        desired_distance = (min_distance + max_distance) / 2
        num_additional_points = int(distance_between_edge_and_center / desired_distance)
        uniform_distance = distance_between_edge_and_center / (num_additional_points + 1)
        uniform_distance = round(uniform_distance, 2)

        current_position = edge_distance
        for _ in range(num_additional_points):
            current_position += uniform_distance
            points.append(current_position)

        points_right = [L - p for p in points if p < center]
        points.extend(points_right)
        points = sorted(points)

    # Блок для нечетного количества новых точек
    else:
        points = [edge_distance, L - edge_distance]
        distance_between_edges = L - 2 * edge_distance
        desired_distance = (min_distance + max_distance) / 2
        num_additional_points = int(distance_between_edges / desired_distance)
        uniform_distance = distance_between_edges / (num_additional_points + 1)
        uniform_distance = round(uniform_distance, 2)

        current_position = edge_distance
        for _ in range(num_additional_points // 2):
            current_position += uniform_distance
            points.append(current_position)

        current_position = L - edge_distance
        for _ in range(num_additional_points // 2):
            current_position -= uniform_distance
            points.append(current_position)

        points = sorted(points)

    # Корректировка основных точек
    for i in range(len(points)):
        for new_point in new_points:
            if abs(points[i] - new_point) < min_distance_to_new_points:
                if points[i] < new_point:
                    points[i] = new_point - min_distance_to_new_points
                else:
                    points[i] = new_point + min_distance_to_new_points
                points[i] = round(points[i], 2)

    # Убедимся, что точки не выходят за границы линии
    points = [max(min(p, L - edge_distance), edge_distance) for p in points]

    # Создание графика с помощью Plotly
    fig = go.Figure()

    # Линия
    fig.add_trace(go.Scatter(
        x=[0, L], y=[0, 0], mode='lines', line=dict(color='black', width=2), name='Линия'
    ))

    # Основные точки
    fig.add_trace(go.Scatter(
        x=points, y=[0] * len(points), mode='markers', marker=dict(color='blue', size=10), name='Основные точки'
    ))

    # Новые точки
    fig.add_trace(go.Scatter(
        x=new_points, y=[0] * len(new_points), mode='markers', marker=dict(color='red', size=10), name='Новые точки'
    ))

    # Подписи для основных точек
    for p in points:
        fig.add_annotation(
            x=p, y=-0.02, text=f'{p:.2f}m', showarrow=False, font=dict(color='blue', size=10), yshift=10
        )

    # Подписи для новых точек
    for p in new_points:
        fig.add_annotation(
            x=p, y=0.02, text=f'{p:.2f}m', showarrow=False, font=dict(color='red', size=10), yshift=10
        )

    # Подписи расстояний между основными точками
    for i in range(len(points) - 1):
        distance = points[i + 1] - points[i]
        mid_point = (points[i] + points[i + 1]) / 2
        fig.add_annotation(
            x=mid_point, y=0.03, text=f'{distance:.2f}m', showarrow=False, font=dict(color='green', size=10), yshift=10
        )

    # Настройка графика
    fig.update_layout(
        xaxis=dict(range=[0, L], showgrid=False),
        yaxis=dict(range=[-0.1, 0.1], showgrid=False, showticklabels=False),
        showlegend=True,
        title='Распределение точек на линии',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

# Интерфейс Streamlit
st.title("Распределение точек на линии")

# Ввод данных
L = st.number_input("Длина линии (L):", value=3.0, min_value=0.1, step=0.1)
edge_distance = st.number_input("Расстояние от края до точки:", value=0.16, min_value=0.01, step=0.01)
min_distance = st.number_input("Минимальное расстояние между точками:", value=0.45, min_value=0.01, step=0.01)
max_distance = st.number_input("Максимальное расстояние между точками:", value=0.65, min_value=0.01, step=0.01)
num_new_points = st.number_input("Количество новых точек:", value=5, min_value=1, step=1)
min_distance_to_new_points = st.number_input("Минимальное расстояние до новых точек:", value=0.04, min_value=0.01, step=0.01)

# Построение графика
if st.button("Построить график"):
    fig = plot_graph(L, edge_distance, min_distance, max_distance, num_new_points, min_distance_to_new_points)
    st.plotly_chart(fig, use_container_width=True)