
from manim import *
from .logo import Logo
from .rule import Rule
from .grid import Grid
from .intro import Intro
from .outro import Outro


config.background_color = "#222222"
Text.set_default(font="CMU Serif")
preamble = TexTemplate.default_preamble.replace("english", "spanish")
tex_template = TexTemplate(preamble=preamble)
MathTex.set_default(tex_template=tex_template)
