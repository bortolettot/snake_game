import random

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

CELL_SIZE = 20
GAME_SPEED = 10

class SnakeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(100, 100)]
        self.direction = (CELL_SIZE, 0)
        self.food = self.random_pos()
        self.score = 0
        Clock.schedule_interval(self.update, 1.0 / GAME_SPEED)

    def random_pos(self):
        x = random.randrange(0, int(self.width - CELL_SIZE), CELL_SIZE)
        y = random.randrange(0, int(self.height - CELL_SIZE), CELL_SIZE)
        return (x, y)

    def on_size(self, *args):
        self.reset()

    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (CELL_SIZE, 0)
        self.food = self.random_pos()
        self.score = 0
        self.parent.update_score(self.score)
        self.draw()

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            self.direction = (CELL_SIZE if dx > 0 else -CELL_SIZE, 0)
        else:
            self.direction = (0, CELL_SIZE if dy > 0 else -CELL_SIZE)

    def move(self):
        head_x, head_y = self.snake[-1]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.snake.append(new_head)
        self.snake.pop(0)

    def update(self, dt):
        self.move()
        if self.snake[-1] == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.random_pos()
            self.score += 1
            self.parent.update_score(self.score)
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.9, 0.9, 1)
            Rectangle(pos=(0, 0), size=self.size)
            Color(1, 0, 0)
            Rectangle(pos=self.food, size=(CELL_SIZE, CELL_SIZE))
            Color(0, 0, 1)
            for x, y in self.snake:
                Rectangle(pos=(x, y), size=(CELL_SIZE, CELL_SIZE))

class SnakeGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.score_label = Label(text='Pontos: 0', font_size=32, size_hint=(1, None), height=50)
        self.add_widget(self.score_label)
        self.game_widget = SnakeWidget(size_hint=(1, 1))
        self.add_widget(self.game_widget)
        controls = BoxLayout(size_hint=(1, None), height=80, padding=10, spacing=10)
        btn_up = Button(text='▲')
        btn_down = Button(text='▼')
        btn_left = Button(text='◀')
        btn_right = Button(text='▶')
        btn_up.bind(on_press=lambda *a: self.set_dir(0, CELL_SIZE))
        btn_down.bind(on_press=lambda *a: self.set_dir(0, -CELL_SIZE))
        btn_left.bind(on_press=lambda *a: self.set_dir(-CELL_SIZE, 0))
        btn_right.bind(on_press=lambda *a: self.set_dir(CELL_SIZE, 0))
        controls.add_widget(btn_left)
        controls.add_widget(BoxLayout(orientation='vertical', children=[btn_up, btn_down]))
        controls.add_widget(btn_right)
        self.add_widget(controls)

    def set_dir(self, x, y):
        self.game_widget.direction = (x, y)

    def update_score(self, value):
        self.score_label.text = f'Pontos: {value}'

class SnakeApp(App):
    def build(self):
        Window.size = (800, 600)
        return SnakeGame()

if __name__ == '__main__':
    SnakeApp().run()
