#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs, os, re, csv
from gimpfu import *
from gimpenums import *


def dbg(text): 
    pdb.gimp_message(text)


# --------------- MAIN ---------------
def script_main(image, drawable, img_dir, data_file, csv_delimiter, csv_quotechar, dest_dir):
    
    # Reading data
    # with codecs.open(data_file, encoding='utf-8') as f:
        # data = csv.reader(f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        # rows = [[cell for cell in row] for row in data]
    # head = rows[0]
    # table = [{head[i]:rows[j][i] for i in range(len(head))} for j in range(1, len(rows))]
    
    for file in os.listdir(unicode(img_dir)):
        if file.find(".xcf") == len(file) - 4:
            filename = os.path.join(img_dir, file)
            image = pdb.gimp_file_load(filename, filename)
            #display = pdb.gimp_display_new(image)
            
            # Do stuff
            
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
        (PF_FILE, 'data_file', 'Data file', "H:\\Hokori Tori\\img\\prog.csv"),
        (PF_RADIO, 'csv_delimiter', ("CSV delimiter"), ',', (("Comma (,)", ','), ("Semicolon (;)", ';'))),
        (PF_RADIO, 'csv_quotechar', ("CSV quote char"), '"', (('Double quote (")', '"'), ("Single quote (')", "'"), ('Vertical bar (|)', '|'))),
        (PF_DIRNAME, 'dest_dir', 'PNG folder', "H:\\Hokori Tori\\img\\zad_PNG")
    ],
    [],	# Return
    script_main
)

main()
