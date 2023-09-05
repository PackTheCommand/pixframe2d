class SpriteMarerialService:
    def __init__(self):
        pass
    def parseCreate(self,Material,range_x,range_y):

        def generate_result(texture_grid,Material,):
            result = []
            rows = len(texture_grid)
            cols = len(texture_grid[0])

            for i in range(rows):
                row = []
                for j in range(cols):

                    if texture_grid[i][j] == 0:
                        row.append("null")
                        continue

                    def get(x, y):

                        if len(texture_grid) > x > -1:
                            t = texture_grid[x]
                            if len(t) > y > -1:
                                return t[y]
                        return 0

                    nabour_e = get(i, j + 1)
                    nabour_w = get(i, j - 1)
                    nabour_n = get(i - 1, j)
                    nabour_s = get(i + 1, j)

                    if nabour_n == 0 and nabour_s == 0 and nabour_e == 0 and nabour_w == 0:
                        row.append((Material.getUNIQUE(),"all"))
                    elif nabour_n == 0 and nabour_e == 1 and nabour_w == 1 and nabour_s == 1:
                        row.append((Material.getUNIQUE(),"n"))
                    elif nabour_s == 0 and nabour_e == 1 and nabour_w == 1 and nabour_n == 1:
                        row.append((Material.getUNIQUE(),"s"))
                    elif nabour_e == 0 and nabour_w == 1 and nabour_n == 1 and nabour_s == 1:
                        row.append((Material.getUNIQUE(),"e"))
                    elif nabour_w == 0 and nabour_n == 1 and nabour_s == 1 and nabour_e == 1:
                        row.append((Material.getUNIQUE(),"w"))
                    elif nabour_n == 0 and nabour_e == 1 and nabour_w == 0 and nabour_s == 1:
                        row.append((Material.getUNIQUE(),"nw"))
                    elif nabour_s == 0 and nabour_e == 1 and nabour_w == 0 and nabour_n == 1:
                        row.append((Material.getUNIQUE(),"sw"))
                    elif nabour_s == 1 and nabour_e == 0 and nabour_w == 1 and nabour_n == 0:
                        row.append((Material.getUNIQUE(),"ne"))
                    elif nabour_s == 0 and nabour_e == 0 and nabour_w == 1 and nabour_n == 1:
                        row.append((Material.getUNIQUE(),"se"))



                    elif nabour_n == 1 and nabour_n == 1 and nabour_s == 1 and nabour_s == 1:
                        row.append("center")

                    else:
                        print("error", i, j, nabour_n, nabour_s, nabour_e, nabour_w)

                        row.append("?")

                result.append(row)
            return result




        pass