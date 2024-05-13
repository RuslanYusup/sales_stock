from prophet import Prophet

def prepare_and_forecast(df, periods=30):
    model = Prophet(weekly_seasonality=2, yearly_seasonality=False,
                    seasonality_mode='multiplicative',
                    seasonality_prior_scale=.02, holidays_prior_scale=3)
    model.add_country_holidays(country_name='UZ')
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return model, forecast




#%%
