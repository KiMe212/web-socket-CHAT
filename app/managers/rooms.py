from app.managers.connection import connection_manager

class RoomsManager:
    def __init__(self):
        self.creator_rooms: dict[str,list] = {}
        

    def add_room(self,room, user_name):
        if room not in connection_manager.user_rooms:
            self.creator_rooms[user_name] = self.creator_rooms.setdefault(user_name, []) + [room]
            connection_manager.user_rooms[room] = []
            print(self.creator_rooms)
            print(connection_manager.user_rooms)
        else:
            raise 
    
    
    def remove_room(self, room, user_name):
        if room in connection_manager.user_rooms:
            if room in self.creator_rooms[user_name]:
                self.creator_rooms[user_name].remove(room)
                del connection_manager.user_rooms[room]
        else:
            raise

    
room_manager = RoomsManager()
