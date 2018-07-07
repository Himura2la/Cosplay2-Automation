#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os, re, csv
from gimpfu import *
from gimpenums import *


def dbg(text): 
    pdb.gimp_message(text)


# --------------- MAIN ---------------
def script_main(image, drawable, img_dir, dest_dir):
       
    for file in os.listdir(unicode(img_dir)):
        if file.find(".xcf") == len(file) - 4:
            filename = os.path.join(img_dir, file)
            image = pdb.gimp_file_load(filename, filename)
            #display = pdb.gimp_display_new(image)
            
            # Do some stuff if you need
            
            merged = image.merge_visible_layers(1)
            filename = os.path.join(dest_dir, file.split(".xcf")[0] + ".png")
            
            pdb.file_png_save_defaults(image, merged, filename, filename)

        
# This is the plugin registration function
register(
    "python_fu_fest_export_zad",	# Function name
    "Выгрузить задники на фест",
    "bla bla bla tulafest.ru. Yuki no Odori is my native festival.",
    "Vladislav Glagolev",
    "Hokori Tori Anime Festival",
    "8/21/2016",
    "<Image>/Tools/Выгрузить задники!",
    "*",	# Image types
    [	# Input
        (PF_DIRNAME, 'img_dir', 'XCF folder', "H:\\Hokori Tori\\img\\zad"),
        (PF_DIRNAME, 'dest_dir', 'PNG folder', "H:\\Hokori Tori\\img\\zad_PNG")
    ],
    [],	# Return
    script_main
)

main()
