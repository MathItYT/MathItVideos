from manim import *
from channel.logo import Logo


config.background_color = "#222222"
config.frame_width = config.frame_height = 8
config.pixel_width = config.pixel_height = 2000


class YouTubeIcon(Scene):
    def construct(self):
        logo = Logo().scale_to_fit_height(self.camera.frame_height - 2)
        self.add(logo)
