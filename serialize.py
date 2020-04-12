import sys
import os
import json
from pptx import Presentation
from pptx.shapes.picture import Picture
from pptx.shapes.autoshape import Shape
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def shape_repr(shape, slide_size):
    if not isinstance(shape, Picture) and shape.text:
        return shape.text
    else:
        return None

def slide_repr(slide, slide_size):
    shape_reprs = list(filter(None, [shape_repr(shape, slide_size) for shape in slide.shapes]))
    return "\n".join(shape_reprs)

def main(filename):
    prs = Presentation(filename)
    slide_size = (prs.slide_width, prs.slide_height)
    slide_reprs = [slide_repr(slide, slide_size) for slide in prs.slides]
    f, _ = os.path.splitext(filename)
    slides_repr = "\n\n---\n\n".join(slide_reprs)
    print(slides_repr)


if __name__ == '__main__':
    main(sys.argv[1])
