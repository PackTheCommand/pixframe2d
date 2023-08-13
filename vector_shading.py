def collision_detection(vector, obstacle, start_vector):
    x1, y1 = vector
    x2, y2 = obstacle[0]
    x3, y3 = obstacle[1]
    x4, y4 = obstacle[2]
    x5, y5 = obstacle[3]
    x6, y6 = start_vector

    # check if the line intersects with any of the edges of the rectangle
    if (y3 - y2) * (x1 - x2) > (y1 - y2) * (x3 - x2) and (y5 - y4) * (x1 - x4) > (y1 - y4) * (x5 - x4):
        return None

    # calculate the intersection point
    if x2 == x3:
        m = (y5 - y4) / (x5 - x4)
        b = y4 - m * x4
        x = x2
        y = m * x + b
    elif x4 == x5:
        m = (y3 - y2) / (x3 - x2)
        b = y2 - m * x2
        x = x4
        y = m * x + b
    else:
        m1 = (y3 - y2) / (x3 - x2)
        b1 = y2 - m1 * x2

        m2 = (y5 - y4) / (x5 - x4)
        b2 = y4 - m2 * x4

        if m1 == m2:
            return None

        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

    # check if the intersection point is inside the rectangle
    if min(x3, x5) <= x <= max(x3, x5) and min(y3, y5) <= y <= max(y3, y5):
        return round(x), round(y)

    return None


from shapely.geometry import Point, Polygon

def is_point_in_rectangle(point, c1, c2, c3, c4):
    rectangle = Polygon([c1, c2, c3, c4])
    point = Point(point)
    return rectangle.contains(point)

# Example usage
c1 = (100, 100)
c2 = (200, 100)
c3 = (200, 200)
c4 = (100, 200)
point = (150, 150)

print(is_point_in_rectangle(point, c1, c2, c3, c4))  # Should print True


def shoot_ray(sV,rV,points=20):
    sVa,sVb=sV
    rVa,rVb=rV
    l=[]

    for i in range(0,points):
        l+=[(sVa+rVa*i,sVb+rVb*i)]

    return l
