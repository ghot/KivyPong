from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, \
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import os, kivy, random

kivy.require('1.0.9')

Builder.load_file('pong.kv')

difficulty = 1.1
score = 20


class PongPaddle(Widget):
    score = NumericProperty(0)
    global difficulty

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * difficulty
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    global difficulty
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # a referencelist property so we can use
    # ball.velocity as a shorthand
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ''move'' function will move ball one step
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    sounds = {"donald": ["sounds/donald/" + x for x in os.listdir("sounds/donald/")],
              "bill": ["sounds/bill/" + x for x in os.listdir("sounds/bill/")]}

    print(sounds)

    def serve_ball(self, vel=(4, difficulty)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        global score
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if self.player1.score < score or self.player2.score < score:
            if self.ball.x < self.x:
                self.player2.score += 1
                p2sound = SoundLoader.load(random.choice(self.sounds["bill"]))
                p2sound.play()
                self.serve_ball(vel=(4, 0))
            if self.ball.x > self.width:
                self.player1.score += 1
                p1sound = SoundLoader.load(random.choice(self.sounds["donald"]))
                p1sound.play()
                self.serve_ball(vel=(-4, 0))
        if self.player1.score >= score or self.player2.score >= score:
            popup = Popup(title='Winner!',
                          content=(Label(text="Player 1 wins!")),
                          auto_dismiss=False)
            popup.open()
            self.p1sound.unload()
            self.p2sound.unload()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class MainMenu(GridLayout, App):

    theme = SoundLoader.load('sounds/menu_rap.wav')
    theme.loop = True
    theme.volume = 0.3
    theme.play()

    def build(self):
        self.title = "Pong Game"
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

    def diff(self):
        global difficulty
        difficulty *= 2

    def scr(self):
        global score
        score = 5

    def on_pause(self):
        self.theme.stop()
        return True

    def on_resume(self):
        self.theme.play()
        pass


class MainMenuApp(App):

    icon = 'images/icon.png'

    def build(self):
        self.title = "Main Menu"
        return MainMenu()


if __name__ == '__main__':
    MainMenuApp().run()
