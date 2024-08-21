from .Vector import * 

class Point(Vec):
    
    names = ["x", "y"]

class Size(Vec):

    names = ["w", "h"]

class Rect(Vec):

    names = ["p", "size"]

    def add_border(self, size):
        self["p"] = self["p"] - size
        self["size"] = self["size"] + 2 * size

    def is_point_in_rect(self, point):
        if (point["x"] >= self["p"]["x"] and
            point["x"] <= (self["p"]["x"] + self["size"]["w"]) and
            point["y"] >= self["p"]["y"] and
            point["y"] <= (self["p"]["y"] + self["size"]["h"])):
            return True
        else: 
            return False

    def scale(self, rect):
        size = self["size"].vec_scale(rect["size"])
        p = rect["p"] + self["p"].vec_scale(size)
        return Rect(p, size)

if __name__ == "__main__":
    print(Point(1,2)["x"])
