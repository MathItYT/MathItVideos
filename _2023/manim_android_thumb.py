from channel import *
from PIL import Image
from pathlib import Path


def get_android_logo():
    arr = np.array(Image.open("assets/Logo-Android.png"))
    r, g, b, a = arr.T
    mask = (r == 0) & (g == 0) & (b == 0) & (a == 255)
    arr[...,:][mask.T] = [255, 255, 255, 255]
    return ImageMobject(arr)


class Thumbnail(Scene):
    def construct(self):
        banner = ManimBanner()
        android_logo = get_android_logo().match_height(banner)
        en = Tex("EN", font_size=96)
        Group(banner, en, android_logo).arrange(RIGHT, buff=1)
        self.add(banner, en, android_logo)
