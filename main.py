"""
Crypto Predictor - Aplicación Móvil Android
Interfaz principal usando Kivy
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
import threading
import json
from datetime import datetime

# Importar módulos del predictor
from predictor_core import CryptoPredictor

# Establecer color de fondo
Window.clearcolor = (0.1, 0.1, 0.15, 1)


class HomeScreen(Screen):
    """Pantalla principal con resumen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.predictor = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='[b]Crypto Predictor[/b]',
            markup=True,
            size_hint=(1, 0.1),
            font_size='24sp',
            color=(0.2, 0.8, 1, 1)
        )
        layout.add_widget(header)
        
        # Estado del sistema
        self.status_label = Label(
            text='Sistema: [color=ffff00]Inicializando...[/color]',
            markup=True,
            size_hint=(1, 0.08),
            font_size='16sp'
        )
        layout.add_widget(self.status_label)
        
        # Selector de símbolo
        symbols_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        symbols_layout.add_widget(Label(text='Símbolo:', size_hint=(0.3, 1)))
        
        self.symbol_spinner = Spinner(
            text='BTC/USDT',
            values=['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT', 'MATIC/USDT'],
            size_hint=(0.7, 1)
        )
        symbols_layout.add_widget(self.symbol_spinner)
        layout.add_widget(symbols_layout)
        
        # Selector de timeframe
        timeframe_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        timeframe_layout.add_widget(Label(text='Timeframe:', size_hint=(0.3, 1)))
        
        self.timeframe_spinner = Spinner(
            text='1h',
            values=['15m', '1h', '4h', '1d'],
            size_hint=(0.7, 1)
        )
        timeframe_layout.add_widget(self.timeframe_spinner)
        layout.add_widget(timeframe_layout)
        
        # Botón analizar
        self.analyze_btn = Button(
            text='Analizar',
            size_hint=(1, 0.12),
            background_color=(0.2, 0.7, 0.3, 1),
            font_size='18sp',
            bold=True
        )
        self.analyze_btn.bind(on_press=self.analyze_symbol)
        layout.add_widget(self.analyze_btn)
        
        # Progress bar
        self.progress = ProgressBar(max=100, size_hint=(1, 0.05))
        layout.add_widget(self.progress)
        
        # Área de resultados
        scroll = ScrollView(size_hint=(1, 0.55))
        self.results_label = Label(
            text='Presiona "Analizar" para comenzar',
            markup=True,
            size_hint_y=None,
            font_size='14sp',
            halign='left',
            valign='top'
        )
        self.results_label.bind(texture_size=self.results_label.setter('size'))
        scroll.add_widget(self.results_label)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        # Inicializar predictor
        Clock.schedule_once(lambda dt: self.init_predictor(), 0.5)
    
    def init_predictor(self):
        """Inicializar el predictor en segundo plano"""
        self.status_label.text = 'Sistema: [color=ffff00]Cargando modelo...[/color]'
        
        def load():
            try:
                self.predictor = CryptoPredictor()
                Clock.schedule_once(lambda dt: self.on_predictor_loaded(), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.on_predictor_error(str(e)), 0)
        
        threading.Thread(target=load).start()
    
    def on_predictor_loaded(self):
        self.status_label.text = 'Sistema: [color=00ff00]✓ Listo[/color]'
        self.analyze_btn.disabled = False
    
    def on_predictor_error(self, error):
        self.status_label.text = f'Sistema: [color=ff0000]Error: {error}[/color]'
        self.results_label.text = '[color=ff0000]Error al cargar el modelo.\nDescarga el modelo primero.[/color]'
    
    def analyze_symbol(self, instance):
        """Analizar el símbolo seleccionado"""
        if not self.predictor:
            self.results_label.text = '[color=ff0000]Error: Modelo no cargado[/color]'
            return
        
        symbol = self.symbol_spinner.text
        timeframe = self.timeframe_spinner.text
        
        self.analyze_btn.disabled = True
        self.progress.value = 0
        self.results_label.text = f'Analizando {symbol}...'
        
        def analyze():
            try:
                # Simular progreso
                for i in range(20, 60, 10):
                    Clock.schedule_once(lambda dt, v=i: setattr(self.progress, 'value', v), 0)
                
                signal = self.predictor.generate_signal(symbol, timeframe)
                
                Clock.schedule_once(lambda dt: setattr(self.progress, 'value', 80), 0)
                Clock.schedule_once(lambda dt: self.display_signal(signal), 0)
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.on_analyze_error(str(e)), 0)
        
        threading.Thread(target=analyze).start()
    
    def display_signal(self, signal):
        """Mostrar los resultados del análisis"""
        self.progress.value = 100
        
        symbol = signal['symbol']
        action = signal['signal']
        price = signal['current_price']
        confidence = signal['confidence']
        
        # Color según la señal
        if action == 'BUY':
            color = '00ff00'
            emoji = '🚀'
        else:
            color = 'ffaa00'
            emoji = '⏸'
        
        result = f"[b][size=18sp][color={color}]{emoji} {action}[/color][/size][/b]\n\n"
        result += f"[b]Símbolo:[/b] {symbol}\n"
        result += f"[b]Precio:[/b] ${price:,.2f}\n"
        result += f"[b]Confianza:[/b] {confidence:.2f}%\n"
        result += f"[b]Tendencia:[/b] {signal.get('trend', 'N/A')}\n"
        
        if action == 'BUY':
            result += f"\n[color=00ff00][b]NIVELES DE TRADING:[/b][/color]\n"
            result += f"[b]Entrada:[/b] ${signal['entry_price']:,.2f}\n"
            result += f"[b]Stop Loss:[/b] ${signal['stop_loss']:,.2f}\n"
            result += f"[b]Take Profit:[/b] ${signal['take_profit']:,.2f}\n"
            result += f"[b]R/R Ratio:[/b] {signal['risk_reward_ratio']:.2f}\n"
            
            loss_pct = ((signal['stop_loss'] / price - 1) * 100)
            profit_pct = ((signal['take_profit'] / price - 1) * 100)
            
            result += f"\n[color=ff4444]Riesgo: {loss_pct:.2f}%[/color]\n"
            result += f"[color=44ff44]Objetivo: {profit_pct:.2f}%[/color]\n"
        else:
            result += f"\n[color=ffaa00]No hay oportunidad clara en este momento.[/color]\n"
        
        if signal.get('rsi'):
            result += f"\n[b]Indicadores:[/b]\n"
            result += f"RSI: {signal['rsi']:.2f}\n"
        
        result += f"\n[size=10sp][color=888888]Actualizado: {datetime.now().strftime('%H:%M:%S')}[/color][/size]"
        
        self.results_label.text = result
        self.analyze_btn.disabled = False
    
    def on_analyze_error(self, error):
        self.results_label.text = f'[color=ff0000]Error: {error}[/color]'
        self.analyze_btn.disabled = False
        self.progress.value = 0


