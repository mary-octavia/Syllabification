# -*- coding: latin-1 -*-
"""
Quick and dirty rule-based orthographic syllabification algorithm for Romanian
===================================================

This algorithm follows the end-of-the-line hyphenation rules listed in 
DOOM3 and applies them to the entire word in order to obtain an 
"orthographic syllabification", which is distinct from proper syllabication
because the rules sometimes violate the MOP.

This code was written for a rule-based model as described in:
Liviu P. Dinu, Vlad Niculae, Octavia-Maria Sulea. Romanian Syllabication 
Using Machine Learning. TSD 2013: 450-456
"""
# Author: Octavia-Maria Sulea
# License: BSD 3

voc="aeiouy"
cons="bcdfghjklmnprstvxz"
liquid="lr"
stop="bcdfghptv"
cc_o=["ch", "gh", "gv", "cv", "sp", "sc", "st", "sf", "zb", "zg", "zd", "zv", "jg", "jd", "sm", "sn", "sl", "zm", "zl", "jn", "tr", "cl", "cr", "pl", "pr", "dr", "gl", "gr", "br", "bl", "fl", "fr", "vl", "vr", "hr", "hl", "ml", "mr"]
ccc_o=["spl", "spr", "str", "jgh", "zdr", "scl", "scr", "zgl", "zgr", "sfr"]
cc_e=["sc", "sf", "sl", "sp"]
dif=["ea", "oa", "ia", "ua", "iu", "uu", "ie", "ii"]
trif=["eoa", "eai", "eau", "iau"]
hiat=["aa","au", "ae", "ie", "ai", "ee", "oe", "oo", "yu"]

# use this set of constants for diacritics
# voc="aeiouăîâ"
# cons="bcdfghjklmnprsștțvxz"
# liquid="lr"
# stop="bcdfghptv"
# cc_o=["ch", "gh", "sp", "sc", "st", "sf", "zb", "zg", "zd", "zv", "șk", "șp", "șt", "șf", "șv", "jg", "jd", "sm", "sn", "sl", "șm", "șn", "șl", "zm", "zl", "jn", "tr", "cl", "cr", "pl", "pr", "dr", "gl", "gr", "br", "bl", "fl", "fr", "vl", "vr", "hr", "hl", "ml", "mr"]
# ccc_o=["spl", "spr", "șpl", "șpr", "str", "ștr", "jgh", "zdr", "scl", "scr", "zgl", "zgr", "sfr"]
# cc_e=["sc", "sf", "sl", "sp", "tr"]
# dif=["ea", "oa", "ia", "ua", "uă" "iu", "uu", "ie"]
# trif=["eoa", "eai", "eau", "iau"]
# hiat=["aa", "au", "ae","ie", "ai", "ee", "oe"]


def ccv(cuv, i):
    if cuv[i] in stop and cuv[i+1] in liquid: # stop+liquid
        cuv=cuv[:i] + '-' + cuv[i:] # split -CCV
    else: # C-CV
        cuv=cuv[:i+1] + '-' + cuv[i+1:] # split
    i = i + 3 # skip 
    return cuv, i

def cccv(cuv, i):
    if cuv[i+1:i+3] in cc_o: # last two Cs are a valid onset
        if cuv[i+1:i+3] in cc_e: # last two Cs are exceptions
            cuv = cuv[:i+2] + '-' + cuv[i+2:] # CC-C
        else: # valid onset    
            cuv = cuv[:i+1] + '-' + cuv[i+1:] # C-CC
            # print cuv
    else: # C-CC invalid
        cuv = cuv[:i+2] + '-' + cuv[i+2:] # CC-C
        # print cuv
    i = i + 4 # skip  
    return cuv, i    

def ccccv(cuv,i):
    if cuv[i+1:i+4] in ccc_o: # C-CCC
        cuv = cuv[:i+1] + '-' + cuv[i+1:]
    elif cuv[i+2:i+4] in cc_o: # CC-CC
        cuv=cuv[:i+2] + '-' + cuv[i+2:]
    else: # CCC-C
        cuv = cuv[:i+3] + '-' + cuv[i+3:]
    i = i + 5
    return cuv, i   

