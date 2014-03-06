# -*- coding:utf-8 -*-
__author__ = 'henri'

from random import choice, randint
import AStar

idList = {
            '#': 'blackwall',
            '.': 'concrete_wall',
            'R': 'orange_wall',
            'F': 'lighthumanskin',
            'P': 'greenish-yellow',
            'D': 'humanskin',
            'S': 'spawn',
            'E': 'exit',
        }

def newRoom(minX,maxX,minY,maxY):
    """
    Creates new room
    """
    roomWidth = randint(minX, maxX)+2
    roomHeight = randint(minY, maxY)+2
    return [roomWidth, roomHeight]

def dungeonGenerator(width=34, height=30, roomsMin = 6, roomsMax = 16, minRoomWidth = 2, maxRoomWidth = 8, minRoomHeight = 2, maxRoomHeight = 8, roomDensity = 20):
    """
    Creates new dungeon as a nested list

    Id list
        '#': 'blackwall',
        '.': 'concrete_wall',
        'R': 'orange_wall',
        'F': 'lighthumanskin',
        'P': 'greenish-yellow',
        'D': 'humanskin',
        'S': 'spawn',
        'E': 'exit',

    :rtype : list
    """
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
                container.append(".")  # Weaker Dungeon wall
            else:
                container.append("#")  # Dungeon wall
        dungeon.append(container)

    #Check whether room should be created
    for rowId in range(len(dungeon)):
        for charId in range(len(dungeon[rowId])):
            if dungeon[rowId][charId] != '#':
                startGeneratingRoomHere = randint(1, roomDensity)
                if startGeneratingRoomHere == 1:
                    generatedRooms += CreateRoom(dungeon, charId, rowId, rooms) #Tries to make room


    createSpawnPoint = True
    exitCoordinates = []
    pathCounter = 0

    #Creates paths from doors
    #Creates spawn point
    for rowId in range(len(dungeon)):
        for charId in range(len(dungeon[rowId])):
            if dungeon[rowId][charId] == 'F':
                if createSpawnPoint:
                    dungeon[rowId][charId] = 'S'
                    createSpawnPoint = False
                else:
                    exitCoordinates.append([charId, rowId])
            if dungeon[rowId][charId] == 'D':
                pathCounter += createPaths(rowId, charId, dungeon)

    exitMap = choice(exitCoordinates)
    dungeon[exitMap[1]][exitMap[0]] = 'E'

    #Prints map
    for row in dungeon:
        container = ''
        for char in row:
            container += char
        print container

    print "Generated rooms", str(generatedRooms)
    print "Generated paths", str(pathCounter)
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
            #TODO Simplify below
            if xId > x and xId < maxX-1 and yId > y and yId < maxY-1:
                dungeon[yId][xId] = 'F'
            else:  # Create walls and door
                # Check that there are not any walls too close
                if (xId != x and xId != maxX-1) or (yId != y and yId != maxY-1):
                    if dungeon[yId-1][xId] != '#' and dungeon[yId+1][xId] != '#':
                        if dungeon[yId][xId+1] != '#' and dungeon[yId][xId-1] != '#':
                            createDoor = randint(1, 6)
                            if yId == maxY-1 and xId == maxX-2:
                                createDoor = 1
                            if createDoor == 1 and door == 0:
                                dungeon[yId][xId] = 'D'  # Door
                                door = 1
                            else:
                                dungeon[yId][xId] = 'R'  # Room wall
                else:
                    dungeon[yId][xId] = 'R'

    rooms.pop(0)
    return 1


def createPaths(y, x, dungeon):
    """
    Create paths
    DONE from door to door or
    TODO from path to door or
    from door to path or
    from door to dead end or
    from path to dead end
    """
    #TODO from path to door
    #TODO from door to path
    #TODO from door to dead end
    #TODO from path to dead end
    #TODO make sure every room is accessible

    mapDataForAstar = []
    doors = []

    for rowId in range(len(dungeon)):
        for charId in range(len(dungeon[rowId])):
            if dungeon[rowId][charId] in "#RFS":  # Check that given spot is free for building
                mapDataForAstar.append(-1)
            elif dungeon[rowId][charId] == "D":  # Check if given spot is door
                if x != charId and y != rowId:
                    doors.append([charId, rowId])  # Add door to door list
                mapDataForAstar.append(1)
            else:
                mapDataForAstar.append(1)

    # ---- Begin path finding -----
    astar = AStar.AStar(AStar.SQ_MapHandler(mapDataForAstar, len(dungeon[0]), len(dungeon)))  # Init A*
    start = AStar.SQ_Location(x, y)  # Give start point
    door = choice(doors)  # Pick door as endpoint
    end = AStar.SQ_Location(door[0], door[1])  # Make the endpoint
    p = astar.findPath(start, end)  # Find the path

    if not p:
        print "No path found!"
        return 0

    else:
        pathlines = []

        for n in p.nodes:
            pathlines.append((n.location.x, n.location.y))  # Add path points to list variable

    for point in pathlines:
        if dungeon[point[1]][point[0]] != "D":  # Make sure that no doors are overwritten
            dungeon[point[1]][point[0]] = "P"  # Write paths to map

    return 1

def newMap(w=34, h=30, roomsMin=6, roomsMax=16, minRoomWidth=2, maxRoomWidth=8, minRoomHeight=2, maxRoomHeight=8, roomDensity=20, tilesetfile="road-tiles.xml"):
    """
    Creates actual xml map from nested list

    """
    import xml.etree.ElementTree as ET
    global idList

    dungeon = dungeonGenerator(w, h, roomsMin, roomsMax, minRoomWidth, maxRoomWidth, minRoomHeight, maxRoomHeight, roomDensity)  # Creates dungeon map as a nested list
    rows = len(dungeon)
    columns = len(dungeon[0])

    # ----- Begin xml file creation -----
    rE = ET.Element('resource')  # Begin xml creation
    rqE = ET.SubElement(rE, 'requires', {'file': tilesetfile})
    reE = ET.SubElement(rE, 'rectmap', {'id': "map0", 'origin': "0,0,0", 'tile_size': "128x128"})

    # Start going trough nested-list map
    for x in range(rows):
        column = ET.SubElement(reE, 'column')
        for y in range(columns):
            key = dungeon[x][y]  # Each sing acts as key for tile
            tileId = idList[key]  # Check which tile this sing is
            ET.SubElement(column, 'cell', {'tile': tileId})  # Add tile id line to xml document

    xmlContent = ET.tostring(rE)
    xmlFile = open('tilemap.xml', 'w+')
    xmlFile.write(xmlContent)
    xmlFile.close()

if __name__ == '__main__':
    newMap(3, 3)
