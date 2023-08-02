from manim import *


class Grid(NumberPlane):
    def __init__(
        self,
        stroke_color: str = GREY,
        x_range: list = None,
        y_range: list = None,
        x_length: int = None,
        y_length: int = None,
        axis_config: dict = None,
        background_line_style: dict = None,
        **kwargs
    ):
        if axis_config is None:
            axis_config = {
                "stroke_color": stroke_color,
                "stroke_width": 2,
                "include_ticks": False,
                "include_tip": False,
                "line_to_number_buff": SMALL_BUFF,
                "label_direction": DR,
                "font_size": 24
            }
        if background_line_style is None:
            background_line_style = {
                "stroke_color": GREY,
                "stroke_width": 2,
                "stroke_opacity": 1,
            }
        if x_range is None:
            x_range = [-config.frame_width / 2, config.frame_width / 2, 1]
        if y_range is None:
            y_range = [-config.frame_height / 2, config.frame_height / 2, 1]
        if x_length is None:
            x_length = config.frame_width
        if y_length is None:
            y_length = config.frame_height
        super().__init__(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config=axis_config,
            background_line_style=background_line_style,
            **kwargs
        )
