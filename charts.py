import pygal

def build_chart(chart_type, title, x_labels, data):
    """Функция создания и настройки диаграммы заданного типа"""
    if chart_type == "bar_vertical":
        chart =  pygal.Bar()
    elif chart_type == "pie":
        chart = pygal.Pie()
    #...

    # Настройка содержания диаграммы
    chart.title = title                     # Установка заголовка
    chart.x_labels = x_labels               # Метки оси X
    chart.x_title = "Result"                # Подпись оси X
    chart.y_title = "Frequency of Result"   # Подпись оси Y
    chart.add("Results", data)              # Добавление данных

    # Возврат готовой диаграммы
    return chart