from manim import *


class Rule(VGroup):
    def __init__(
        self,
        width: float = 9,
        height: float = 2,
        length: int = 8,
        step_size: float = 0.25,
        buff: float = 0.5,
        fill_opacity: float = 1,
        fill_color: str = BLACK,
        stroke_width: int = 4,
        stroke_opacity: float = 1,
        stroke_color: str = WHITE,
        add_numbers: bool = True,
        number_font_size: int = 30,
        round_corners: float | None = 0.2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.rect = Rectangle(width=width, height=height)
        if round_corners is not None:
            self.rect.round_corners(round_corners)
        self.integer_lines = VGroup()
        self.lines = self.generate_lines(length, step_size, buff)
        self.add(self.rect, self.lines)
        if add_numbers:
            self.numbers = self.generate_numbers(length, number_font_size)
            self.add(self.numbers)
        self.set_stroke(stroke_color, stroke_width, stroke_opacity)
        self.set_fill(fill_color, fill_opacity)
    
    def generate_lines(self, length, step_size, buff):
        lines = VGroup()
        for x in np.arange(0, length + step_size, step_size):
            if x % 1 == 0:
                line_length = 0.8
            elif x % 0.5 == 0:
                line_length = 0.5
            else:
                line_length = 0.3
            line = Line(
                line_length * UP,
                ORIGIN
            )
            lines.add(line)
            if x % 1 == 0:
                self.integer_lines.add(line)
        lines_buff = (length - 2 * buff) / len(lines)
        lines.arrange(RIGHT, lines_buff, aligned_edge=UP)
        lines.next_to(self.rect.get_top(), DOWN, 0)
        return lines
    
    def generate_numbers(self, length, number_font_size):
        numbers = VGroup()
        for x, line in zip(range(length + 1), self.integer_lines):
            number = Integer(x, font_size=number_font_size)
            number.next_to(line, DOWN, 0.1)
            numbers.add(number)
        return numbers
