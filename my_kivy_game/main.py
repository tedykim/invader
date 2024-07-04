from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from random import randint

class InvaderGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ship = Rectangle(pos=(288, 50), size=(24, 24))
        self.beam = Rectangle(pos=(-24, -24), size=(24, 24))
        self.aliens = []
        self.bombs = []
        self.score = 0
        self.game_over = False

        with self.canvas:
            Color(1, 1, 1, 1)
            self.ship_color = Color(0, 1, 0, 1)
            self.canvas.add(self.ship_color)
            self.canvas.add(self.ship)
            self.beam_color = Color(1, 0, 0, 1)
            self.canvas.add(self.beam_color)
            self.canvas.add(self.beam)
        
        for ypos in range(4):
            for xpos in range(10):
                alien = Rectangle(pos=(100 + xpos * 50, ypos * 50 + 400), size=(24, 24))
                self.aliens.append(alien)
                self.canvas.add(alien)
        
        for _ in range(4):
            bomb = Rectangle(pos=(-24, -24), size=(24, 24))
            self.bombs.append(bomb)
            self.canvas.add(bomb)

        self.restart_button = Button(text='Restart', pos=(540, 540), size_hint=(None, None), size=(50, 50))
        self.restart_button.bind(on_press=self.restart_game)
        self.add_widget(self.restart_button)

        self.score_label = Label(text='Score: 0', pos=(500, 10), size_hint=(None, None))
        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 1 / 60.0)

    def restart_game(self, instance):
        self.__init__()

    def update(self, dt):
        if not self.game_over:
            self.beam.pos = (self.beam.pos[0], self.beam.pos[1] + 5)
            if self.beam.pos[1] > self.height:
                self.beam.pos = (-24, -24)

            for alien in self.aliens[:]:
                if self.beam.collide_widget(alien):
                    self.aliens.remove(alien)
                    self.canvas.remove(alien)
                    self.beam.pos = (-24, -24)
                    self.score += 10
                    self.score_label.text = f'Score: {self.score}'

            for bomb in self.bombs:
                bomb.pos = (bomb.pos[0], bomb.pos[1] + 5)
                if bomb.pos[1] > self.height:
                    bomb.pos = (-24, -24)
                    bomb.pos = (self.aliens[randint(0, len(self.aliens) - 1)].pos[0], self.height)
                if bomb.collide_widget(self.ship):
                    self.game_over = True
                    self.add_widget(Label(text='GAME OVER', pos=(self.width / 2 - 100, self.height / 2)))

            if not self.aliens:
                self.game_over = True
                self.add_widget(Label(text='YOU WIN!', pos=(self.width / 2 - 100, self.height / 2)))

    def on_touch_move(self, touch):
        self.ship.pos = (touch.x - self.ship.size[0] / 2, self.ship.pos[1])
        if self.ship.pos[0] < 0:
            self.ship.pos = (0, self.ship.pos[1])
        if self.ship.pos[0] > self.width - self.ship.size[0]:
            self.ship.pos = (self.width - self.ship.size[0], self.ship.pos[1])

    def on_touch_down(self, touch):
        self.beam.pos = (self.ship.pos[0] + self.ship.size[0] / 2 - 12, self.ship.pos[1] + self.ship.size[1])

class InvaderApp(App):
    def build(self):
        return InvaderGame()

if __name__ == '__main__':
    InvaderApp().run()
