class Store:
    def __init__(self):
        self.__game_objects = []    # mesh objects
        self.__cameras = []

    def game_objects(self):
        return self.__game_objects

    def add_game_object(self, obj):
        self.__game_objects.append(obj)

    def cameras(self):
        return self.__cameras

    def add_camera(self, camera):
        self.__cameras.append(camera)