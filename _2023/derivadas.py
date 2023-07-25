from channel import *
from manim.utils.rate_functions import ease_in_out_expo


def get_tangent_line(func, derivative_func, x, length=10, **kwargs):
    line = Line(ORIGIN, length * RIGHT, **kwargs)
    line.rotate(np.arctan(derivative_func(x)), about_point=ORIGIN)
    line.move_to(x * RIGHT + func(x) * UP)
    return line


def get_T_to_val(
    ax: CoordinateSystem,
    val,
    t_label = None,
    triangle_size = MED_SMALL_BUFF,
    triangle_color = WHITE,
    is_x_axis = True
):
    T_label_group = VGroup()
    triangle = RegularPolygon(n=3, start_angle=np.pi / 2, stroke_width=0).set_fill(
        color=triangle_color,
        opacity=1,
    )
    triangle.height = triangle_size

    if not is_x_axis:
        triangle.rotate(-PI / 2)
        direction = LEFT
        triangle.next_to(ax.c2p(0, val), direction, 0)
    else:
        direction = DOWN
        triangle.next_to(ax.c2p(val, 0), direction, 0)

    T_label_group.add(triangle)

    if t_label is not None:
        t_label.next_to(triangle, direction, buff=SMALL_BUFF)
        T_label_group.add(t_label)

    return T_label_group


class Miniatura(Scene):
    def construct(self):
        titulo = Text("¿Qué son las derivadas?", font_size=80)
        subtitulo = Text("Cálculo diferencial")
        titulos = VGroup(titulo, subtitulo).arrange(DOWN)
        logo = Logo().scale(0.5).to_corner(DR)
        circle = Circle(radius=0.75)
        dy_dx = MathTex("{d", "y", "\\over", "d", "x}")
        dy_dx.set_color_by_tex_to_color_map({"y": RED, "x": RED})
        subject = VGroup(circle, dy_dx)
        subject.to_corner(UL)
        ax = Axes(
            x_length=1.5,
            y_length=1.5,
            x_range=[-1, 1, 0.2],
            y_range=[-1, 1, 0.2],
            tips=False,
            axis_config={"tick_size": 0.05}
        )
        graph = ax.plot(lambda x: x ** 3, x_range=[-1, 1], color=ORANGE)
        secant_line = ax.get_secant_slope_group(
            x=-0.5,
            graph=graph,
            dx=0.05,
            secant_line_length=1.5,
            secant_line_color=LIGHTER_GREY
        )
        graph_g = VGroup(ax, graph, secant_line).to_corner(UR)
        grid = Grid()
        graph_grid = grid.plot(
            lambda x: (lambda t: t ** 3 + t ** 2)(0.3 * x),
            x_range=[-config.frame_x_radius, config.frame_x_radius],
            color=ORANGE
        )
        background_mobjects = VGroup(grid, graph_grid).set_stroke(opacity=0.2)
        parte = Text("#1", font_size=80).to_corner(DL)
        self.add(background_mobjects, titulos, logo, subject, graph_g, parte)


class MechanicsScene(Scene):
    gravity = 10

    def setup(self):
        self.ground = None

    def make_ground(self, width=config.frame_width, x=0, y=-3.5):
        self.ground = Line(width / 2 * LEFT, width / 2 * RIGHT)
        self.ground.move_to(x * RIGHT+  y * UP)
        self.ground_y = y
        return self.ground

    def make_rigid_mobject(self, mobject: Mobject):
        mobject.vy = 0

        if not hasattr(mobject, "mechanics_updater"):
            mobject.mechanics_updater = None
        else:
            self.stop_rigid_mobject(mobject)

        def updater(mob: Mobject, dt):
            mob.shift(mob.vy * dt * UP)
            mob.vy -= self.gravity * dt
            if self.ground is None:
                return
            if not (self.ground.get_start()[0] <= mob.get_x() <= self.ground.get_end()[0]):
                return
            if mob.get_y() < self.ground_y:
                mob.set_y(self.ground_y)
                mob.vy *= -0.8

        mobject.mechanics_updater = updater
        return mobject
    
    def stop_rigid_mobject(self, mobject: Mobject):
        if mobject.mechanics_updater is not None:
            mobject.remove_updater(mobject.mechanics_updater)
            mobject.mechanics_updater = None
        return mobject


