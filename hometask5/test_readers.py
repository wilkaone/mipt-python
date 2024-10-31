import sys
import argparse

from utils.reader import image_reader as imread
from utils.reader import csv_reader, bin_reader, txt_reader, json_reader
from utils.processor import histogram
from utils.writer import csv_writer, bin_writer, txt_writer, image_writer, json_writer

from utils.image_toner import stat_correction, equalization, gamma_correction

def print_args_1():
    print(type(sys.argv))
    if (len(sys.argv) > 1):
        for param in sys.argv[1:]:
            print(param, type(param))
    return sys.argv[1:]

def init_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument ('-img','--img_path', default ='', help='Path to image')
    parser.add_argument ('-p','--path', default ='', help='Input file path ')
    parser.add_argument('-m', '--mode', default='', help='Input mode program: histogram (or hist), equalization (or eq), gamma_correction (or gc) or stat_correction (or sc)')
    parser.add_argument('-o', '--output', help='Save file path')

    return parser

if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args(sys.argv[1:])

    image = None
    hist = None

    if args.img_path == '':
        print('[test_readers.py]: img_path is missing')
        exit(0)
    image = imread.read_data(args.img_path)

    if args.output == '':
        print('[test_readers.py]: output (path) is missing')
        exit(0)
    
    if args.mode == 'histogram' or args.mode == 'hist':
        txt_writer.write_data(args.output, histogram.image_processing(image))
    elif args.mode == 'equalization' or args.mode == 'eq':
        #hist = histogram.image_processing(image)
        image_writer.write_data(args.output, equalization.processing(image))
    elif args.mode == 'gamma_correction' or args.mode == 'gc':
        image_writer.write_data(args.output, gamma_correction.processing(image, float(input("Enter gamma value for gamma correction (type float or int): "))))
    elif args.mode == 'stat_correction' or args.mode == 'sc':
        hist_template = None

        type = args.path.split('.')[-1]
        match type:
            case 'jpg':
                hist_template = histogram.image_processing(imread.read_data(args.path))
            case 'csv':
                hist_template = csv_reader.read_data(args.path)
            case 'bin':
                hist_template = bin_reader.read_data(args.path)
            case 'txt':
                hist_template = txt_reader.read_data(args.path)
            case 'json':
                hist_template = json_reader.read_data(args.path)
            case _:
                print('[test_readers.py]: type file not supported')
                exit(0)

        image_writer.write_data(args.output, stat_correction.processing(hist_template, image))
    else:
        print('[test_readers.py]: indefinite mode')
        exit(0)