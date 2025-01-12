import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import logging

class SneakerPricePredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        
    def prepare_features(self, df):
        # Convert price to numeric, removing currency symbols
        df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
        
        # Add time-based features
        df['date_scraped'] = pd.to_datetime(df['date_scraped'])
        df['day_of_week'] = df['date_scraped'].dt.dayofweek
        df['month'] = df['date_scraped'].dt.month
        
        # Add any additional feature engineering here
        return df
        
    def train(self, X, y):
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model.fit(X_train_scaled, y_train)
            
            # Calculate and log accuracy
            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            logging.info(f"Train score: {train_score}, Test score: {test_score}")
            
            return test_score
            
        except Exception as e:
            logging.error(f"Error during training: {e}")
            raise
            
    def predict(self, features):
        features_scaled = self.scaler.transform(features)
        return self.model.predict(features_scaled)
        
    def save_model(self, filepath='models/sneaker_predictor.joblib'):
        joblib.dump((self.model, self.scaler), filepath)
        
    def load_model(self, filepath='models/sneaker_predictor.joblib'):
        self.model, self.scaler = joblib.load(filepath)