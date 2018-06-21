import argparse as ap
from sys import stdin,stderr
from PIL import Image
import numpy as np

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def proc(pathstr, args):
    try:
        image = Image.open(pathstr)
        ok = True

        if args.width_min is not None and args.width_min > image.width:
            ok = False
        if args.width_max is not None and args.width_max < image.width:
            ok = False
        if args.height_min is not None and args.height_min > image.height:
            ok = False
        if args.height_max is not None and args.height_max < image.height:
            ok = False

        sat_avg = 0.

        if not all(v is None for v in [
            args.sat_avg_min, args.sat_avg_max, args.sat_stddev_min, args.sat_stddev_max]):
            hsv_arr = np.array(image.convert('HSV'), dtype=np.float32)
            s_arr = hsv_arr.transpose([2,0,1])[1].reshape([-1])

        if not all(v is None for v in [args.sat_avg_min, args.sat_avg_max]):
            sat_avg = np.average(s_arr)

        if args.sat_avg_min is not None:
            ok = ok and args.sat_avg_min <= sat_avg
        if args.sat_avg_max is not None:
            ok = ok and args.sat_avg_max >= sat_avg

        sat_stddev = 0.

        if not all(v is None for v in [args.sat_stddev_min, args.sat_stddev_max]):
            sat_stddev = np.std(s_arr)

        if args.sat_stddev_min is not None:
            ok = ok and args.sat_stddev_min <= sat_stddev
        if args.sat_stddev_max is not None:
            ok = ok and args.sat_stddev_max >= sat_stddev

        aspect_ratio = 0

        if not all(v is None for v in [args.aspect_min, args.aspect_max]):
            aspect_ratio = image.width / image.height
        if not all(v is None for v in [args.max_aspect_min, args.max_aspect_max]):
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
        print('FileNotFoundError: {}'.format(pathstr), file=stderr)
    except ValueError as e:
        print('ValueError(something occuerd on image conversion): {}'.format(pathstr), file=stderr)

def run():
    parser = ap.ArgumentParser(description="filter images with conditions")

    parser.add_argument("--sat-avg-min", type=float, default=None, metavar="VAL",
        help="ok if average of HSV sat >= VAL")
    parser.add_argument("--sat-avg-max", type=float, default=None, metavar="VAL",
        help="ok if average of HSV sat <= VAL")
    parser.add_argument("--sat-stddev-min", type=float, default=None, metavar="VAL",
        help="ok if standard deviation of HSV sat >= VAL")
    parser.add_argument("--sat-stddev-max", type=float, default=None, metavar="VAL",
        help="ok if standard deviation of HSV sat <= VAL")

    parser.add_argument("--width-min", type=float, default=None, metavar="VAL",
        help="ok if width >= VAL")
    parser.add_argument("--width-max", type=float, default=None, metavar="VAL",
        help="ok if width <= VAL")
    parser.add_argument("--height-min", type=float, default=None, metavar="VAL",
        help="ok if height >= VAL")
    parser.add_argument("--height-max", type=float, default=None, metavar="VAL",
        help="ok if height <= VAL")

    parser.add_argument("--aspect-min", type=float, default=None, metavar="VAL",
        help="ok if width / height >= VAL")
    parser.add_argument("--aspect-max", type=float, default=None, metavar="VAL",
        help="ok if width / height <= VAL")
    parser.add_argument("--max-aspect-min", type=float, default=None, metavar="VAL",
        help="ok if max(width / height, height / width) >= VAL")
    parser.add_argument("--max-aspect-max", type=float, default=None, metavar="VAL",
        help="ok if max(width / height, height / width) <= VAL")

    args =  parser.parse_args()

    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as p_exec:
        for line in stdin.readlines():
            line = line.rstrip()
            p_exec.submit(proc, line, args)

if __name__ == '__main__':
    run()

