import numpy as np

def worker_grove(id, secret, q_request, q_reply):

    log=False
    dodgeDistance=100
    V_MIN =  10.0
    V_MAX =  42.0
    A_MAX = 100.0


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

    #gibt verschiedene Attribute von Puck "n" zurück
    def getSpeedPositionAndAccelerationOfAPuck(n):
        q_request.put(('GET_PUCK', n, id))
        x=q_reply.get()[1]
        if log:
            print(x)
        return x

    #weißt dem eigenen Puck eine Beschleunigung zu
    def setAcceleration(b):
        q_request.put(('SET_ACCELERATION', b, secret, id))
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

    #gibt die Position eines bestimmten Pucks n zurück
    def getPositionOfAPuck(n):
        q_request.put(('GET_PUCK', n, id))
        x=q_reply.get()[1]
        position = x.get_position()
        if log:
            print("Position of Puck", n, position)
        return position

    #gibt die Position meines Pucks zurück
    def getVelocityOfMyPuck():
        q_request.put(('GET_PUCK', id, id))
        x=q_reply.get()[1]
        velocity = x.get_velocity()
        if log:
            print("Velocity of My Puck", velocity)
        return velocity
    
    #gibt die Geschwindigkeit des Pucks "n" zurück
    def getVelocityOfAPuck(n):
        q_request.put(('GET_PUCK', n, id))
        x=q_reply.get()[1]
        velocity = x.get_velocity()
        if log:
            print("Velocity of Puck", n, velocity)
        return velocity

    #gibt den Puck mit dem geringsten Abstand und seinen Abstand zurück
    def getDistanceToNearestPuck(n):
        minDistance=1000
        for i in range (0, n-1):
            if i!=id:
                x=getSpeedPositionAndAccelerationOfAPuck(i)
                if x is not None:
                    distance = np.linalg.norm(getPositionOfMyPuck()-getPositionOfAPuck(i))
                    if distance<minDistance:
                        minDistance=distance
                        idOtherPuck=i
        if log:
            print("my id:", id, "Distance to nearest Puck", idOtherPuck, minDistance)
        return idOtherPuck, minDistance

    def getVelocityOfNearestPuck():
        x=getDistanceToNearestPuck(NumberOfPucks)
        y=x[0]
        velocity=getVelocityOfAPuck(y)
        if log:
            print("Velocity of nearest Puck", y, velocity)
        return velocity
        
    def dodgeOtherPuck():
        puckAndDistance=getDistanceToNearestPuck(NumberOfPucks)
        distance=puckAndDistance[1]
        puck=puckAndDistance[0]
        if distance<dodgeDistance:
            escape_vector = -getVelocityOfAPuck(puck)
            escape_vector = escape_vector/np.linalg.norm(escape_vector) * (A_MAX/4)
            setAcceleration(escape_vector)

    def speedControl():     
        velocity=np.linalg.norm(getVelocityOfMyPuck())
        if velocity>V_MAX*0.9:
            deceleration = -(getVelocityOfMyPuck()/np.linalg.norm(getVelocityOfMyPuck()))*A_MAX*0.2
            setAcceleration(deceleration)
        elif velocity<V_MIN*1.1:
            acceleration = (getVelocityOfMyPuck()/np.linalg.norm(getVelocityOfMyPuck()))*A_MAX*0.2
            setAcceleration(acceleration)
    
    NumberOfPucks=getNumberOfPucks()
    setName()
    box=getBox()
    while True:
        dodgeOtherPuck()
        speedControl()