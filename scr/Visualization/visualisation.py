import matplotlib.pyplot as plt


def plot_model(model, forecast):
    model.plot(forecast, figsize=(10, 6))
    plt.show()


def plot_table(table):
    real_values = table['Реальное значение'][-40:].dropna()
    predicted_values = table['Предсказанное значение'][-30:]
    timestamps = table['Дата'][-40:]

    window_size = 10
    real_mean = real_values.mean()
    real_color = 'blue'
    predicted_color = 'red'

    plt.figure(figsize=(20, 6))

    plt.plot(timestamps[:len(real_values)], real_values, label='Реальное значение', color=real_color)
    plt.plot(timestamps[len(real_values):], predicted_values, label='Прогнозируемое значение',
             color=predicted_color)
    plt.axhline(real_mean, color='gray', linestyle='--', label='Среднее значение')
    lower_bound = table['Нижняя граница интервала'][-len(real_values):]
    upper_bound = table['Верхняя граница интервала'][-len(real_values):]
    plt.fill_between(timestamps[:len(real_values)], lower_bound, upper_bound, alpha=0.2, color='gray',
                     label='Доверительный интервал')

    plt.xlabel('Дата')
    plt.ylabel('Объем продаж')
    plt.title('Предиктивная аналитика продаж PE на узбекской Бирже')
    plt.legend()
    plt.show()