def vvv(cuv, i):
    if cuv[i:i+3] in trif: #e triftong (pleoape)
        i = i + 3 # skip triphthong 
    elif cuv[i+1:i+3] in dif:
        cuv=cuv[:i+1] + '-' + cuv[i+1:] #despart V-VV
        i = i + 4 # skip VVV-
        # print cuv
    else: # ambigous case we treat as triphthong
        i = i + 3 # skip without split
    return cuv, i


def syllabify(cuv):
    i, nucleu = 0, 0

    while i < len(cuv) - 1:
        # print i, cuv[i]
        if cuv[i] in voc: # starts with a vowel (V)
            nucleu = 1 # assume it's a nucleus
            if cuv[i+1] in voc: # VV
                if (i+2) <= len(cuv)-1: # cuv[i+2] exists
                    if cuv[i+2] in voc: # VVV (ex: ploua, pleoape)
                        if (i+3) <= len(cuv) - 1: # cuv(i+3) exists
                            if cuv[i+3] in voc: # VVVV
                                cuv = cuv[:i+2] + '-' + cuv[i+2:] # split VV-VV
                                i = i + 5
                            else: # VVVC
                                cuv, i = vvv(cuv, i)
                        else: # at the end with VVV
                            cuv, i = vvv(cuv, i)
                    else: # VVC
                        if cuv[i:i+2] in dif: # diphthong
                            i = i + 2 # skip it
                        elif cuv[i:i+2] in hiat: # hiatus
                            cuv = cuv[:i+1] + '-' + cuv[i+1:] # split it V-V
                            # print cuv
                            i = i + 3 # skip VV-
                        else: # ambiguous VV
                            i = i + 2 # skip it (NOTE: change here when more info is present)
                else: # at the end
                    i = i + 2
            else: # VC
                i = i + 1 # skip V
        else: # cuv[i] is a consonant (C)
            if nucleu == 0: # no nucleus found already
                i = i + 1 # we are at the onset => skip
            else: # there is a nucleus 
                if cuv[i+1] in cons: # CC
                    if (i + 2) < (len(cuv) - 1): # cuv[i+2] exists & not at the end
                        if cuv[i+2] in cons: # CCC
                            if (i + 3) < (len(cuv) - 1): # cuv[i+3] exists
                                if cuv[i+3] in cons: # CCCC
                                    if (i + 4) < (len(cuv) - 1):
                                        if cuv[i+4] in cons: # CCCCC (ex: optsprezece)
                                            cuv = cuv[:i+2] + '-' + cuv[i+2:]
                                            i = i + 6
                                        else: # CCCCV
                                            cuv, i = ccccv(cuv, i)
                                    else: # at the end
                                        if cuv[i+4] in cons: # CCCCC at the end
                                            i = i + 5 # skip to the end
                                        else: # CCCCV
                                            cuv, i = ccccv(cuv, i)
                                else: # CCCV            
                                    cuv, i = cccv(cuv, i)
                            else: # at the end
                                if cuv[i+3] in cons: # CCCC at the end
                                    i = i + 4
                                else: # CCCV at the end
                                    cuv, i = cccv(cuv, i)    
                        else: # CCV
                            cuv, i = ccv(cuv, i)
                    elif (i+2) == (len(cuv) - 1): # at the end
                        if cuv[i+2] in voc: # CCV at the end (problems with CCi)
                            cuv, i = ccv(cuv, i)   
                        else: # CCC at the end (ex: 'stm' from 'astm')
                            i = i + 3
                    else: # CC at the end
                        break
                else: # CV
                    cuv = cuv[:i] + '-' + cuv[i:] # split as -CV (acc. to MOP)
                    # print cuv
                    i = i + 2
    print cuv               
                

        
syllabify("lingvistica")