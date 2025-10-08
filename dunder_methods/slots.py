class Point:
    # It does not need __dict__ -> it is more memory-efficient and a little bit faster
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        (self.x, self.y, self.z) = (x, y, z)


def point_path_from_file(filename):
    with open(filename) as lines:
        return [
            Point(*map(float, point_line.split()))
            for point_line in lines
        ]


if __name__ == '__main__':
    point = Point(1, 2, 3)
    point.a = 1
