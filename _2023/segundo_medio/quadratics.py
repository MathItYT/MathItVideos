from channel import *


class VideoIntro(Intro):
    pass


class Thumbnail(Scene):
    def construct(self):
        titulo = Tex("Ecuaciones cuadráticas", font_size=96).to_edge(UP)
        segundo = Tex("2")
        medio = Tex("medio")
        circ = Circle(color=WHITE).match_height(medio)
        circ.set_stroke(width=12)
        segundo.scale(4)
        segundo_medio = VGroup(segundo, circ, medio)
        segundo_medio.arrange(RIGHT, aligned_edge=UP)
        segundo_medio.scale(2)
        logo = Logo().scale(0.75).to_corner(DR)
        eq = MathTex("a", "x^", "2", "+", "b", "x", "+", "c", "=", "0", font_size=96)
        eq.to_edge(DOWN)
        eq.set_color_by_tex("x", YELLOW)
        self.add(logo, segundo_medio, titulo, eq)
