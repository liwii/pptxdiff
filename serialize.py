import sys
import os
import json
from pptx import Presentation
from pptx.shapes.picture import Picture
from pptx.shapes.autoshape import Shape
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def color_str(rgb):
    return '#' + str.upper('%02x%02x%02x' % rgb)

def shape_repr_str(type, frame, info):
    head = "{} {}".format(type, frame)
    return head + json.dumps(info, indent=2)

def fig_repr(shape, frame):
    info = {
        'color': color_str(shape.fill.fore_color.rgb)
    }
    type_dict = {
        MSO_SHAPE.RECTANGLE: 'rectangle',
        MSO_SHAPE.ROUNDED_RECTANGLE: 'rounded_rectangle'
    }
    if shape.auto_shape_type in type_dict:
        info['type'] = type_dict[shape.auto_shape_type]
    else:
        info['type'] = shape.auto_shape_type
    return shape_repr_str('shape', frame, info)

def image_repr(shape, frame):
    info = {
        'image': shape.image.sha1
    } 
    return shape_repr_str('image', frame, info)

def text_repr(shape, frame):
    p = shape.text_frame.paragraphs[0]
    if len(p.runs) == 0:
        fontname = p.font.name
        fontsize = p.font.size
        fontcolor = p.font.color.rgb
    else:
        pfont = p.font
        rfont = p.runs[0].font
        if rfont.name is None:
            fontname = pfont.name
        else:
            fontname = rfont.name
        if rfont.size is None:
            fontsize = pfont.size
        else:
            fontsize = rfont.size
        if rfont.color.type is None:
            fontcolor = pfont.color.rgb
        else:
            fontcolor = rfont.color.rgb
    valign_dict = {
        MSO_ANCHOR.TOP: 'top',
        MSO_ANCHOR.MIDDLE: 'middle',
        MSO_ANCHOR.BOTTOM: 'bottom'
    }

    halign_dict = {
        PP_ALIGN.LEFT: 'left',
        PP_ALIGN.CENTER: 'center',
        PP_ALIGN.RIGHT: 'right'
    }

    info = {
        'value': shape.text,
        'font': fontname,
        'fontsize': fontsize / Pt(1),
        'fontcolor': color_str(fontcolor),
        'valign': valign_dict[shape.text_frame.vertical_anchor],
        'halign': halign_dict[p.alignment]
    }
    return shape_repr_str('text', frame, info)
    

def shape_frame(shape, slide_size):
    t, l, w, h = shape.top, shape.left, shape.width, shape.height
    sw, sh = slide_size
    x1 = int(100 * l / sw)
    y1 = int(100 * t / sh) 
    x2 = x1 + int(100 * w / sw)
    y2 = y1 + int(100 * h / sh)
    return [[x1, x2], [y1, y2]]

    
def shape_repr(shape, slide_size):
    frame = shape_frame(shape, slide_size)
    if isinstance(shape, Picture):
        return image_repr(shape, frame)
    elif shape.text_frame.paragraphs[0].font.name is not None:
        return text_repr(shape, frame)
    else:
        return fig_repr(shape, frame)


def slide_repr(slide, slide_size):
    shape_reprs = [shape_repr(shape, slide_size) for shape in slide.shapes]
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
