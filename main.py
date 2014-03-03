# -*- coding: utf-8 -*-

__author__ = 'henri'

nimi = raw_input("Mikä on nimesi?\n")

print "Hei,",nimi
mietin = raw_input("Mitäpä mietit?\n")
if nimi == "henri" or nimi == "Henri" or mietin == "Liamia":
    print "Olet paras!"
elif nimi == "Reijo":
    print "Jäkä jäkä jäkä"
else:
    print "Mee pois!"