import pandas as pd


class DataPreparation:
    """Класс для загрузки и предобработки данных
    :param file_path: путь к файлу с данными
    output: предобработанный датафрейм
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        df_raw = pd.read_excel(self.file_path)
        df_raw["Дата контракта"] = pd.to_datetime(df_raw["Дата контракта"], format="%d.%m.%Y %H:%M:%S")
        df_raw["Дата"] = df_raw["Дата контракта"].dt.date
        df_filtered = df_raw[["Дата", "Количество"]]
        df_sorted = df_filtered.sort_values(by="Дата")
        grouped_sales = df_sorted.groupby("Дата")["Количество"].sum().reset_index()
        return grouped_sales


    def remove_anomalies(self, df):
        df_prophet = df.rename(columns={'Дата': 'ds', 'Количество': 'y'})
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
        df_pr = df_prophet.copy()
        df_pr['moving_average'] = df_pr.rolling(window=300, min_periods=1, center=True, on='ds')['y'].mean()
        df_pr['std_dev'] = df_pr.rolling(window=300, min_periods=1, center=True, on='ds')['y'].std()
        df_pr['lower'] = df_pr['moving_average'] - 1.65 * df_pr['std_dev']
        df_pr['upper'] = df_pr['moving_average'] + 1.65 * df_pr['std_dev']
        df_pr = df_pr[(df_pr['y'] < df_pr['upper']) & (df_pr['y'] > df_pr['lower'])]
        df_pr.drop(['moving_average', 'std_dev', 'lower', 'upper'], axis=1, inplace=True)
        df_pr = df_pr.reset_index(drop=True)
        return df_pr


# %%
