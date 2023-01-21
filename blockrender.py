import argparse
import copy
import math
import numpy as np
import png

from pathlib import Path
from svgwrite.container import Group
from svgwrite.drawing import Drawing
from svgwrite.filters import Filter
from svgwrite.shapes import Rect


def sprite(png_path):
    bitmap = png.Reader(filename=png_path)
    (_, _, reader, _) = bitmap.asRGBA8()

    rgba = np.array([], dtype="byte")
    for row in reader:
        rgba = np.append(rgba, np.array(row))

    rgba = rgba.reshape((-1, 4))

    svg = Group()
    for pixel_indx, (r, g, b, a) in enumerate(rgba):
        if a == 0:
            continue

        x_pos = pixel_indx % 16
        y_pos = math.floor(pixel_indx / 16)

        pixel = Rect(
            # Imperceptable increase in size prevents background showing thru
            size=(1.05, 1.05),
            insert=(x_pos, y_pos),
            fill=f"rgb({r}, {g}, {b})",
        )
        if a / 255. != 1.0:
            pixel['fill_opacity'] = a / 255.

        svg.add(pixel)

    return svg


# Thanks minecraft overviewer for a how-to
def block(drawing, top_svg, left_svg, right_svg):
    darken_by = 0.35
    darken = drawing.filter(id="darken")
    drawing.add(darken)
    fect = darken.feComponentTransfer()
    fect.feFuncR("linear", slope=darken_by)
    fect.feFuncG("linear", slope=darken_by)
    fect.feFuncB("linear", slope=darken_by)

    top_svg.translate(12, 0)
    top_svg.scale(1 + 1 / 16)
    top_svg.scale(1, 0.5)
    top_svg.rotate(angle=45)

    left_svg.translate(0, 6)
    left_svg.scale(0.75)
    # Not sure why 26.5deg is interesting, Overviewer says shear by 1.5 in y
    left_svg.skewY(26.5)

    right_svg['filter'] = "url(#darken)"
    right_svg.translate(12, 12)
    right_svg.scale(0.75)
    right_svg.skewY(-26.5)

    svg = Group()
    svg.add(top_svg)
    svg.add(left_svg)
    svg.add(right_svg)
    return svg


if __name__ == "__main__":
    parser = argparse.ArgumentParser("blockrender")
    parser.add_argument(
        "sprite",
        help="Path to a png sprite to render to svg",
    )
    parser.add_argument(
        "-o", "--outfile",
        help="Write svg to filename",
        required=False,
    )
    parser.add_argument(
        "-b", "--block",
        help="Render SPRITE to a block instead of a 2D sprite",
        action="store_true",
    )
    parser.add_argument(
        "-r", "--right",
        help="Png for the right face (requires --block)",
        required=False,
    )
    parser.add_argument(
        "-l", "--left",
        help="Png for the left face (requires --block)",
        required=False,
    )
    args = parser.parse_args()

    png_path = Path(args.sprite)

    svg_path = args.outfile \
        if args.outfile is not None else png_path.with_suffix(".svg")

    svg = Drawing(svg_path)

    grp = sprite(png_path)
    width, height = (16, 16)

    if args.block:
        left = sprite(args.left) \
            if args.left is not None else copy.deepcopy(grp)
        right = sprite(args.right) \
            if args.right is not None else copy.deepcopy(grp)

        grp = block(svg, grp, left, right)
        width, height = (24, 24)

    svg.add(grp)
    svg['width'] = width
    svg['height'] = height
    svg.save(svg_path)
