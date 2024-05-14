
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

class ModelEvaluation:
    """Класс для оценки модели
    """
    def __init__(self):
        pass

    def evaluate_model(self, y_true, y_pred):
        mape = mean_absolute_percentage_error(y_true, y_pred)*100
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        return mape, mae, mse

    def evaluate_last_n(self, df_true, df_pred, n):
        y_true = df_true['y'][-n:]
        y_pred = df_pred['yhat'][-n:]
        return self.evaluate_model(y_true, y_pred)
    