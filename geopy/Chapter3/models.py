

class Geocache(object):
    """This class represents a single geocaching point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def coordinates(self):
        return self.x, self.y


class PointCollection(object):
    def __init__(self):
        """This class represents a group of vector data."""
        Self.data = []


if __name__ == '__main__':
    one_geocaching_point = Geocache(20, 40)
    print(one_geocaching_point.coordinates)
