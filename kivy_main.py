import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

bloco_cobra = 20

class GameWidget(Widget):
    def __init__(self, velocidade=10, num_obstaculos=5, tempo_pausa=5, **kwargs):
        super().__init__(**kwargs)
        self.velocidade = velocidade
        self.num_obstaculos = num_obstaculos
        self.tempo_pausa = tempo_pausa
        self.snake = []
        self.bot = []
        self.obstaculos = []
        self.snake_dir = (bloco_cobra, 0)
        self.bot_dir = (bloco_cobra, 0)
        self.score = 0
        self.bot_score = 0
        self.label = Label(text='', pos=(10, self.height-40))
        self.add_widget(self.label)
        self.pausa_jogador = 0
        self.pausa_bot = 0
        self.reset()
        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.update, 1/float(self.velocidade))

    def reset(self):
        self.snake = [(self.width/2, self.height/2)]
        self.bot = [(self.width/4, self.height/4)]
        self.obstaculos = [self.random_pos() for _ in range(self.num_obstaculos)]
        self.food = self.random_pos()
        self.score = 0
        self.bot_score = 0
        self.update_label()

    def random_pos(self):
        x = random.randrange(0, int(self.width-bloco_cobra), bloco_cobra)
        y = random.randrange(0, int(self.height-bloco_cobra), bloco_cobra)
        return (x, y)

    def on_size(self, *args):
        self.reset()

    def update_label(self):
        self.label.text = f"Voce: {self.score}  Bot: {self.bot_score}"
        self.label.pos = (10, self.height-40)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 273:  # up
            self.snake_dir = (0, bloco_cobra)
        elif key == 274:  # down
            self.snake_dir = (0, -bloco_cobra)
        elif key == 276:  # left
            self.snake_dir = (-bloco_cobra, 0)
        elif key == 275:  # right
            self.snake_dir = (bloco_cobra, 0)

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            if dx > 0:
                self.snake_dir = (bloco_cobra, 0)
            else:
                self.snake_dir = (-bloco_cobra, 0)
        else:
            if dy > 0:
                self.snake_dir = (0, bloco_cobra)
            else:
                self.snake_dir = (0, -bloco_cobra)

    def move_entity(self, body, direction):
        head_x, head_y = body[-1]
        new_head = (head_x + direction[0], head_y + direction[1])
        body.append(new_head)
        body.pop(0)

    def update(self, dt):
        self.move_entity(self.snake, self.snake_dir)
        # simple bot movement towards food
        if abs(self.bot[-1][0] - self.food[0]) > abs(self.bot[-1][1] - self.food[1]):
            self.bot_dir = (bloco_cobra if self.bot[-1][0] < self.food[0] else -bloco_cobra, 0)
        else:
            self.bot_dir = (0, bloco_cobra if self.bot[-1][1] < self.food[1] else -bloco_cobra)
        self.move_entity(self.bot, self.bot_dir)

        if self.snake[-1] == self.food:
            self.food = self.random_pos()
            self.snake.append(self.snake[-1])
            self.score += 1
        elif self.bot[-1] == self.food:
            self.food = self.random_pos()
            self.bot.append(self.bot[-1])
            self.bot_score += 1
        self.update_label()
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.95, 0.95, 0.95)
            Rectangle(pos=(0,0), size=self.size)
            Color(0,1,0)
            Rectangle(pos=self.food, size=(bloco_cobra, bloco_cobra))
            Color(0.5,0.5,0.5)
            for ox, oy in self.obstaculos:
                Rectangle(pos=(ox,oy), size=(bloco_cobra, bloco_cobra))
            Color(0,0,1)
            for x, y in self.snake:
                Rectangle(pos=(x,y), size=(bloco_cobra, bloco_cobra))
            Color(1,0,0)
            for x, y in self.bot:
                Rectangle(pos=(x,y), size=(bloco_cobra, bloco_cobra))

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = GameWidget()
        self.add_widget(self.game)

    def setup(self, velocidade, num_obs, pausa):
        self.remove_widget(self.game)
        self.game = GameWidget(velocidade, num_obs, pausa)
        self.add_widget(self.game)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text='Escolha a dificuldade', font_size=32))
        botoes = [
            ('Facil', 5, 3, 3),
            ('Medio', 15, 5, 5),
            ('Dificil', 20, 7, 7)
        ]
        for texto, vel, obs, pausa in botoes:
            btn = Button(text=texto, size_hint=(1, None), height=50)
            btn.bind(on_press=lambda inst, v=vel, o=obs, p=pausa: self.start(v,o,p))
            layout.add_widget(btn)
        self.add_widget(layout)

    def start(self, velocidade, obs, pausa):
        game_screen = self.manager.get_screen('game')
        game_screen.setup(velocidade, obs, pausa)
        self.manager.current = 'game'

class SnakeApp(App):
    def build(self):
        Window.size = (800, 600)
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    SnakeApp().run()
