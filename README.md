filter\_images.py
============================

simple tool to filter many image files with conditions.

## install

```bash
python setup.py install
```

## usage

```bash
# our image
$ identify sample.jpg
sample.jpg JPEG 1280x720 1280x720+0+0 8-bit sRGB 66.6KB 0.010u 0:00.010
```

```bash
# filter with min width
$ echo sample.jpg | filterimages --width-min=300
sample.jpg
```

```bash
# if image file does not satisfy condition, no output made
$ echo sample.jpg | filterimages --width-min=2000
```

