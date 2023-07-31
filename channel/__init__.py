from manim import *
from .logo import Logo
from .rule import Rule
from .grid import Grid
from .intro import Intro
from .outro import Outro
import os


config.background_color = "#222222"
Text.set_default(font="CMU Serif")
config.tex_template_file = os.getenv("DEFAULT_TEX_TEMPLATE")
config.tex_template.tex_compiler = "xelatex"
config.tex_template.output_format = ".xdv"
MathTex.set_default(tex_template=config.tex_template)
