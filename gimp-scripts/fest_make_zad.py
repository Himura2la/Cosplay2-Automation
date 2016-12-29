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
    with codecs.open(data_file, encoding='utf-8') as f:
        data = csv.reader(f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        rows = [[cell for cell in row] for row in data]
    head = rows[0]
    table = [{head[i]:rows[j][i] for i in range(len(head))} for j in range(1, len(rows))]
    
    w, h = pdb.gimp_image_width(image), pdb.gimp_image_height(image)
    src_layers = image.layers
    
    for zad in table:
        new_image = pdb.gimp_image_new(w, h, RGB)
        pdb.gimp_display_new(new_image)
        for layer in src_layers:
            new_layer = pdb.gimp_layer_new_from_drawable(layer, new_image)
            pdb.gimp_image_insert_layer(new_image, new_layer, None, 999)
            removed = False
            
            if pdb.gimp_item_is_text_layer(new_layer):
                text = pdb.gimp_text_layer_get_text(new_layer)
                for key, val in zad.iteritems():
                    old_text = text
                    text = text.replace('[' + key + ']', val) # Essence!!!
                    if old_text != text and val == "": # Replaced to empty string
                        pdb.gimp_image_remove_layer(new_image, new_layer)
                        removed = True
                if not removed:
                    pdb.gimp_text_layer_set_text(new_layer, text)

        filename = os.path.join(img_dir, "ID %03d .jpg" % int(zad["ID"]))
        if not os.path.isfile(filename):
            filename = os.path.join(img_dir, "ID %03d .png" % int(zad["ID"]))
        if not os.path.isfile(filename):
            filename = "H:\\Hokori Tori\\img\\Maskot_small.png"
        pic = pdb.gimp_file_load(filename, filename)
        pic_layer = pdb.gimp_layer_new_from_drawable(pic.layers[0], new_image)
        pdb.gimp_image_insert_layer(new_image, pic_layer, None, 0)
        ratio = float(pdb.gimp_drawable_width(pic_layer)) / float(pdb.gimp_drawable_height(pic_layer)) # h*r = w
        
        target_w, target_h = 760, 740
        
        if ratio < 1: # vertical
            pdb.gimp_layer_scale(pic_layer, int(target_h*ratio), target_h, True)
            abs_y = (768-target_h)/2
            abs_x = 507+772/2 - int(target_h*ratio/2)
        else: # horizontal
            pdb.gimp_layer_scale(pic_layer, target_w, int(target_w/ratio), True)
            abs_x = 507
            abs_y = 768/2 - int(target_w/ratio/2)
        
        offx, offy = pdb.gimp_drawable_offsets(pic_layer)
        offx, offy = abs_x - offx, abs_y - offy
        pdb.gimp_layer_translate(pic_layer, offx, offy)

        
        essence = "???"
        if "Название" in zad and zad["Название"] != "": essence = zad["Название"]
        elif "Фэндом" in zad and zad["Фэндом"] != "": essence = zad["Фэндом"]
        elif "Композиция" in zad and zad["Композиция"] != "": essence = zad["Композиция"]
        
        filename = "#%03d %s - %s.xcf" % (int(zad["ID"]), zad["Участник(и)"], essence)
        filename = "".join(i for i in filename if i not in '\/:*?<>|"')
        
        filename = os.path.join(dest_dir, filename)
        pdb.gimp_xcf_save(0, new_image, new_layer, filename, filename)
        saved_image = pdb.gimp_file_load(filename, filename)
        pdb.gimp_displays_reconnect(new_image, saved_image)
        pdb.gimp_image_clean_all(saved_image)
        
# This is the plugin registration function
register(
    "python_fu_fest_make_zad",	# Function name
    "Делать задники на фест",
    "bla bla bla tulafest.ru. Yuki no Odori is my native festival.",
    "Vladislav Glagolev",
    "Hokori Tori Anime Festival",
    "8/18/2016",
    "<Image>/Tools/Делать задники на фест!",
    "*",	# Image types
    [	# Input
        (PF_DIRNAME, 'img_dir', 'Images folder', "H:\\Hokori Tori\\img\\pic"),
        (PF_FILE, 'data_file', 'Data file', "H:\\Hokori Tori\\img\\data_cosband.csv"),
        (PF_RADIO, 'csv_delimiter', ("CSV delimiter"), ',', (("Comma (,)", ','), ("Semicolon (;)", ';'))),
        (PF_RADIO, 'csv_quotechar', ("CSV quote char"), '"', (('Double quote (")', '"'), ("Single quote (')", "'"), ('Vertical bar (|)', '|'))),
        (PF_DIRNAME, 'dest_dir', 'Output folder', "H:\\Hokori Tori\\img\\zad")
    ],
    [],	# Return
    script_main
)

main()
