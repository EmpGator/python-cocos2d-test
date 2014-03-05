# -*- coding:utf-8 -*-
__author__ = 'henri'

from random import choice, randint
import AStar

def newRoom(minX,maxX,minY,maxY):
    roomWidth = randint(minX, maxX)+2
    roomHeight = randint(minY, maxY)+2
    return [roomWidth, roomHeight]

def dungeonGenerator():
    width = 60
    height = 60
    roomsMin = 22
    roomsMax = 24
    minRoomWidth = 2
    maxRoomWidth = 6
    minRoomHeight = 2
    maxRoomHeight = 6
    generatedRooms = 0
    dungeon = []
    rooms = []

    roomAmount = randint(roomsMin, roomsMax)

    #Adds rooms to rooms list
    for x in range(roomAmount):
        rooms.append(newRoom(minRoomWidth, maxRoomWidth, minRoomHeight, maxRoomHeight))


    #Makes map with walls
    for y in range(height):
        container = []
        for x in range(width):
            if x > 2 and x < width-3 and y > 2 and y < height-3:
                container.append(".")
            else:
                container.append("#")
        dungeon.append(container)

    #Check wheter room should be created
    for rowId in range(len(dungeon)):
        for charId in range(len(dungeon[rowId])):
            if dungeon[rowId][charId] != '#':
                startGeneratingRoomHere = randint(1, 10)
                if startGeneratingRoomHere == 1:
                    generatedRooms += CreateRoom(dungeon, charId, rowId, rooms) #Tries to make room

    #Prints map
    for rowId in range(len(dungeon)):
        for charId in range(len(dungeon[rowId])):
            if dungeon[rowId][charId] == 'D':
                createPaths(rowId, charId, dungeon)

    for row in dungeon:
        container = ''
        for char in row:
            container += char
        print container

    print "Generated rooms", str(generatedRooms)
    return dungeon


def CreateRoom(dungeon, x, y, rooms):
    """

    :rtype : int
    """
    if rooms != []:
        room = rooms[0]
    else:
        return 0

    maxX = x+room[0]
    maxY = y+room[1]
    door = 0

    #Make sure room isn't generated over wall
    if maxX > len(dungeon[0])-3 or maxY > len(dungeon)-3:
        rooms.append(rooms[0])
        rooms.pop(0)
        return 0

    #Check if there are any rooms too close
    for yId in range(y-1, maxY+1):
        for xId in range(x-1, maxX+1):
            if 'R' == dungeon[yId][xId] or 'F' == dungeon[yId][xId]:
                rooms.append(rooms[0])
                rooms.pop(0)
                return 0

    #Create rooms for dungeon
    for yId in range(y, maxY):
        for xId in range(x, maxX):
            dungeon[yId][xId] = 'R'
            if xId > x and xId < maxX-1 and yId > y and yId < maxY-1:
                dungeon[yId][xId] = 'F'
            else: #Create walls and door
                if (xId != x and xId != maxX-1) or (yId != y and yId != maxY-1):
                    if dungeon[yId-1][xId] != '#' and dungeon[yId+1][xId] != '#':
                        if dungeon[yId][xId+1] != '#' and dungeon[yId][xId-1] != '#':
                            createDoor = randint(1, 6)
                            if yId == maxY-1 and xId == maxX-2:
                                createDoor = 1
                            if createDoor == 1 and door == 0:
                                dungeon[yId][xId] = 'D'
                                door = 1
                            else:
                                dungeon[yId][xId] = 'R'
                else:
                    dungeon[yId][xId] = 'R'

    rooms.pop(0)
    return 1


def createPaths(y, x, dungeon):
    """
    Create paths
    from door to door or
    from path to door or
    from door to path or
    from door to dead end or
    from path to dead end
    """
    mapDataForAstar = []
    doors = []

    #dungeon[y][x] = 'S'
    for rowId in range(len(dungeon)):
        for charId in range(len(dungeon[rowId])):
            if dungeon[rowId][charId] in "#RF":
                mapDataForAstar.append(-1)
            elif dungeon[rowId][charId] == "D":
                if x != charId and y != rowId:
                    doors.append([rowId, charId])
                mapDataForAstar.append(1)
            else:
                mapDataForAstar.append(1)

    astar = AStar.AStar(AStar.SQ_MapHandler(mapDataForAstar, len(dungeon[0]), len(dungeon)))
    start = AStar.SQ_Location(x, y)
    end = AStar.SQ_Location(doors[0][0], doors[0][1])

    p = astar.findPath(start, end)

    if not p:
        print "No path found!"
        pathlines = []
    else:
        print "Found path in",str(len(p.nodes)),"moves."
        pathlines = []
        #pathlines.append((start.x, start.y))
        for n in p.nodes:
            pathlines.append((n.location.x, n.location.y))
        pathlines.append((end.x, end.y))

    for point in pathlines:
        dungeon[point[1]][point[0]] = "P"

def newMap(tilesetfile="road-tiles.xml"):
    import xml.etree.ElementTree as ET

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

    #print idList
    dungeon = dungeonGenerator()

    idList = {
        '#': 'blackwall',
        '.': 'concrete_wall',
        'R': 'orange_wall',
        'F': 'lighthumanskin',
        'P': 'greenish-yellow',
        'D': 'humanskin'
    }

    rows = len(dungeon)
    columns = len(dungeon[0])

    for x in range(rows):
        column = ET.SubElement(reE, 'column')
        for y in range(columns):
            key = dungeon[y][x]
            tileId = idList[key]
            #randId = choice(idList)
            ET.SubElement(column, 'cell', {'tile': tileId})

    xmlContent = ET.tostring(rE)
    xmlFile = open('tilemap.xml','w+')
    xmlFile.write(xmlContent)
    xmlFile.close()

if __name__ == '__main__':
    #x = input("Rows?: ")
    #y = input("Columns? ")
    newMap(3, 3)
    #dungeonGenerator()