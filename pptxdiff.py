import sys
import os 
from pptx import Presentation
from serialize import shape_repr
from lcs import LCS
def head(ls):
    return ls[0] if ls else None

def slide_repr(slide, slide_size):
    return [shape_repr(shape, slide_size) for shape in slide.shapes]

def labels(length, idx, head):
    if length > 0:
        return [head + str(idx + i) for i in range(length)]
    else:
        return [head + str(idx)]

def show_diff(lines1, lines2, idx1, idx2):
    labels1 = ", ".join(labels(len(lines1), idx1, "Slide"))
    labels2 = ", ".join(labels(len(lines2), idx2, "Slide"))
    if not labels1:
        print(labels1 + " a " + labels2)
    elif not labels2:
        print(labels1 + " d " + labels2)
    else:
        print(labels1 + " c " + labels2)
    print("<<<")
    print("\n---\n".join(["\n".join(els) for els in lines1]))
    print(">>>")
    print("\n---\n".join(["\n".join(els) for els in lines2]))
    print()
    

def main(file1, file2):
    prs1 = Presentation(file1)
    slide_size = (prs1.slide_width, prs1.slide_height)
    slides1 = [slide_repr(slide, slide_size) for slide in prs1.slides]
    prs2 = Presentation(file2)
    slides2 = [slide_repr(slide, slide_size) for slide in prs2.slides]
    lcs = LCS(slides1, slides2)
    for ((l1, i1), (l2, i2)) in lcs.diff():
        lines1 = [slides1[i + i1] for i in range(l1)]
        lines2 = [slides2[i + i2] for i in range(l2)]
        show_diff(lines1, lines2, i1, i2)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
