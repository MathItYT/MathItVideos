from manim import *
from channel.rule import Rule


class Logo(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rule = Rule(stroke_width=2, add_numbers=False).scale(0.25).rotate(PI / 6).shift(0.25 * RIGHT)
        self.integral = MathTex(r"\int", color=RED, font_size=96).shift(0.2 * LEFT)
        self.infinity = MathTex(r"\infty", color=ORANGE, font_size=144).shift(RIGHT)
        self.mathit = Tex("\\textsc{MathIt}", font_size=66)
        self.icon = VGroup(self.rule, self.integral, self.infinity)
        self.add(self.icon, self.mathit)
        self.set_opacity(1)
        self.arrange(DOWN)

    def create(self, run_time=1.5, **kwargs):
        return AnimationGroup(
            SpiralIn(self.icon),
            Write(self.mathit),
            run_time=run_time,
            **kwargs
        )
