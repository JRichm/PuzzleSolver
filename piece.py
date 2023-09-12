class Piece:
    def __init__(self):
        self.peice_id = None

    def __repr__(self):
        print("\tPuzzle Peice")
        print("Peice ID: ", self.peice_id)
        print("")
        return
    
    def find_connectors(self):
        pass

    def try_connection(self):
        pass



class Connection: 
    def __init__(self):
        self.connector_type