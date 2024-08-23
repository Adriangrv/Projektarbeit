def worker_grove(id, secret, q_request, q_reply):

    log=True
    
    def getBox():
        q_request.put(('GET_BOX', id))
        box=q_reply.get()[1]
        if log:
            print("Size of the Box: ", box)
        return box

    def setName():
        name="Adrian"
        q_request.put(('SET_NAME', name, secret, id))
        x=q_reply.get()[1]
        if log:
            print("Puckname: ", x)
        return x

    def getNumberOfPucks():
        q_request.put(('GET_SIZE', id))
        n=q_reply.get()[1]
        if log:
            print("Number of Pucks: ", n)
        return n

    def getSpeedPositionAndAccelerationOfAllPucks(n):
        for i in range (0, n-1):
            q_request.put(('GET_PUCK', i, id))
            x=q_reply.get()[1]
            if log:
                print(x)
        return x


    setName()
    getBox()
    getNumberOfPucks()
    getSpeedPositionAndAccelerationOfAllPucks(getNumberOfPucks())