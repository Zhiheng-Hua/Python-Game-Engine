class Store:
    def __init__(self):
        self.__game_objects = []    # mesh objects

    def game_objects(self):
        return self.__game_objects

    def add_game_object(self, obj):
        self.__game_objects.append(obj)
