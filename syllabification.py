# -*- coding: latin-1 -*-
"""
Quick and dirty MOP-based "proper" syllabification algorithm for Romanian
===================================================

This algorithm syllabifies Romanian words (written orthographically 
rather than in IPA) using the MOP and Ioana Chitoran's analysis 
of Romanian Phonology.

This code was initially written for a rule-based model as described in:
Liviu P. Dinu, Vlad Niculae, Octavia-Maria Sulea. Romanian Syllabication 
Using Machine Learning. TSD 2013: 450-456

but never adapted and tested on IPA written words.
"""
# Author: Octavia-Maria Sulea
# License: BSD 3

voc = "aeiouy"
cons = "bcdfghjklmnprstvxz"
cc_o = ["ch", "gh", "sp", "sc", "st", "sf", "zb", "zg", "zd", "zv", "jg", 
    "jd", "sm", "sn", "sl", "zm", "zl", "jn", "tr", "cl", "cr", "pl", "pr", 
    "dr", "gl", "gr", "br", "bl", "fl", "fr", "vl", "vr", "hr", "hl", "ml", "mr"]
ccc_o = ["spl", "spr", "str", "jgh", "zdr", "scl", "scr", "zgl", "zgr", "sfr"]
dif = ["ea", "oa", "ia", "ua", "iu", "uu", "ie", "ii"]
trif = ["eoa", "eai", "eau", "iau"]
hiat = ["aa","au", "ae", "ie", "ai", "ee", "oe", "oo", "yu"]

# use this set of constants for diacritics
# voc = "aeiouăîâ"
# cons = "bcdfghjklmnprsștțvxz"
# cc_o = ["ch", "gh", "sp", "sc", "st", "sf", "zb", "zg", "zd", 
    # "zv", "șk", "șp", "șt", "șf", "șv", "jg", "jd", "sm", "sn", 
    # "sl", "șm", "șn", "șl", "zm", "zl", "jn", "tr", "cl", "cr", 
    # "pl", "pr", "dr", "gl", "gr", "br", "bl", "fl", "fr", "vl", "vr", 
    # "hr", "hl", "ml", "mr"]
# ccc_o = ["spl", "spr", "șpl", "șpr", "str", "ștr", "jgh", "zdr", "scl", 
    # "scr", "zgl", "zgr", "sfr"]
# dif = ["ea", "oa", "ia", "ua", "uă" "iu", "uu", "ie"]
# trif = ["eoa", "eai", "eau", "iau"]
# hiat = ["aa", "au", "ae","ie", "ai", "ee", "oe"]


def ccv(cuv, i):
    if cuv[i:i+2] in cc_o: # -CCV
        cuv = cuv[:i] + '-' + cuv[i:] # split -CCV
        # print cuv
    else: #nu  decat C-CV
        cuv = cuv[:i+1] + '-' + cuv[i+1:] #despartim
        # print cuv
    i = i + 3 # skip CC-
    return cuv, i

def cccv(cuv, i):
    if cuv[i:i+3] in ccc_o: # -CCC
        cuv = cuv[:i] + '-' + cuv[i:] # split
        # print cuv
    elif cuv[i+1:i+3] in cc_o: # C-CC
        cuv = cuv[:i+1] + '-' + cuv[i+1:] # split 
        # print cuv
    else: # MOP => CC-C
        cuv = cuv[:i+2] + '-' + cuv[i+2:] # split 
        # print cuv
    i = i + 4 # skip      
    return cuv, i    

def ccccv(cuv,i):
    if cuv[i+1:i+4] in ccc_o: # C-CCC
        cuv = cuv[:i+1] + '-' + cuv[i+1:]
    elif cuv[i+2:i+4] in cc_o: # CC-CC
        cuv = cuv[:i+2] + '-' + cuv[i+2:]
    else: # CCC-C
        cuv = cuv[:i+3] + '-' + cuv[i+3:]
    i = i + 5
    return cuv, i   

