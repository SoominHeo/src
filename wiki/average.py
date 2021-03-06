import sys
import os
sys.path.append(os.getcwd()+"\metric")

import check_translate_pair
import paragraph
import photo_check
import reading
import reference
import tree_compare

sys.path.insert(0, "./metric")

def average(sources_k, sources_e):
    lst = ['','','','','','']
    lst[0] = reference.reference(sources_k,sources_e)
    lst[1] = tree_compare.tree_compare(sources_k,sources_e)
    lst[2] = photo_check.photo_check(sources_k,sources_e)
    lst[3] = check_translate_pair.check_translate_pair(sources_k)
    lst[4] = paragraph.paragraph(sources_k,sources_e)
    lst[5] = reading.reading(sources_k,sources_e)

    return lst