#%%
import pandas as pd
import warnings

from matplotlib import pyplot as plt


# Импорт из scr с указанием правильного пути и имя скрипта
from scr.datasets.download_prep_data import DataPreparation
from scr.models.model import prepare_and_forecast
from scr.models.evaluation import ModelEvaluation
from scr.Visualization.table import create_table
from scr.Visualization.visualisation import plot_model, plot_table

# Загрузка и предобработка данных
data_prep = DataPreparation('C:\\Users\\yusup\\OneDrive\\Рабочий стол\\sales_stock\\Data\\raw\\PE.xlsx')
grouped_sales = data_prep.load_data()
df_pr = data_prep.remove_anomalies(grouped_sales)
df_pr['ds'] = pd.to_datetime(df_pr['ds']) # Преобразование в формат даты уже явно задал

# Подготовка и обучение модели
model, forecast = prepare_and_forecast(df_pr, 30)

# Оценка модели
model_eval = ModelEvaluation()
mape, mae, mse = model_eval.evaluate_last_n(df_pr, forecast, 18)
print('MAPE %:', mape, 'MAE:', mae, 'MSE:', mse)

# Визуализация модели
graph_model = model.plot(forecast, figsize=(10, 6))
plt.show(block=True)

# Создание таблицы и сохранение ее в CSV-файл
table = create_table(forecast, df_pr, 'C:\\Users\\yusup\\OneDrive\\Рабочий стол\\sales_stock\\Data\\Proccesed\\table.csv')

# Визуализация таблицы
#graph_forecast = plot_table(table)
#print(type(graph_forecast))

#%%

#%%