class SignalsScreen(Screen):
    """Pantalla de señales múltiples"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.predictor = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='[b]Señales Múltiples[/b]',
            markup=True,
            size_hint=(1, 0.1),
            font_size='20sp'
        )
        layout.add_widget(header)
        
        # Botón actualizar
        update_btn = Button(
            text='Actualizar Todas',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        update_btn.bind(on_press=self.update_all_signals)
        layout.add_widget(update_btn)
        
        # Lista de señales
        scroll = ScrollView(size_hint=(1, 0.8))
        self.signals_layout = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        self.signals_layout.bind(minimum_height=self.signals_layout.setter('height'))
        scroll.add_widget(self.signals_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Cuando se entra a esta pantalla"""
        if hasattr(self.manager, 'predictor'):
            self.predictor = self.manager.predictor
            self.update_all_signals(None)
    
    def update_all_signals(self, instance):
        """Actualizar todas las señales"""
        if not self.predictor:
            return
        
        self.signals_layout.clear_widgets()
        
        symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT']
        
        for symbol in symbols:
            card = self.create_signal_card(symbol)
            self.signals_layout.add_widget(card)
    
    def create_signal_card(self, symbol):
        """Crear tarjeta de señal"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            padding=5,
            spacing=3
        )
        
        # Fondo de la tarjeta
        from kivy.graphics import Color, Rectangle
        with card.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            card.rect = Rectangle(size=card.size, pos=card.pos)
        
        card.bind(pos=lambda obj, val: setattr(card.rect, 'pos', val))
        card.bind(size=lambda obj, val: setattr(card.rect, 'size', val))
        
        label = Label(
            text=f'[b]{symbol}[/b]\nCargando...',
            markup=True,
            size_hint=(1, 1)
        )
        card.add_widget(label)
        
        # Cargar señal en segundo plano
        def load_signal():
            try:
                signal = self.predictor.generate_signal(symbol, '1h')
                text = self.format_signal_card(signal)
                Clock.schedule_once(lambda dt: setattr(label, 'text', text), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(label, 'text', f'[color=ff0000]{symbol}\nError[/color]'), 0)
        
        threading.Thread(target=load_signal).start()
        
        return card
    
    def format_signal_card(self, signal):
        """Formatear señal para la tarjeta"""
        symbol = signal['symbol']
        action = signal['signal']
        price = signal['current_price']
        conf = signal['confidence']
        
        if action == 'BUY':
            color = '00ff00'
            text = f"[b][color={color}]{symbol} - 🚀 COMPRA[/color][/b]\n"
        else:
            color = 'ffaa00'
            text = f"[b][color={color}]{symbol} - ⏸ ESPERAR[/color][/b]\n"
        
        text += f"${price:,.2f} | Conf: {conf:.1f}%"
        
        return text


class SettingsScreen(Screen):
    """Pantalla de configuración"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = Label(
            text='[b]Configuración[/b]',
            markup=True,
            size_hint=(1, 0.1),
            font_size='20sp'
        )
        layout.add_widget(header)
        
        info = Label(
            text='Crypto Predictor Mobile v1.0\n\n'
                 'Sistema de predicción de criptomonedas\n'
                 'basado en Machine Learning\n\n'
                 '[b]Configuración:[/b]\n'
                 'Confianza mínima: 70%\n'
                 'Risk/Reward mínimo: 2:1\n\n'
                 '[size=10sp][color=888888]Para re-entrenar el modelo,\n'
                 'usa la versión de escritorio.[/color][/size]',
            markup=True,
            size_hint=(1, 0.9)
        )
        layout.add_widget(info)
        
        self.add_widget(layout)


