import numpy as np


def worker_grove(id, secret, q_request, q_reply):

    log=False

    #fragt nach den Grenzen der Box und gibt sie zurück
    def getBox():
        q_request.put(('GET_BOX', id))
        box=q_reply.get()[1]
        if log:
            print("Size of the Box: ", box)
        return box

    #gibt dem eigenen Puck einen Namen
    def setName():
        name="Adrian"
        q_request.put(('SET_NAME', name, secret, id))
        x=q_reply.get()[1]
        if log:
            print("Puckname: ", x)
        return x

    #gibt die verbliebene Anzahl der Pucks auf dem dem Spielfeld zurück
    def getNumberOfPucks():
        q_request.put(('GET_SIZE', id))
        n=q_reply.get()[1]
        if log:
            print("Number of Pucks: ", n)
        return n

    #gibt verschiedene Attribute aller verbliebenen Pucks zurück
    def getSpeedPositionAndAccelerationOfAllPucks(n):
        for i in range (0, n-1):
            q_request.put(('GET_PUCK', i, id))
            x=q_reply.get()[1]
            if log:
                print(x)
        return x

    def getSpeedPositionAndAccelerationOfAPuck(n):
        q_request.put(('GET_PUCK', n, id))
        x=q_reply.get()[1]
        if log:
            print(x)
        return x

    #weißt dem eigenen Puck eine Beschleunigung zu
    def setAcceleration(b):
        q_request.put(('SET_ACCELERATION', name, secret, id))
        x=q_reply.get()[1]
        if log:
            print("Beschleunigung: ", x)
        return x

    #gibt die Position des eigenen Pucks zurück
    def getPositionOfMyPuck():
        q_request.put(('GET_PUCK', id, id))
        x=q_reply.get()[1]
        position = x.get_position()
        if log:
            print("Position of my Puck:", position)
        return position

    #gibt die Position aller Pucks zurück
    def getPositionOfAllPucks(n):
        for i in range (0, n-1):
            q_request.put(('GET_PUCK', i, id))
            x=q_reply.get()[1]
            position = x.get_position()
            if log:
                print("Position of Puck", i, position)
        return position

    #gibt die Position eines bestimmten Pucks zurück
    def getPositionOfAPuck(n):
        q_request.put(('GET_PUCK', n, id))
        x=q_reply.get()[1]
        position = x.get_position()
        if log:
            print("Position of Puck", n, position)
        return position

    def getDistanceBetweenTwoPucks():
        pass


    #gibt den Puck mit dem geringsten Abstand und den Abstand zurück
    def getDistanceToNearestPuck(n):
        minDistance=1000
        for i in range (0, n-1):
            if i!=id:
                x=getSpeedPositionAndAccelerationOfAPuck(i)
                if x is not None:
                    distance = np.linalg.norm(getPositionOfMyPuck()-getPositionOfAPuck(i))
                    if distance<minDistance:
                        minDistance=distance
                        y=i
        if True:
            print("my id:", id, "Distance to nearest Puck", y, minDistance)
        return y, minDistance
        
        
    
    
    NumberOfPucks=getNumberOfPucks()
    setName()
    getBox()
    getSpeedPositionAndAccelerationOfAllPucks(getNumberOfPucks())
    getPositionOfMyPuck()
    getPositionOfAllPucks(getNumberOfPucks())
    getDistanceToNearestPuck(NumberOfPucks)