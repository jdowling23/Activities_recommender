from Activities import Activites 
#class for resturaunt
class Restaurant(Activities):
    def __init__(self, outdoors, child_friendly, cost, is_open, distance, type, rating, menu):
        #inherit from Activites class        
        super().__init__(outdoors, child_friendly, cost, is_open, distance)
        self.type = type
        self.rating = rating
        self.menu = menu

    

    