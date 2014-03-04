# -*- coding:utf-8 -*-
__author__ = 'henri'


def newMap(x, y, tilesetfile="road-tiles.xml"):
    import xml.etree.ElementTree as ET
    from random import choice

    columns = y
    rows = x
    idList = []

    try:
        tileXml = ET.parse(tilesetfile).getroot()
    except IOError:
        print "Couldn't open file"
        quit()
    except:
        print "Error occurred"
        quit()



    for child in tileXml:
        if child.tag == "tileset":
            for tile in child.findall('tile'):
                idList.append(tile.get('id'))



    rE = ET.Element('resource')
    rqE = ET.SubElement(rE, 'requires', {'file': tilesetfile})
    reE = ET.SubElement(rE, 'rectmap', {'id': "map0", 'origin': "0,0,0", 'tile_size': "128x128"})
    for x in range(rows):
        column = ET.SubElement(reE, 'column')
        for y in range(columns):
            randId = choice(idList)
            ET.SubElement(column, 'cell', {'tile': randId})

    xmlContent = ET.tostring(rE)
    xmlFile = open('tilemap.xml','w+')
    xmlFile.write(xmlContent)
    xmlFile.close()

if __name__ == '__main__':
    x = input("Rows?: ")
    y = input("Columns? ")
    newMap(x,y)