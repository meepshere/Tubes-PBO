class userGen:
    def __init__(self, objek, idUser, sandi):
        self.__objek = objek
        self.__idUser = idUser
        self.__sandi = sandi

    def getObjek(self):
        return self.__objek
    
    def getID(self):
        return self.__idUser

    def getSandi(self):
        return self.__sandi

    def __repr__(self):
        return f"ID USER : {self.getID()}"

class userNow(userGen):
    def __init__(self, objek, idUser, sandi, nama):
        super(userNow, self).__init__(objek, idUser, sandi)
        self.__nama = nama
        self.__activity = 0

    def __iadd__(self, other):
        self.__activity = self.__activity + other
        return self.__activity
        
    def getObjek(self):
        return super().getObjek()
    
    def getID(self):
        return super().getID()
    
    def getNama(self):
        return self.__nama
    
    def getSandi(self):
        return super().getSandi()
    
    def getAct(self):
        return self.__activity

    def setAct(self, new):
        self.__activity = new

    def __repr__(self):
        return f"Activity : {self.getAct()}"
