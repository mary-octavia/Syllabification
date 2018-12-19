Syllabification
===============

These are two non-optimized, quick and dirty, algorithms for syllabifying 
Romanian words written orthographically (and not in IPA). They were written 
in order to have a baseline accuracy for the machine learning experiments 
described in [Liviu P. Dinu, Vlad Niculae, Octavia-Maria Sulea. Romanian 
Syllabication Using Machine Learning. TSD 2013: 450-456](https://www.academia.edu/29136876/Romanian_Syllabication_using_Machine_Learning_preprint_) and implemented [here](https://github.com/nlp-unibuc/ro-hyphen)

ortho_syllabify.py 
- follows the end-of-the-line hyphenation rules listed in [DOOM](https://www.universenciclopedic.ro/dictionarul-ortografic-ortoepic-si-morfologic-al-limbii-romane)
- can be quickly tested here: http://www.codeskulptor.org/#user5-Sx4RXVO6ROjUMze-7.py

syllabify.py 
- follows [MOP](http://www.glottopedia.org/index.php/Maximal_Onset_Principle) and Ioana Chitoran's [constraint based approach to Romanian Phonology](https://www.degruyter.com/view/product/174489)
- can be quickly tested here: http://www.codeskulptor.org/#user5-AN4aaEbwtq49Ar4-18.py
