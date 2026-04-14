"""
Честный ценник - приложение для расчёта реальной цены за 1 кг или 1 литр
Заголовок полностью виден на любом экране
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import platform
from kivy.metrics import dp
import os


class CheatPriceApp(App):
    """Главный класс приложения"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results_history = []

    def build(self):
        # Настройка окна
        Window.clearcolor = (0.95, 0.95, 0.95, 1)

        # ГЛАВНЫЙ КОНТЕЙНЕР (НЕ СКРОЛЛИТСЯ)
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[dp(16), dp(16), dp(16), dp(16)],  # Увеличен верхний отступ
            spacing=dp(8)
        )

        # Загружаем фоновое изображение
        self.load_background(main_layout)

        # ===== ВЕРХНЯЯ ЗАКРЕПЛЁННАЯ ЧАСТЬ =====
        # Заголовок (ещё больше увеличил высоту)
        title = Label(
            text='ЧЕСТНЫЙ ЦЕННИК',
            font_size='34sp',
            size_hint=(1, None),
            height=dp(75),     # Ещё больше высоты
            color=(0.1, 0.55, 0.1, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        title.bind(size=title.setter('text_size'))
        main_layout.add_widget(title)

        # Подзаголовок (тоже увеличил)
        subtitle = Label(
            text='Узнай реальную цену за 1 кг или 1 литр',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(38),
            color=(1, 0.5, 0, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        main_layout.add_widget(subtitle)

        # Отступ
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # --- Поле: Продукт / бренд ---
        product_label = Label(
            text='Продукт / бренд (необязательно):',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(24),
            color=(0.1, 0.3, 0.7, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        product_label.bind(size=product_label.setter('text_size'))
        main_layout.add_widget(product_label)

        # Контейнер для центрирования поля
        product_input_wrapper = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(42))
        product_input_wrapper.add_widget(Widget(size_hint_x=0.25))
        self.product_input = TextInput(
            text='',
            multiline=False,
            font_size='16sp',
            hint_text='Например: Кефир',
            size_hint_x=None,
            width=dp(200),
            height=dp(40),
            padding=[dp(12), dp(10)],
            background_color=(1, 1, 1, 1),
            halign='center'
        )
        product_input_wrapper.add_widget(self.product_input)
        product_input_wrapper.add_widget(Widget(size_hint_x=0.25))
        main_layout.add_widget(product_input_wrapper)

        # --- Поле: Вес или объём ---
        weight_label = Label(
            text='Вес или объём (граммы / мл):',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(24),
            color=(0.1, 0.3, 0.7, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        weight_label.bind(size=weight_label.setter('text_size'))
        main_layout.add_widget(weight_label)

        # Контейнер для центрирования поля
        weight_input_wrapper = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(42))
        weight_input_wrapper.add_widget(Widget(size_hint_x=0.25))
        self.velichina_input = TextInput(
            text='',
            multiline=False,
            font_size='16sp',
            hint_text='Например: 750',
            size_hint_x=None,
            width=dp(200),
            height=dp(40),
            padding=[dp(12), dp(10)],
            background_color=(1, 1, 1, 1),
            halign='center'
        )
        weight_input_wrapper.add_widget(self.velichina_input)
        weight_input_wrapper.add_widget(Widget(size_hint_x=0.25))
        main_layout.add_widget(weight_input_wrapper)

        # --- Поле: Цена товара ---
        price_label = Label(
            text='Цена товара (рубли):',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(24),
            color=(0.1, 0.3, 0.7, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        price_label.bind(size=price_label.setter('text_size'))
        main_layout.add_widget(price_label)

        # Контейнер для центрирования поля
        price_input_wrapper = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(42))
        price_input_wrapper.add_widget(Widget(size_hint_x=0.25))
        self.price_input = TextInput(
            text='',
            multiline=False,
            font_size='16sp',
            hint_text='Например: 99.90',
            size_hint_x=None,
            width=dp(200),
            height=dp(40),
            padding=[dp(12), dp(10)],
            background_color=(1, 1, 1, 1),
            halign='center'
        )
        price_input_wrapper.add_widget(self.price_input)
        price_input_wrapper.add_widget(Widget(size_hint_x=0.25))
        main_layout.add_widget(price_input_wrapper)

        # Отступ перед кнопкой
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # Контейнер для кнопки с контуром
        button_container = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(52))
        button_container.add_widget(Widget(size_hint_x=0.35))

        # Обычная кнопка
        self.calc_button = Button(
            text='РАССЧИТАТЬ',
            size_hint_x=None,
            width=dp(150),
            height=dp(48),
            background_color=(0.2, 0.6, 0.3, 1),
            background_normal='',
            font_size='16sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        self.calc_button.bind(on_press=self.calculate)

        # Добавляем контур к кнопке
        self.calc_button.bind(pos=self._update_button_outline, size=self._update_button_outline)

        button_container.add_widget(self.calc_button)
        button_container.add_widget(Widget(size_hint_x=0.35))
        main_layout.add_widget(button_container)

        # Отступ перед историей
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Заголовок истории
        history_title = Label(
            text='ПОСЛЕДНИЕ РАСЧЁТЫ',
            font_size='14sp',
            size_hint=(1, None),
            height=dp(28),
            color=(0.1, 0.3, 0.7, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        history_title.bind(size=history_title.setter('text_size'))
        main_layout.add_widget(history_title)

        # ===== ОКНО РЕЗУЛЬТАТОВ (СКРОЛЛИТСЯ) =====
        results_window = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1)
        )

        # Белый фон и рамка
        with results_window.canvas.before:
            Color(1, 1, 1, 0.95)
            results_window.bg_rect = Rectangle(pos=results_window.pos, size=results_window.size)
            Color(0, 0, 0, 1)
            results_window.border = Line(rectangle=(results_window.x, results_window.y,
                                                    results_window.width, results_window.height),
                                         width=1.5)
        results_window.bind(pos=self._update_results_bg, size=self._update_results_bg)

        # Контейнер для результатов
        self.results_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.results_container.bind(minimum_height=self.results_container.setter('height'))

        # Добавляем распорку сверху для отступа
        self.top_spacer = Widget(size_hint_y=None, height=dp(12))
        self.results_container.add_widget(self.top_spacer)

        results_scroll = ScrollView()
        results_scroll.add_widget(self.results_container)
        results_window.add_widget(results_scroll)

        main_layout.add_widget(results_window)

        return main_layout

    def _update_button_outline(self, instance, value):
        """Обновляет контур кнопки"""
        if hasattr(instance, 'outline'):
            instance.canvas.after.remove(instance.outline)
        with instance.canvas.after:
            Color(1, 0.5, 0, 1)
            instance.outline = Line(rectangle=(instance.x, instance.y, instance.width, instance.height), width=2)

    def _update_results_bg(self, instance, value):
        """Обновляет фон и рамку окна результатов"""
        if hasattr(instance, 'bg_rect'):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        if hasattr(instance, 'border'):
            instance.border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def load_background(self, layout):
        """Загружает фоновое изображение"""
        try:
            if platform == 'android':
                bg_path = 'assets/background.png'
            else:
                bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'background.png')

            if os.path.exists(bg_path):
                with layout.canvas.before:
                    Color(1, 1, 1, 1)
                    self.bg = Rectangle(source=bg_path, pos=layout.pos, size=layout.size)
                layout.bind(pos=self.update_bg, size=self.update_bg)
        except Exception as e:
            print(f"Фон не загружен: {e}")

    def update_bg(self, instance, value):
        """Обновляет размер и позицию фона"""
        if hasattr(self, 'bg'):
            self.bg.pos = instance.pos
            self.bg.size = instance.size

    def add_result_to_history(self, product_name, weight, price, true_price):
        """Добавляет результат в историю"""
        self.results_history.insert(0, {
            'product': product_name if product_name else '',
            'weight': weight,
            'price': price,
            'true_price': true_price
        })

        if len(self.results_history) > 12:
            self.results_history.pop()

        self.update_results_display()

    def update_results_display(self):
        """Обновляет отображение окна с результатами"""
        self.results_container.clear_widgets()
        self.results_container.add_widget(self.top_spacer)

        if not self.results_history:
            empty_label = Label(
                text='Здесь будут отображаться ваши расчёты',
                font_size='12sp',
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(40)
            )
            self.results_container.add_widget(empty_label)
            return

        for i, result in enumerate(self.results_history):
            result_item = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(70) if result['product'] else dp(58),
                padding=[dp(8), dp(4)],
                spacing=dp(2)
            )

            if result['product']:
                product_label = Label(
                    text=result['product'],
                    font_size='12sp',
                    color=(0.4, 0.2, 0.6, 1),
                    size_hint_y=None,
                    height=dp(20),
                    halign='center',
                    valign='middle',
                    bold=True,
                    italic=True
                )
                product_label.bind(size=product_label.setter('text_size'))
                result_item.add_widget(product_label)

            info_label = Label(
                text=f"{result['weight']:.1f} г/мл  |  {result['price']:.2f} руб.",
                font_size='11sp',
                color=(0.2, 0.2, 0.2, 1),
                size_hint_y=None,
                height=dp(22),
                halign='center',
                valign='middle',
                bold=True
            )
            info_label.bind(size=info_label.setter('text_size'))
            result_item.add_widget(info_label)

            price_label = Label(
                text=f"Цена за 1 кг/литр: {result['true_price']:.2f} руб.",
                font_size='13sp',
                color=(0.1, 0.55, 0.1, 1),
                size_hint_y=None,
                height=dp(24),
                halign='center',
                valign='middle',
                bold=True
            )
            price_label.bind(size=price_label.setter('text_size'))
            result_item.add_widget(price_label)

            if i < len(self.results_history) - 1:
                separator = BoxLayout(size_hint_y=None, height=dp(1))
                with separator.canvas:
                    Color(0.85, 0.85, 0.85, 1)
                    Rectangle(pos=separator.pos, size=separator.size)
                result_item.add_widget(separator)

            self.results_container.add_widget(result_item)

    def calculate(self, instance):
        """Выполняет расчёт"""
        try:
            product_name = self.product_input.text.strip()
            velichina_str = self.velichina_input.text.strip()
            price_str = self.price_input.text.strip()

            if not velichina_str or not price_str:
                return

            velichina = float(velichina_str)
            price = float(price_str)

            if velichina <= 0 or price < 0:
                return

            true_price = price / velichina * 1000
            self.add_result_to_history(product_name, velichina, price, true_price)

            self.product_input.text = ''
            self.velichina_input.text = ''
            self.price_input.text = ''

        except ValueError:
            pass


if __name__ == '__main__':
    CheatPriceApp().run()
