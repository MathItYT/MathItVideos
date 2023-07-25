from manim import *


class Outro(Scene):
    include_guide = False
    animate = True
    gracias_por_ver_txt = "¡Gracias por ver!"
    my_suggestion_txt = "Te sugiero ver"
    watch_next_txt = "Siguiente video"


    def setup(self):
        gracias_por_ver = Tex(self.gracias_por_ver_txt, font_size=96)
        gracias_por_ver.set_color_by_gradient(RED, YELLOW)
        gracias_por_ver.shift(2 * UP)

        my_suggestion_rect = ScreenRectangle(height=2.2, color=WHITE).set_fill(opacity=1)
        icon_circ = Circle(color=WHITE).set_fill(opacity=1)
        watch_next_rect = ScreenRectangle(height=2.2, color=WHITE).set_fill(opacity=1)

        VGroup(my_suggestion_rect, icon_circ, watch_next_rect).arrange(RIGHT, buff=0.725).shift(0.5 * DOWN)
        VGroup(my_suggestion_rect, watch_next_rect).shift(0.05 * UP)

        my_suggestion = Tex(self.my_suggestion_txt, font_size=48)
        my_suggestion.next_to(my_suggestion_rect, DOWN)
        watch_next = Tex(self.watch_next_txt, font_size=48)
        watch_next.next_to(watch_next_rect, DOWN)

        self.gracias_por_ver = gracias_por_ver
        self.my_suggestion_rect = my_suggestion_rect
        self.icon_circ = icon_circ
        self.watch_next_rect = watch_next_rect
        self.my_suggestion = my_suggestion
        self.watch_next = watch_next

        self.add(gracias_por_ver, my_suggestion_rect, icon_circ, watch_next_rect, my_suggestion, watch_next)
        
        if self.include_guide:
            self.bring_to_back(ImageMobject("outro_guide.jpg").scale_to_fit_height(config.frame_height))
        else:
            self.remove(*self.mobjects)
    
    def construct(self):
        if self.animate:
            self.play(LaggedStart(*[FadeIn(mob, scale=2) for mob in self.gracias_por_ver[0]]))
            self.add(self.my_suggestion_rect, self.icon_circ, self.watch_next_rect)
            self.play(Write(self.my_suggestion), Write(self.watch_next), run_time=1)
            self.wait(19)

