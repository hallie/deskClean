#!/usr/bin/python
import logging
import os

from optparse import OptionParser

DIR_MAP = {
    "Desktop": "Desktop",
    "Documents": "Documents",
    "GIFs": "Pictures/GIFs",
    "HTML": "Documents/HTML",
    "Installers": "Downloads/Installers",
    "Pictures": "Pictures",
    "PDFs": "Documents/PDFs",
    "Screen Shot": "Pictures/ScreenShots",
    # "TextFile": "/Documents/TextFiles/",
    "XML": "Documents/XML",
}

EXT_DIR_MAP = {
    "Documents": [".doc", ".docx"],
    "GIFs": [".gif"],
    "HTML": [".html"],
    "Installers": [".exe",".dmg", ".pkg", ".tar", ".zip"],
    "PDFs": [".pdf"],
    "Pictures": [".jpg", ".jpeg", ".png"],
    # "TextFile": [".txt", "rtf"],
    "XML": [".xml"],
}

log = logging.getLogger(__name__)
handler = logging.FileHandler('/var/tmp/desk_clean.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.WARNING)

def _get_sorted_files_from_look_path(base_dir, look_path):
    sorted_files = {key:[] for key in DIR_MAP.keys()}
    sorted_files[look_path] = []
    dir_path = os.path.join(base_dir, look_path)
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if not os.path.isfile(item_path):
            continue
        file_name, file_ext = os.path.splitext(item)
        if ' '.join(file_name.split(' ')[:2]) == 'Screen Shot':
            new_name = ' '.join(file_name.split(' ')[2:]) + file_ext
            sorted_files['Screen Shot'].append(new_name)
            continue
        correct_dir = next((key for key in EXT_DIR_MAP
                            if file_ext in set(EXT_DIR_MAP[key])), look_path)
        sorted_files[correct_dir].append(item)
    return sorted_files

def _move_all_sorted_files(base_dir, look_path):
    sorted_files = _get_sorted_files_from_look_path(base_dir, look_path)
    for key in sorted_files:
        if key in DIR_MAP:
            mv = os.path.join(base_dir, DIR_MAP[key])
        else:
            mv = os.path.join(base_dir, look_path)
        log.info(mv)
        for val in sorted_files[key]:
            if key == 'Screen Shot':
                name = os.path.join(base_dir, look_path, 'Screen Shot ' + val)
            else:
                name = os.path.join(base_dir, look_path, val)
            rename = os.path.join(mv, val)
            print "\t%s -> %s" % (name, rename)
            log.info("\t%s -> %s" % (name, rename))
            os.rename(name, rename)
    return

parser = OptionParser()
parser.add_option("-d", "--directory", dest="directory",
                  default="Desktop", help="The directory to clean")

if __name__ == '__main__':
    base_dir = '/Users/%s' % os.getlogin()
    options, args = parser.parse_args()
    _move_all_sorted_files(base_dir, options.directory)
