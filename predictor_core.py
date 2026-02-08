"""
Módulo core del predictor para Android
Versión simplificada optimizada para móvil
"""
import json
import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Imports condicionales para Android
try:
    import ccxt
    CCXT_AVAILABLE = True
except:
    CCXT_AVAILABLE = False

try:
    import joblib
    JOBLIB_AVAILABLE = True
except:
    JOBLIB_AVAILABLE = False


class CryptoPredictor:
    """Predictor de criptomonedas optimizado para móvil"""
    
    def __init__(self, model_path=None):
        """
        Inicializar predictor
        
        Args:
            model_path: Ruta al modelo (opcional, usa modelo incluido por defecto)
        """
        self.model = None
        self.preprocessor = None
        self.feature_names = None
        
        # Cargar modelo si está disponible
        if model_path is None:
            # Buscar en directorio de la app
            app_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(app_dir, 'model.pkl')
        
        if os.path.exists(model_path) and JOBLIB_AVAILABLE:
            try:
                model_data = joblib.load(model_path)
                self.model = model_data.get('model')
                self.feature_names = model_data.get('feature_names', [])
                
                preprocessor_path = model_path.replace('model.pkl', 'preprocessor.pkl')
                if os.path.exists(preprocessor_path):
                    self.preprocessor = joblib.load(preprocessor_path)
            except:
                pass
        
        # Configuración
        self.min_confidence = 0.70
        self.min_risk_reward = 2.0
    
    def download_data(self, symbol, timeframe='1h', limit=500):
        """
        Descargar datos del exchange
        
        Args:
            symbol: Par de trading
            timeframe: Timeframe
            limit: Número de velas
            
        Returns:
            DataFrame con datos OHLCV
        """
        if not CCXT_AVAILABLE:
            raise Exception("CCXT no disponible")
        
        exchange = ccxt.binance({'enableRateLimit': True})
        
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
        
        return df
    
    def calculate_indicators(self, df):
        """
        Calcular indicadores técnicos básicos
        
        Args:
            df: DataFrame con OHLCV
            
        Returns:
            DataFrame con indicadores
        """
        df = df.copy()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # EMAs
        df['ema_9'] = df['close'].ewm(span=9).mean()
        df['ema_21'] = df['close'].ewm(span=21).mean()
        df['ema_50'] = df['close'].ewm(span=50).mean()
        
        # MACD
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        df['macd'] = ema12 - ema26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(20).mean()
        bb_std = df['close'].rolling(20).std()
        df['bb_upper'] = df['bb_middle'] + (2 * bb_std)
        df['bb_lower'] = df['bb_middle'] - (2 * bb_std)
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        
        # ATR
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = true_range.rolling(14).mean()
        
        # Volume
        df['volume_sma'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # Returns
        df['return_1'] = df['close'].pct_change(1)
        df['return_5'] = df['close'].pct_change(5)
        
        # Volatility
        df['volatility_20'] = df['close'].pct_change().rolling(20).std()
        
        return df
    
    def create_features(self, df):
        """
        Crear features para predicción
        
        Args:
            df: DataFrame con indicadores
            
        Returns:
            DataFrame con features
        """
        df = df.copy()
        
        # Features adicionales simples
        df['price_to_ema50'] = df['close'] / df['ema_50']
        df['rsi_normalized'] = (df['rsi'] - 50) / 50
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        return df
    
    def detect_trend(self, df):
        """
        Detectar tendencia simple
        
        Args:
            df: DataFrame con EMAs
            
        Returns:
            String: 'uptrend', 'downtrend', 'sideways'
        """
        if len(df) < 50:
            return 'unknown'
        
        ema_short = df['ema_21'].iloc[-1]
        ema_long = df['ema_50'].iloc[-1]
        
        if ema_short > ema_long * 1.01:
            return 'uptrend'
        elif ema_short < ema_long * 0.99:
            return 'downtrend'
        else:
            return 'sideways'
    
    def generate_signal(self, symbol, timeframe='1h'):
        """
        Generar señal de trading
        
        Args:
            symbol: Par de trading
            timeframe: Timeframe
            
        Returns:
            Diccionario con señal
        """
        # Descargar datos
        df = self.download_data(symbol, timeframe)
        
        # Calcular indicadores
        df = self.calculate_indicators(df)
        df = self.create_features(df)
        
        # Última fila
        current = df.iloc[-1]
        current_price = current['close']
        
        # Detectar tendencia
        trend = self.detect_trend(df)
        
        # Predicción simple basada en reglas si no hay modelo
        if self.model is None:
            prediction, confidence = self._rule_based_prediction(df)
        else:
            prediction, confidence = self._ml_prediction(df)
        
        # Calcular niveles
        atr = current['atr']
        stop_loss = current_price - (2 * atr)
        take_profit = current_price + (4 * atr)
        risk_reward = (take_profit - current_price) / (current_price - stop_loss)
        
        # Validar señal
        is_valid = (
            prediction == 1 and
            confidence >= self.min_confidence and
            risk_reward >= self.min_risk_reward
        )
        
        signal = {
            'symbol': symbol,
            'timeframe': timeframe,
            'timestamp': df.index[-1],
            'current_price': float(current_price),
            'prediction': int(prediction),
            'confidence': float(confidence * 100),
            'signal': 'BUY' if is_valid else 'HOLD',
            'entry_price': float(current_price) if is_valid else None,
            'stop_loss': float(stop_loss) if is_valid else None,
            'take_profit': float(take_profit) if is_valid else None,
            'risk_reward_ratio': float(risk_reward) if is_valid else None,
            'trend': trend,
            'rsi': float(current['rsi']) if not pd.isna(current['rsi']) else None,
            'volume_ratio': float(current['volume_ratio']) if not pd.isna(current['volume_ratio']) else None,
        }
        
        return signal
    
    def _rule_based_prediction(self, df):
        """
        Predicción basada en reglas técnicas
        
        Args:
            df: DataFrame con indicadores
            
        Returns:
            Tupla (prediction, confidence)
        """
        current = df.iloc[-1]
        
        score = 0
        max_score = 7
        
        # RSI
        if 30 < current['rsi'] < 50:
            score += 1
        elif current['rsi'] < 30:
            score += 2
        
        # Tendencia
        if current['close'] > current['ema_21'] > current['ema_50']:
            score += 2
        
        # MACD
        if current['macd'] > current['macd_signal']:
            score += 1
        
        # Bollinger Bands
        if current['close'] < current['bb_lower']:
            score += 1.5
        
        # Volume
        if current['volume_ratio'] > 1.2:
            score += 0.5
        
        confidence = min(score / max_score, 0.95)
        prediction = 1 if confidence >= 0.6 else 0
        
        return prediction, confidence
    
    def _ml_prediction(self, df):
        """
        Predicción usando modelo ML
        
        Args:
            df: DataFrame con features
            
        Returns:
            Tupla (prediction, confidence)
        """
        try:
            last_row = df.iloc[-1:]
            
            # Seleccionar features
            X = last_row[self.feature_names]
            
            # Normalizar
            if self.preprocessor:
                X = self.preprocessor.transform(X)
            
            # Predecir
            prediction = self.model.predict(X)[0]
            confidence = self.model.predict_proba(X)[0, 1]
            
            return prediction, confidence
            
        except Exception as e:
            # Fallback a reglas
            return self._rule_based_prediction(df)


# Versión simplificada para cuando no hay modelo
if __name__ == "__main__":
    predictor = CryptoPredictor()
    signal = predictor.generate_signal('BTC/USDT', '1h')
    print(json.dumps(signal, indent=2, default=str))
