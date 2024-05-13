import pandas as pd
import numpy as np


def create_table(forecast, df, output_path=None):
    table = pd.DataFrame({
        'Дата': forecast['ds'],
        'Предсказанное значение': forecast['yhat'],
        'Реальное значение': df['y'],
        'Отклонение в %': np.abs((forecast['yhat'] - df['y']) / df['y']) * 100,
        'Нижняя граница интервала': forecast['yhat_lower'],
        'Верхняя граница интервала': forecast['yhat_upper']
    })
    table.to_csv(output_path, index=False)
    return table


