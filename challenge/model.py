import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from datetime import datetime

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union(Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        # Extract relevant columns for feature engineering
        data['Fecha-I'] = pd.to_datetime(data['Fecha-I'])
        data['Fecha-O'] = pd.to_datetime(data['Fecha-O'])
        data['DIA'] = data['Fecha-I'].dt.day
        data['MES'] = data['Fecha-I'].dt.month
        data['DIANOM'] = data['Fecha-I'].dt.day_name()
        
        # Define a function to get the period of the day
        def get_period_day(date):
            date_time = date.time()
            morning_min = datetime.strptime("05:00", '%H:%M').time()
            morning_max = datetime.strptime("11:59", '%H:%M').time()
            afternoon_min = datetime.strptime("12:00", '%H:%M').time()
            afternoon_max = datetime.strptime("18:59", '%H:%M').time()
            evening_min = datetime.strptime("19:00", '%H:%M').time()
            evening_max = datetime.strptime("23:59", '%H:%M').time()
            night_min = datetime.strptime("00:00", '%H:%M').time()
            night_max = datetime.strptime("4:59", '%H:%M').time()

            if (date_time > morning_min and date_time < morning_max):
                return 'mañana'
            elif (date_time > afternoon_min and date_time < afternoon_max):
                return 'tarde'
            elif ((date_time > evening_min and date_time < evening_max) or
                  (date_time > night_min and date_time < night_max)):
                return 'noche'
        
        data['period_day'] = data['Fecha-I'].apply(get_period_day)
        
        # Define a function to check high season
        def is_high_season(fecha):
            fecha_año = int(fecha.split('-')[0])
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year=fecha_año)
            range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year=fecha_año)
            range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year=fecha_año)
            range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year=fecha_año)
            range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year=fecha_año)
            range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year=fecha_año)
            range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year=fecha_año)
            range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year=fecha_año)

            if ((fecha >= range1_min and fecha <= range1_max) or
                (fecha >= range2_min and fecha <= range2_max) or
                (fecha >= range3_min and fecha <= range3_max) or
                (fecha >= range4_min and fecha <= range4_max)):
                return 1
            else:
                return 0

        data['high_season'] = data['Fecha-I'].apply(is_high_season)
        
        # Define a function to calculate time difference in minutes
        def get_min_diff(data):
            fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
            fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
            min_diff = ((fecha_o - fecha_i).total_seconds()) / 60
            return min_diff

        data['min_diff'] = data.apply(get_min_diff, axis=1)
        
        # Define a threshold for delay
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)
        
        # Drop unnecessary columns and split data into features and target
        if target_column:
            features = data.drop(target_column, axis=1)
            target = data[target_column]
            return features, target
        else:
            return features
        
    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        return