from manim import *
from channel.logo import Logo
from manim.utils.unit import Pixels
from channel.grid import Grid


config.background_color = "#222222"
config.pixel_width = 2560
config.pixel_height = 1440
SAFE_AREA_SIZE_X, SAFE_AREA_SIZE_Y = 1546, 423
TABLET_SIZE_X, TABLET_SIZE_Y = 1855, 423
COMPUTER_SIZE_X, COMPUTER_SIZE_Y = 2560, 423
TV_SIZE_X, TV_SIZE_Y = 2560, 1440


class Banner(Scene):
    include_guide = False

    def construct(self):
        self.logo = Logo().scale(0.5)
        self.logo.next_to(SAFE_AREA_SIZE_X / 2 * Pixels * LEFT, RIGHT)
        self.frase = Tex("``Las matemáticas son la puerta\\\\y la llave de la ciencia''", tex_environment="flushright", font_size=40)
        self.autor = Tex("-- Roger Bacon", font_size=40)
        self.frase_grupo = VGroup(self.frase, self.autor).arrange(DOWN, buff=0.05, aligned_edge=RIGHT)
        self.frase_grupo.next_to(SAFE_AREA_SIZE_X / 2 * Pixels * RIGHT, LEFT)
        x_range = [-config.frame_width / 2, config.frame_width / 2, 0.5]
        y_range = [-config.frame_height / 2, config.frame_height / 2, 0.5]
        axis_config = {
            "stroke_color": GREY,
            "stroke_width": 2,
            "stroke_opacity": 0,
            "include_ticks": False,
            "include_tip": False,
            "line_to_number_buff": SMALL_BUFF,
            "label_direction": DR,
            "font_size": 24
        }
        background_lines_style = {
            "stroke_color": GREY,
            "stroke_width": 2,
            "stroke_opacity": 0.25
        }
        self.grid = Grid(
            x_range=x_range,
            y_range=y_range,
            axis_config=axis_config,
            background_line_style=background_lines_style
        )
        self.add(self.grid, self.logo, self.frase_grupo)
        if self.include_guide:
            img = ImageMobject("banner_guide.jpg")
            img.scale_to_fit_height(config.frame_height)
            self.bring_to_back(img)
            self.logo.mathit.set_color(BLACK)
            self.frase_grupo.set_color(BLACK)
