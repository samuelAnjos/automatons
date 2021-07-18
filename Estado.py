class Estado:

    def __init__(self, posX, posY, isFinal, isInitial, id, nome):
        self._posX = posX
        self._posY = posY
        self._isFinal = isFinal
        self._isInitial = isInitial
        self._id = id
        self._nome = nome


    @property
    def nome(self):
        return self._nome

    def __eq__(self, other):
        print('A __eq__ called')
        return self._id == other.id
