from manim import *
from channel.logo import Logo


class Intro(Scene):
    def setup(self):
        self.logo = Logo()

    def construct(self):
        self.play(self.logo.create())
        self.wait()
