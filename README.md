# pptxdiff
pptxdiff is a tool to show the difference of two PowerPoint presentation files (.pptx files) as a text

## Dependencies
- Python 3.7.6
  - python-pptx

## Usage

```sh
$ python pptxdiff.py <PPTX_FILE_1> <PPTX_FILE_1>
```

## Sample

```sh
$ python pptxdiff.py Checkpoint.pptx Checkpoint2.pptx 

Slide2 d Slide2
<<<
Outline
Collecting data
Annotation
Developing CNN model
>>>


Slide5 c Slide4
<<<
Annotation
>>>
Annotation???

Slide6 a Slide5
<<<

>>>
Completely New Slide!!
Yeahhh!!!!!!

Slide6 c Slide6
<<<
Annotation
>>>
Slightly different slide
```