class Introduccion(MechanicsScene, Intro):
    def setup(self):
        MechanicsScene.setup(self)
        Intro.setup(self)
        self.logo.scale(0.5).to_corner(DR)

    def construct(self):
        dot = Dot(color=ORANGE).to_edge(UP)
        ground = self.make_ground(y=-3.75)
        self.play(Create(ground), FadeIn(dot))
        Intro.construct(self)
        self.make_rigid_mobject(dot)
        self.play(UpdateFromFunc(
            dot,
            lambda m: dot.mechanics_updater(m, dt=1 / self.camera.frame_rate),
            run_time=5
        ))
        self.stop_rigid_mobject(dot)
        self.play(dot.animate.to_corner(UL), FadeOut(self.logo))
        ax = Axes(
            x_length=5,
            y_length=8,
            x_range=[0, 5, 1],
            y_range=[0, 8, 1],
            tips=False
        ).scale_to_fit_height(7.75)
        ax.next_to(ground, UP, 0)
        ax.to_edge(RIGHT)
        x_axis: NumberLine = ax.get_x_axis()
        x_axis.add_numbers(range(1, 5), direction=UP)
        y_axis: NumberLine = ax.get_y_axis()
        y_axis.add_numbers(range(1, 8), direction=LEFT)
        ax.shift(0.1 * DOWN)
        labels = VGroup(
            ax.get_x_axis_label("t", direction=UP),
            ax.get_y_axis_label("y", direction=RIGHT)
        )
        y = ax.p2c(dot.get_center())[1]
        graph = VMobject(color=ORANGE, stroke_width=2)
        dashed_line = DashedLine(ax.c2p(0, y), dot.get_center())
        current_t = -1 / self.camera.frame_rate
        
        def graph_updater(m: VMobject, dt):
            nonlocal current_t
            current_y = ax.p2c(dot.get_center())[1]
            if graph.has_no_points():
                graph.start_new_path(ax.c2p(0, y))
            m.add_points_as_corners([ax.c2p(current_t, current_y)])
        
        def dashed_line_updater(m: DashedLine, dt):
            nonlocal current_t
            m.put_start_and_end_on(ax.c2p(current_t, ax.p2c(dot.get_center())[1]), dot.get_center())
            current_t += dt
        
        self.play(Write(VGroup(ax, labels)))
        self.add(dashed_line, dot, graph)
        self.play(Create(dashed_line))
        self.make_rigid_mobject(dot)
        self.play(
            UpdateFromFunc(dot, lambda m: dot.mechanics_updater(m, dt=1 / self.camera.frame_rate)),
            UpdateFromFunc(graph, lambda m: graph_updater(m, dt=1 / self.camera.frame_rate)),
            UpdateFromFunc(dashed_line, lambda m: dashed_line_updater(m, dt=1 / self.camera.frame_rate)),
            run_time=5
        )
        self.stop_rigid_mobject(dot)
        self.wait()

        self.play(
            dot.animate.to_corner(UL),
            FadeOut(dashed_line)
        )
        group = VGroup(ax, labels, dot, graph, ground)
        for mob in group:
            mob.save_state()
        self.play(group.animate.fade(0.75))
        quiero = MathTex("\\text{¿}", "v(3)", "\\text{?}")
        self.play(LaggedStart(*[FadeIn(submob, scale=2) for submob in quiero], lag_ratio=1 / 3))
        self.wait()

        self.play(FadeOut(quiero), *[Restore(mob) for mob in group])
        dashed_line = DashedLine(ax.c2p(0, y), dot.get_center())
        self.bring_to_back(dashed_line)
        self.play(Create(dashed_line))
        self.make_rigid_mobject(dot)
        current_t = -1 / self.camera.frame_rate
        self.play(
            UpdateFromFunc(dot, lambda m: dot.mechanics_updater(m, dt=1 / self.camera.frame_rate)),
            UpdateFromFunc(dashed_line, lambda m: dashed_line_updater(m, dt=1 / self.camera.frame_rate)),
            run_time=3
        )
        self.stop_rigid_mobject(dot)

        dot = Dot(ax.c2p(3, ax.p2c(dot.get_center())[1]))
        self.play(FadeIn(dot, scale=2))
        self.wait()


