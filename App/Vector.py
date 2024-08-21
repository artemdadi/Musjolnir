## partly taken from  https://gist.github.com/mcleonard/5351452

class Vec:

    names = []

    def __init__(self, *values):
        self.values = list(values)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.values[self.names.index(key)]
        else:
            return self.values[key]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.values[self.names.index(key)] = value
        else:
            self.values[key] = value

    def vec_scale(self, vec):
        product = tuple( a * b for a, b in zip(self, vec) )
        return self.__class__(*product)

    def inner(self, vector):
        if not isinstance(vector, Vec):
            raise ValueError('The dot product requires another vector')
        return sum(a * b for a, b in zip(self, vector))
    
    def __mul__(self, other):
        if isinstance(other, Vec):
            return self.inner(other)
        elif isinstance(other, (int, float)):
            product = tuple( a * other for a in self )
            return self.__class__(*product)
        else:
            raise ValueError("Multiplication with type {} not supported".format(type(other)))
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, Vec):
            added = tuple( a + b for a, b in zip(self, other) )
        elif isinstance(other, (int, float)):
            added = tuple( a + other for a in self )
        else:
            raise ValueError("Addition with type {} not supported".format(type(other)))
        return self.__class__(*added)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vec):
            subbed = tuple( a - b for a, b in zip(self, other) )
        elif isinstance(other, (int, float)):
            subbed = tuple( a - other for a in self )
        else:
            raise ValueError("Subtraction with type {} not supported".format(type(other)))
        return self.__class__(*subbed)
    
    def __rsub__(self, other):
        return self.__sub__(other)

    def __str__(self):
        return self.__class__.__name__ + str(self.values)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.values.__iter__()

if __name__ == "__main__":
    x, y = Vec(1,2).values
    print(x)
