# -*- coding: utf-8 -*-
# Version date: Nov 07, 2021
# @author: Sara Brambilla

import os
import shutil
from class_def import *
from read_inputs import *


def create_plots_folder(gen_gif, img_specs: ImgClass, prj_folder: str):
    img_specs.save_dir = os.path.join(prj_folder, "Plots")
    if os.path.isdir(img_specs.save_dir):
        shutil.rmtree(img_specs.save_dir, ignore_errors=True, onerror=None)
    os.mkdir(img_specs.save_dir)

    if gen_gif == 1:
        img_specs.gif_dir = os.path.join(img_specs.save_dir, 'Gifs')
        if os.path.isdir(img_specs.gif_dir):
            shutil.rmtree(img_specs.gif_dir, ignore_errors=True, onerror=None)
        os.mkdir(img_specs.gif_dir)
    else:
        img_specs.gif_dir = []


def open_file(filename: str, howto: str):
    try:
        fid = open(filename, howto)
        return fid
    except IOError:
        print("Error while opening " + filename)
        input("PRESS ENTER TO CONTINUE.")
        sys.exit()


def get_times(is_ave_time: bool, q: GridClass):
    if is_ave_time is True:
        ntimes = q.ntimes_ave
        times = q.time_ave
    else:
        ntimes = q.ntimes
        times = q.time

    return ntimes, times
