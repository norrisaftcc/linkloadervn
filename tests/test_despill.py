"""Tests for tools/assets/despill.py, using synthetic images.

Each test builds a small image in memory. No project art is touched.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools", "assets"))

import despill  # noqa: E402

MAGENTA = (255, 0, 255, 255)
BROWN = (120, 80, 60, 255)
BLACK = (10, 10, 10, 255)
CLEAR = (0, 0, 0, 0)


def sprite_with_rim(rim_alpha=255, glow_width=0):
    """A 20x20 image: brown square in the middle, magenta rim, then an
    optional magenta glow, then transparency."""
    im = Image.new("RGBA", (20, 20), CLEAR)
    for y in range(20):
        for x in range(20):
            edge = min(x, y, 19 - x, 19 - y)
            if edge >= 6:
                im.putpixel((x, y), BROWN)
            elif edge == 5:
                im.putpixel((x, y), (255, 0, 255, rim_alpha))
            elif glow_width and edge >= 5 - glow_width:
                im.putpixel((x, y), (255, 0, 255, 60))
    return im


def test_rim_touching_outside_is_halo():
    halo, enclosed = despill.scan_image(sprite_with_rim())
    assert halo > 0
    assert enclosed == 0


def test_rim_is_recoloured_from_clean_art():
    fixed = despill.despill_image(sprite_with_rim())
    r, g, b, a = fixed.getpixel((5, 10))
    assert (r, g, b) == BROWN[:3]
    assert a == 255
    assert despill.scan_image(fixed)[0] == 0


def test_wide_glow_far_from_art_becomes_transparent():
    fixed = despill.despill_image(sprite_with_rim(glow_width=4))
    assert fixed.getpixel((1, 10))[3] == 0
    assert despill.scan_image(fixed)[0] == 0


def test_enclosed_magenta_is_untouched():
    im = Image.new("RGBA", (20, 20), CLEAR)
    for y in range(2, 18):
        for x in range(2, 18):
            inside = 5 <= x <= 14 and 5 <= y <= 14
            im.putpixel((x, y), MAGENTA if inside else BLACK)
    halo, enclosed = despill.scan_image(im)
    assert halo == 0
    assert enclosed == 100
    assert despill.despill_image(im).tobytes() == im.tobytes()


def test_transparent_and_neutral_pixels_are_untouched():
    im = Image.new("RGBA", (10, 10), CLEAR)
    im.putpixel((5, 5), (128, 128, 128, 90))
    assert despill.despill_image(im).tobytes() == im.tobytes()


def test_scan_exit_status(tmp_path):
    sprite_with_rim().save(tmp_path / "bad.png")
    assert despill.main(["--scan", str(tmp_path)]) == 1
    despill.main(["--fix", str(tmp_path / "bad.png")])
    assert despill.main(["--scan", str(tmp_path)]) == 0


def test_dark_and_pale_glow_colours_count_as_magenta():
    import numpy as np
    for rgb in [(13, 0, 7), (194, 80, 150), (172, 90, 136), (255, 0, 255)]:
        r, g, b = (np.array([v]) for v in rgb)
        assert despill.is_magenta(r, g, b)[0], rgb


def test_skin_hat_and_shadow_do_not_count_as_magenta():
    import numpy as np
    for rgb in [(120, 80, 60), (150, 60, 70), (230, 200, 210), (4, 2, 3), (128, 128, 128)]:
        r, g, b = (np.array([v]) for v in rgb)
        assert not despill.is_magenta(r, g, b)[0], rgb