def vvv(cuv, i):
    if cuv[i:i+3] in trif: # triphthong (ex: pleoape)
        i = i + 3 # skip triphthong
    elif cuv[i+1:i+3] in dif:
        cuv = cuv[:i+1] + '-' + cuv[i+1:] #despart V-VV
        i = i + 4 # skip VVV-
        #print cuv
    else: # ambiguous, treat as triphthong
        i = i + 3 # skip
    return cuv, i


def syllabify(cuv):
    i, nucleu = 0, 0

    while i < len(cuv) - 1:
        # print i, cuv[i]
        if cuv[i] in voc: # starts with a vowel (V)
            nucleu = 1 # mark nucleus
            if cuv[i+1] in voc: # VV
                if (i+2)<=len(cuv)-1: # cuv[i+2] exists
                    if cuv[i+2] in voc: # VVV (ex: ploua, pleoape)
                        if (i+3)<=len(cuv)-1: # cuv[i+3] exists
                            if cuv[i+3] in voc: # VVVV
                                cuv=cuv[:i+2] + '-' + cuv[i+2:] # VV-VV
                                i=i+5
                            else: # VVVC
                                cuv,i=vvv(cuv,i)
                        else: #suntem la sf si  VVV
                            cuv,i=vvv(cuv,i)
                    else: # VVC
                        if cuv[i:i+2] in dif: # diphthong
                            i = i + 2 # skip
                        elif cuv[i:i+2] in hiat: # hiatus
                            cuv = cuv[:i+1] + '-' + cuv[i+1:] # V-V
                            # print cuv
                            i = i + 3 
                        else: # ambiguous VV
                            i = i + 2 
                else: # at the end
                    i = i + 2
            else: # VC
                i = i + 1 # skip V
        else: # cuv[i] is a consonant (C)
            if nucleu == 0: # no nucleus yet
                i = i + 1 # onset=> skip
            else: # already found nucleus
                if cuv[i+1] in cons: # CC
                    if (i+2) < (len(cuv)-1): # cuv[i+2] exists & not at the end
                        if cuv[i+2] in cons: # CCC
                            if (i+3) < (len(cuv)-1):
                                if cuv[i+3] in cons: # CCCC
                                    if (i+4) < (len(cuv)-1):
                                        if cuv[i+4] in cons: # CCCCC (ex: optsprezece)
                                            cuv = cuv[:i+2] + '-' + cuv[i+2:]
                                            i = i + 6
                                        else: # CCCCV
                                            cuv, i = ccccv(cuv, i)
                                    else: # at the end
                                        if cuv[i+4] in cons: # CCCCC at the end
                                            i = i + 5
                                        else:# CCCCV
                                            cuv, i = ccccv(cuv, i)
                                else: # CCCV            
                                    cuv, i = cccv(cuv, i)
                            else: # at the end
                                if cuv[i+3] in cons: # CCCC at the end
                                    i = i + 4
                                else: # CCCV at the end
                                    cuv, i = cccv(cuv, i)    
                        else: # CCV
                            cuv, i = ccv(cuv, i) # CCV
                    elif (i+2)==(len(cuv)-1): # at the end
                        if cuv[i+2] in voc: # CCV at the end (problem with CCi)
                            cuv, i = ccv(cuv, i) # CCV      
                        else: #  CCC at the end (ex: 'stm' in 'astm')
                            i = i + 3
                    else:# CC at the end
                        break
                else: # CV
                    cuv=cuv[:i] + '-' + cuv[i:] # MOP => split -CV
                    # print cuv
                    i = i + 2
    print cuv               
                

        
syllabify("lingvistica")
#probleme (infara de ambiguitatile de diftong):
#copci vs. craci vs. citi (toate iau i drept vocala), orice vs. varice
#se rezolva folosind eticheta de functie sintactica 
#i.e. verbele au i vocalic mai putin la -esti, iar restul au i semivocalic
#u-ul
#lingvistica (regula e proasta)
#accent