class Introduccion2(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_color": GREY, "stroke_opacity": 0.5})
        plane.add_coordinates()
        self.play(Write(plane))

        def func(x):
            return 4 / 343 * x ** 3

        graph = plane.plot(func, color=ORANGE)
        self.play(Create(graph))
        self.wait()
        
        x1 = ValueTracker(-4)
        x2 = ValueTracker(-2)

        def line_g_func():
            base_line_g = plane.get_secant_slope_group(
                x=x1.get_value(),
                graph=graph,
                dx=x2.get_value() - x1.get_value(),
                secant_line_color=LIGHTER_GREY,
                dx_line_color=LIGHTER_GREY,
                dy_line_color=LIGHTER_GREY,
                dx_label="\\Delta x",
                dy_label="\\Delta y"
            )
            base_line_g.dx_label[0][1].set_color(ORANGE)
            base_line_g.df_label[0][1].set_color(ORANGE)
            return base_line_g

        line_g = always_redraw(line_g_func)
        x1_dot = always_redraw(lambda: Dot(plane.i2gp(x1.get_value(), graph)))
        x2_dot = always_redraw(lambda: Dot(plane.i2gp(x2.get_value(), graph)))
        self.play(Write(line_g), Create(x1_dot), Create(x2_dot), run_time=2)
        self.wait()
        self.play(x1.animate.set_value(2), x2.animate.set_value(5), run_time=3)
        self.wait()

        pendiente = MathTex("m", "=", "{\\Delta", "y", "\\over", "\\Delta", "x}", color=LIGHTER_GREY)
        pendiente.set_color_by_tex_to_color_map({"y": ORANGE, "x": ORANGE, "m": ORANGE})
        rect = SurroundingRectangle(pendiente, color=ORANGE).set_fill(BLACK, opacity=1)
        pendiente_g = VGroup(rect, pendiente).to_corner(UL)
        self.play(Write(pendiente_g))
        self.wait()

        x = ValueTracker(-3)

        def derivada(x):
            return 12 / 343 * x ** 2

        def derivada_line_g_func():
            base_derivada_line_g = get_tangent_line(func, derivada, x.get_value(), color=LIGHTER_GREY)
            return base_derivada_line_g
        
        derivada_line_g = always_redraw(derivada_line_g_func)
        self.play(Create(derivada_line_g))
        self.wait()
        self.play(x.animate.set_value(2), run_time=3)
        self.wait()
        self.play(x.animate.set_value(-5), run_time=3)
        self.wait()


class VideoIntro(Intro):
    pass


class RecordemosLimites(Scene):
    def construct(self):
        lim = MathTex(
            "\\lim_{", "x\\relax", "\\to", "a\\relax}", "f\\relax", "(", "x\\relax", ")", "=",
            "L\\relax", font_size=96
        )
        lim.set_color_by_tex_to_color_map({
            "x\\relax": ORANGE,
            "f\\relax": RED,
            "L\\relax": LIGHT_GREY,
            "a\\relax": LIGHT_GREY
        })
        self.play(FadeIn(lim, scale=2))
        self.play(ApplyWave(lim))
        self.wait()

        epsilon_delta = MathTex(
            "(", "\\forall", "\\varepsilon", ">", "0", ")", "(", "\\exists", "\\delta", ">", "0", ")",
            "(", "\\forall", "x\\relax", "\\in", "\\operatorname{Dom}", "f\\relax", ")", "(", "0", "<", "\\lvert",
            "x\\relax", "-", "a\\relax", "\\rvert", "<", "\\delta", ")", "\\implies",
            "\\lvert", "f\\relax", "(", "x\\relax", ")", "-", "L\\relax", "\\rvert", "<", "\\varepsilon", ")"
        ).set_color_by_tex_to_color_map({
            "x\\relax": ORANGE,
            "f\\relax": RED,
            "L\\relax": LIGHT_GREY,
            "a\\relax": LIGHT_GREY,
            "\\varepsilon": ORANGE,
            "\\delta": ORANGE
        })
        epsilon_delta.scale(0.75)
        epsilon_delta.next_to(lim, DOWN)
        self.play(TransformMatchingTex(lim.copy(), epsilon_delta))
        self.wait()

        self.play(FadeOut(epsilon_delta), lim.animate.scale(0.5).to_corner(UL))
        rect = SurroundingRectangle(lim, color=ORANGE).set_fill(BLACK, opacity=1)
        self.bring_to_back(rect)
        self.play(Write(rect))
        plane = NumberPlane(background_line_style={"stroke_color": GREY, "stroke_opacity": 0.5})
        plane.add_coordinates()
        self.bring_to_back(plane)
        self.play(Write(plane))
        self.wait()
        
        def almost_cubic(x):
            return 4 / 343 * x ** 3 if x != 0 else -2
        
        graph1 = plane.plot(almost_cubic, x_range=[-7, -0.06], color=ORANGE).reverse_points()
        graph2 = plane.plot(almost_cubic, x_range=[0.06, 7], color=ORANGE)
        empty_point = Dot(plane.c2p(0, 0), color=BLACK).set_stroke(ORANGE, width=4)
        point = Dot(plane.c2p(0, -2), color=ORANGE)
        graph = VGroup(graph1, empty_point, point, graph2)
        self.play(*[Write(mob) for mob in graph])
        graph1.reverse_points()
        self.wait()

        lim_to_0 = MathTex(
            "\\lim_{", "x\\relax", "\\to", "0\\relax}", "f\\relax", "(", "x\\relax", ")", "=",
            "0\\relax"
        )
        lim_to_0.set_color_by_tex_to_color_map({
            "x\\relax": ORANGE,
            "f\\relax": RED,
            "0\\relax": LIGHT_GREY
        })
        lim_to_0.move_to(lim)
        self.play(TransformMatchingTex(lim, lim_to_0))
        self.wait()

        lo_que_busca1 = MathTex("\\text{El límite no evalúa en }", "x\\relax", "=", "a\\relax", "\\text{,}")
        lo_que_busca2 = MathTex("\\text{sino que es el valor al que }", "f\\relax", "(", "x\\relax", ")")
        lo_que_busca3 = MathTex("\\text{se acerca cuando }", "x\\relax", "\\text{ se acerca a }", "a\\relax", "\\text{.}")
        lo_que_busca = VGroup(lo_que_busca1, lo_que_busca2, lo_que_busca3).arrange(DOWN)
        for m in lo_que_busca:
            m.set_color_by_tex_to_color_map({
                "x\\relax": ORANGE,
                "f\\relax": RED,
                "a\\relax": LIGHT_GREY
            })
        rect2 = SurroundingRectangle(lo_que_busca, color=ORANGE).set_fill(BLACK, opacity=1)
        lo_que_busca_g = VGroup(rect2, lo_que_busca).to_edge(DOWN)
        self.play(Write(rect2), LaggedStart(*[FadeIn(sm, scale=2)
                                              for mob in lo_que_busca for submob in mob for sm in submob]))
        self.wait()

        self.play(FadeOut(lo_que_busca_g))
        
        left_x = ValueTracker(-6)
        right_x = ValueTracker(6)
        left_dot = always_redraw(lambda: Dot(plane.c2p(left_x.get_value(), almost_cubic(left_x.get_value()))))
        right_dot = always_redraw(lambda: Dot(plane.c2p(right_x.get_value(), almost_cubic(right_x.get_value()))))
        left_lines = always_redraw(lambda: plane.get_lines_to_point(left_dot.get_center(), color=LIGHT_GREY))
        right_lines = always_redraw(lambda: plane.get_lines_to_point(right_dot.get_center(), color=LIGHT_GREY))
        left_dot_update_func = left_dot.get_updaters()[0]
        left_dot.clear_updaters()
        right_dot_update_func = right_dot.get_updaters()[0]
        right_dot.clear_updaters()
        left_lines_update_func = left_lines.get_updaters()[0]
        left_lines.clear_updaters()
        right_lines_update_func = right_lines.get_updaters()[0]
        right_lines.clear_updaters()
        self.play(Create(left_lines), Create(right_lines), FadeIn(left_dot, scale=2), FadeIn(right_dot, scale=2))
        self.wait()
        self.play(
            left_x.animate.set_value(-0.08),
            right_x.animate.set_value(0.08),
            UpdateFromFunc(left_dot, left_dot_update_func),
            UpdateFromFunc(right_dot, right_dot_update_func),
            UpdateFromFunc(left_lines, left_lines_update_func),
            UpdateFromFunc(right_lines, right_lines_update_func),
            run_time=3,
            rate_func=ease_in_out_expo
        )
        self.wait()
        self.play(Circumscribe(empty_point, color=ORANGE))
        self.wait()
        cross = Cross(point).scale(4)
        self.play(Create(cross))
        self.play(FadeOut(cross))
        self.wait()


class RectaSecante(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_color": GREY, "stroke_opacity": 0.5})
        self.play(Write(plane))

        def cubic(x):
            return 4 / 343 * x ** 3
        
        graph = plane.plot(cubic, x_range=[-7, 7], color=ORANGE)
        self.play(Create(graph))
        self.wait()

        x1 = ValueTracker(-4)
        x2 = ValueTracker(-2)
        
        def secant_line_func():
            base_secant_line =  plane.get_secant_slope_group(
                x=x1.get_value(),
                graph=graph,
                dx=x2.get_value() - x1.get_value(),
                secant_line_color=LIGHTER_GREY,
                dx_line_color=LIGHTER_GREY,
                dy_line_color=LIGHTER_GREY,
                dx_label="\\Delta x",
                dy_label="\\Delta y"
            )
            base_secant_line.dx_label[0][1].set_color(ORANGE)
            base_secant_line.df_label[0][1].set_color(ORANGE)
            return base_secant_line
        
        secant_line = always_redraw(secant_line_func)
        x1_dot = always_redraw(lambda: Dot(plane.i2gp(x1.get_value(), graph)))
        x2_dot = always_redraw(lambda: Dot(plane.i2gp(x2.get_value(), graph)))
        self.play(Write(secant_line), Create(x1_dot), Create(x2_dot), run_time=2)
        self.wait()
        self.play(x1.animate.set_value(2), x2.animate.set_value(5), run_time=3)
        self.wait()

        pendiente = MathTex("m", "=", "{\\Delta", "y", "\\over", "\\Delta", "x}", color=LIGHTER_GREY)
        pendiente.set_color_by_tex_to_color_map({"y": ORANGE, "x": ORANGE, "m": ORANGE})
        rect = SurroundingRectangle(pendiente, color=ORANGE).set_fill(BLACK, opacity=1)
        pendiente_g = VGroup(rect, pendiente).to_corner(UL)
        self.play(Write(pendiente_g))
        self.wait()

        p1, p2 = MathTex("P_1", color=ORANGE), MathTex("P_2", color=ORANGE)
        p1.next_to(x1_dot, UL, SMALL_BUFF)
        p2.next_to(x2_dot, UL, SMALL_BUFF)
        self.play(DrawBorderThenFill(p1), DrawBorderThenFill(p2))
        self.wait()

        p1_coords = MathTex("P_1", "=", "(", "x", ",", "f", "(", "x", ")", ")")
        p1_coords.set_color_by_tex_to_color_map({"P_1": ORANGE, "x": ORANGE, "f": RED})
        p2_coords = MathTex("P_2", "=", "(", "x", "+", "\\Delta", "x", ",", "f", "(", "x", "+", "\\Delta", "x", ")", ")")
        p2_coords.set_color_by_tex_to_color_map({"P_2": ORANGE, "x": ORANGE, "f": RED})
        p_coords = VGroup(p1_coords, p2_coords).arrange(DOWN).to_corner(DL)
        rect2 = SurroundingRectangle(p_coords, color=ORANGE).set_fill(BLACK, opacity=1)
        p_coords.add_to_back(rect2)
        self.play(Write(rect2), Write(p1_coords))
        self.wait()

        lines_to_x1 = plane.get_lines_to_point(x1_dot.get_center(), color=LIGHT_GREY)
        lines_to_x2 = plane.get_lines_to_point(x2_dot.get_center(), color=LIGHT_GREY)
        t_labels = VGroup()

        for x, [label1, label2] in zip(
            [x1, x2],
            [
                (["x"], ["f", "(", "x", ")"]),
                (["x", "+", "\\Delta", "x"], ["f", "(", "x", "+", "\\Delta", "x", ")"])
            ]
        ):
            t_labels.add(get_T_to_val(
                plane,
                x.get_value(),
                t_label=MathTex(*label1).set_color_by_tex("x", ORANGE)
            ))
            t_labels.add(get_T_to_val(
                plane,
                cubic(x.get_value()),
                t_label=MathTex(*label2).set_color_by_tex_to_color_map({"x": ORANGE, "f": RED}),
                is_x_axis=False
            ))
        
        p1_t_labels = t_labels[:2]
        p2_t_labels = t_labels[2:]
        
        self.bring_to_back(lines_to_x1)
        self.play(Create(lines_to_x1), FadeIn(p1_t_labels, scale=2))
        self.wait()

        self.bring_to_back(lines_to_x2)
        self.play(
            Create(lines_to_x2),
            FadeIn(p2_t_labels, scale=2)
        )
        self.wait()
        self.play(Write(p2_coords))
        self.wait()

        self.play(FadeOut(
            t_labels,
            lines_to_x1,
            lines_to_x2,
            p1,
            p2
        ))

        pendiente2 = MathTex(
            "m", "=", "{f", "(", "x", "+", "\\Delta", "x", ")",
            "-", "f", "(", "x", ")", "\\over", "\\Delta", "x}"
        )
        pendiente2.set_color_by_tex_to_color_map({"f": RED, "x": ORANGE, "m": ORANGE})
        rect3 = SurroundingRectangle(pendiente2, color=ORANGE).set_fill(BLACK, opacity=1)
        pendiente2_g = VGroup(rect3, pendiente2).to_corner(UL)
        self.play(ReplacementTransform(pendiente_g, pendiente2_g))
        self.wait()

        delta_x_equals_0_question = MathTex("\\text{¿}", "\\Delta", "x\\relax", "=", "0", "\\text{?}")
        delta_x_equals_0_question.set_color_by_tex("x\\relax", ORANGE)
        rect4 = SurroundingRectangle(delta_x_equals_0_question, color=ORANGE).set_fill(BLACK, opacity=1)
        delta_x_equals_0_question_g = VGroup(rect4, delta_x_equals_0_question).to_edge(UP)
        self.play(DrawBorderThenFill(delta_x_equals_0_question_g))
        self.wait()
        cross = Cross(delta_x_equals_0_question_g)
        self.play(Create(cross))
        self.wait()
        self.play(FadeOut(delta_x_equals_0_question_g, cross))
        self.wait()

        tiende = MathTex("\\Delta", "x\\relax", "\\to", "0")
        tiende.set_color_by_tex("x\\relax", ORANGE)
        rect5 = SurroundingRectangle(tiende, color=ORANGE).set_fill(BLACK, opacity=1)
        tiende_g = VGroup(rect5, tiende).to_edge(UP)
        self.play(DrawBorderThenFill(tiende_g))
        self.wait()

        self.play(x2.animate.set_value(2.01), rate_func=ease_in_out_expo, run_time=3)
        self.wait()

        pendiente3 = MathTex("m", "=", "\\lim_{", "\\Delta", "x", "\\to", "0}", "{f", "(", "x", "+", "\\Delta", "x", ")",
                             "-", "f", "(", "x", ")", "\\over", "\\Delta", "x}")
        pendiente3.set_color_by_tex_to_color_map({"f": RED, "x": ORANGE, "m": ORANGE})
        rect6 = SurroundingRectangle(pendiente3, color=ORANGE).set_fill(BLACK, opacity=1)
        pendiente3_g = VGroup(rect6, pendiente3).to_corner(UL)
        self.play(FadeOut(tiende_g))
        self.play(ReplacementTransform(pendiente2_g, pendiente3_g))
        self.wait()

        derivada = MathTex("f", "'", "(", "x", ")", "=", "\\lim_{", "\\Delta", "x", "\\to", "0}", "{f", "(", "x", "+",
                            "\\Delta", "x", ")", "-", "f", "(", "x", ")", "\\over", "\\Delta", "x}")
        derivada.set_color_by_tex_to_color_map({"f": RED, "x": ORANGE, "m": ORANGE})
        rect7 = SurroundingRectangle(derivada, color=ORANGE).set_fill(BLACK, opacity=1)
        derivada_g = VGroup(rect7, derivada).to_corner(UL)
        self.play(ReplacementTransform(pendiente3_g, derivada_g))
        self.wait()

        self.play(x1.animate.set_value(-2), x2.animate.set_value(-1.99), run_time=3)
        self.wait()
        self.play(x1.animate.set_value(2), x2.animate.set_value(2.01), run_time=3)
        self.wait()


class Conclusion(Outro):
    watch_next_txt = "Atento a esta lista"

    def construct(self):
        formula = MathTex("f", "'", "(", "x", ")", ":", "=", "\\lim_{", "\\Delta", "x", "\\to", "0}", "{f", "(", "x", "+",
                            "\\Delta", "x", ")", "-", "f", "(", "x", ")", "\\over", "\\Delta", "x}", font_size=60)
        formula.set_color_by_tex_to_color_map({"f": RED, "x": ORANGE, "m": ORANGE})
        self.play(LaggedStart(*[FadeIn(sm, scale=2) for mob in formula for sm in mob]))
        self.wait()

        self.play(Circumscribe(formula, color=ORANGE))
        self.wait()

        self.play(FadeOut(formula, scale=10))
        self.wait()

        super().construct()