class CryptoPredictorApp(App):
    """Aplicación principal"""
    
    def build(self):
        # Screen manager
        sm = ScreenManager()
        
        # Agregar pantallas
        home = HomeScreen(name='home')
        signals = SignalsScreen(name='signals')
        settings = SettingsScreen(name='settings')
        
        sm.add_widget(home)
        sm.add_widget(signals)
        sm.add_widget(settings)
        
        # Layout principal con navegación
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(sm)
        
        # Barra de navegación inferior
        nav_bar = BoxLayout(size_hint=(1, 0.08), spacing=2)
        
        btn_home = Button(text='Inicio', background_color=(0.2, 0.6, 0.8, 1))
        btn_home.bind(on_press=lambda x: setattr(sm, 'current', 'home'))
        nav_bar.add_widget(btn_home)
        
        btn_signals = Button(text='Señales', background_color=(0.2, 0.6, 0.8, 1))
        btn_signals.bind(on_press=lambda x: setattr(sm, 'current', 'signals'))
        nav_bar.add_widget(btn_signals)
        
        btn_settings = Button(text='Config', background_color=(0.2, 0.6, 0.8, 1))
        btn_settings.bind(on_press=lambda x: setattr(sm, 'current', 'settings'))
        nav_bar.add_widget(btn_settings)
        
        main_layout.add_widget(nav_bar)
        
        # Compartir predictor entre pantallas
        sm.predictor = None
        Clock.schedule_once(lambda dt: self.init_shared_predictor(sm), 1)
        
        return main_layout
    
    def init_shared_predictor(self, sm):
        """Inicializar predictor compartido"""
        try:
            sm.predictor = CryptoPredictor()
        except:
            pass


if __name__ == '__main__':
    CryptoPredictorApp().run()
