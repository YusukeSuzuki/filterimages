import argparse as ap
from sys import stdin
from PIL import Image
import numpy as np

def proc(pathstr, args):
    try:
        image = Image.open(pathstr)
        rgb_arr = np.array(image, dtype=np.float32)
        hsv_arr = np.array(image.convert('HSV'), dtype=np.float32)
        s_arr = hsv_arr.transpose([2,0,1])[1].reshape([-1])

        ok = True

        sat_avg = 0.

        if args.width_min is not None and args.width_min > image.width:
            ok = False
        if args.width_min is not None and args.width_max < image.width:
            ok = False
        if args.height_min is not None and args.height_min > image.height:
            ok = False
        if args.height_min is not None and args.height_max < image.height:
            ok = False

        if args.sat_avg_min is not None or args.sat_avg_max is not None:
            sat_avg = np.average(s_arr)

        if args.sat_avg_min is not None and args.sat_avg_min > sat_avg:
            ok = False
        if args.sat_avg_max is not None and args.sat_avg_max < sat_avg:
            ok = False

        aspect_ratio = 0

        if None in [args.aspect_min, args.aspect_max]:
            aspect_ratio = image.width / image.height
        if None in [args.max_aspect_min, args.max_aspect_max]:
            max_aspect_ratio = max(image.width, image.height) / min(image.width, image.height)

        if args.aspect_min is not None and args.aspect_min > aspect_ratio:
            ok = False
        if args.aspect_max is not None and args.aspect_max < aspect_ratio:
            ok = False
        if args.max_aspect_min is not None and args.max_aspect_min > max_aspect_ratio:
            ok = False
        if args.max_aspect_max is not None and args.max_aspect_max < max_aspect_ratio:
            ok = False

        if ok:
            print(pathstr)
    except FileNotFoundError as e:
        pass

def run():
    parser = ap.ArgumentParser(description="filter images with conditions")

    parser.add_argument("--sat-avg-min", type=float, default=None)
    parser.add_argument("--sat-avg-max", type=float, default=None)

    parser.add_argument("--width-min", type=float, default=None)
    parser.add_argument("--width-max", type=float, default=None)
    parser.add_argument("--height-min", type=float, default=None)
    parser.add_argument("--height-max", type=float, default=None)

    parser.add_argument("--aspect-min", type=float, default=None)
    parser.add_argument("--aspect-max", type=float, default=None)
    parser.add_argument("--max-aspect-min", type=float, default=None)
    parser.add_argument("--max-aspect-max", type=float, default=None)

    args =  parser.parse_args()

    for line in stdin.readlines():
        line = line.rstrip()
        proc(line, args)

if __name__ == '__main__':
    run()

