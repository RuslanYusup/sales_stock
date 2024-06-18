#%%
import os
from datetime import datetime

import apiclient
import httplib2
import pandas as pd
import warnings

from google.oauth2.gdch_credentials import ServiceAccountCredentials
from matplotlib import pyplot as plt
import gdown # Импорт библиотеки для загрузки файла

# экспорт файла на гугл диск
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


# Импорт из scr с указанием правильного пути и имя скрипта
from scr.datasets.download_prep_data import DataPreparation
from scr.models.model import prepare_and_forecast
from scr.models.evaluation import ModelEvaluation
from scr.Visualization.table import create_table
from scr.Visualization.visualisation import plot_model, plot_table

import gspread
from gspread_dataframe import set_with_dataframe

# Загрузка и предобработка данных
file_id = '1aU0M0sBQ55vhKxXJaaD8B9Bu_O60s5zG'
url = f'https://drive.google.com/uc?id={file_id}'

# Загрузка файла
gdown.download(url, 'D:\\project\\sales_stock\\Data\\raw\\PE.xlsx', quiet=False)

data_prep = DataPreparation('D:\\project\\sales_stock\\Data\\raw\\PE.xlsx')
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
table = create_table(forecast, df_pr, 'D:\\project\\sales_stock\\Data\\Proccesed\\table.csv')

# Визуализация таблицы
graph_forecast = plot_table(table)
print(type(graph_forecast))


# def get_google_auth(cred_file_name: str):
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file_name,
#                                                                    ['https://www.googleapis.com/auth/spreadsheets',
#                                                                     'https://www.googleapis.com/auth/drive'])
#
#     httpAuth = credentials.authorize(httplib2.Http())
#     service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
#     return service

# def add_log_in_google(google_service, google_file_id: str, log_text: str, PAGE_LOGS=None) -> None:
#     body = {
#         'values': [
#             [datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), log_text],
#         ]
#     }
#     resp = google_service.spreadsheets().values().append(
#         spreadsheetId=google_file_id,
#         range=PAGE_LOGS,
#         valueInputOption="RAW",
#         body=body).execute()
#
# service = get_google_auth('D:\\project\\sales_stock\\client_secret.json')
#
# table_list = table.values.tolist()
#
# for row in table_list:
#     log_text = ', '.join(map(str, row))
#     add_log_in_google(service, '107QRRuZQirWomm01WRs9Qqzo0weLKtBKTnsSQUU-EY4', log_text)

# os.chdir('D:\\project\\sales_stock\\')
#
# gauth = GoogleAuth('settings.yaml')
# # открываем окно авторизации
# gauth.LocalWebserverAuth()
#
#
# drive = GoogleDrive(gauth)
#
# # Путь к папке 'Proccesed'
# processed_folder_path = 'D:\\project\\sales_stock\\Data\\Proccesed\\table.csv'
#
# # Получение списка всех файлов в папке 'Proccesed'
# files_in_processed = os.listdir(processed_folder_path)
#
# # Запись из папки 'Proccesed' в Google Drive
# # Авторизация и открытие таблицы
# gc = gspread.service_account(filename='D:\\project\\sales_stock\\client_secret.json')
# spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/107QRRuZQirWomm01WRs9Qqzo0weLKtBKTnsSQUU-EY4/edit?gid=2060637574')
#
# # Получение рабочего листа
# worksheet = spreadsheet.get_worksheet(0)
#
# # Запись данных в рабочий лист
# set_with_dataframe(worksheet, table)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import yaml

# Загрузка данных из файла table.csv в DataFrame
table = pd.read_csv('D:\\project\\sales_stock\\Data\\Proccesed\\table.csv')

# Загрузка настроек из файла settings.yaml
with open('D:\\project\\sales_stock\\settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

# Получение учетных данных для авторизации в Google Drive
credentials = ServiceAccountCredentials.from_json_keyfile_name(settings['client_config_file'],
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

# Создание объекта service для работы с Google Sheets
gc = gspread.authorize(credentials)

# Открытие таблицы Google Sheets
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/107QRRuZQirWomm01WRs9Qqzo0weLKtBKTnsSQUU-EY4/edit?gid=2060637574')

# Получение рабочего листа
worksheet = spreadsheet.get_worksheet(0)

# Запись данных в рабочий лист
set_with_dataframe(worksheet, table)









#%%

#%%

#%%

#%%
