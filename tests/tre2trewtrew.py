def generate_result(texture_grid):
    result = []
    rows = len(texture_grid)
    cols = len(texture_grid[0])

    for i in range(rows):
        row = []
        for j in range(cols):

            if texture_grid[i][j] == 0:
                row.append("null")
                continue

            def get(x,y):

                if len(texture_grid) > x>-1:
                    t = texture_grid[x]
                    if len(t)>y>-1:
                        return t[y]
                return 0

            nabour_e=get(i,j+1)
            nabour_w=get(i,j-1)
            nabour_n =get(i-1,j)
            nabour_s=get(i+1,j)



            if nabour_n==0 and nabour_s==0 and nabour_e==0 and nabour_w==0:
                row.append("all")
            elif nabour_n==0 and nabour_e==1 and nabour_w==1 and nabour_s==1:
                row.append("n")
            elif  nabour_s==0 and nabour_e==1 and nabour_w==1 and  nabour_n==1:
                row.append("s")
            elif  nabour_e==0 and nabour_w==1 and  nabour_n==1 and  nabour_s==1:
                row.append("e")
            elif   nabour_w==0 and nabour_n==1 and  nabour_s==1 and  nabour_e==1:
                row.append("w")
            elif nabour_n==0 and nabour_e==1 and nabour_w==0 and nabour_s==1:
                row.append("nw")
            elif  nabour_s==0 and nabour_e==1 and nabour_w==0 and  nabour_n==1:
                row.append("sw")
            elif  nabour_s==1 and nabour_e==0 and nabour_w==1 and  nabour_n==0:
                row.append("ne")
            elif  nabour_s==0 and nabour_e==0 and nabour_w==1 and  nabour_n==1:
                row.append("se")



            elif nabour_n==1 and nabour_n==1 and nabour_s==1 and nabour_s==1:
                row.append("center")

            else:
                print("error",i,j,nabour_n,nabour_s,nabour_e,nabour_w)

                row.append("?")

        result.append(row)
    return result


# Define the input texture grid (can be of any size)
texture_grid = [
    [1, 1, 1,0,0,0],
    [1, 1, 1,0,0,0],
    [1, 1, 1,1,0,0],
    [1, 1, 1,1,0,0],
    [1, 1, 1,0,0,0],
    [1, 1, 1,1,1,1]
]

# Generate the result grid
result = generate_result(texture_grid)

# Print the result
for row in result:
    print(row)

exit()
def getI(x,y):
    if len(texture_grid)>x:



        if len(texture_grid) > x:
            t = texture_grid[x]
            if len(t)>y:
                return bool(t[y])

    return False



def get_direction(x, y):
    if not getI(x,y):
        return "empty"
    l={


        "n":getI(x-1,y)&(not getI(x,y+1))&getI(x+1,y),
       "s":getI(x-1,y)&(not getI(x,y-1))&getI(x+1,y)&getI(x,y+1),

       "center":getI(x,y+1)&getI(x,y-1)&getI(x+1,y)&getI(x-1,y),





       }
    for key in l:
        if l[key]:
            return key
    return "base"









def generate_texture_map(texture_grid):
    directions = ["center", "n", "s", "w", "e", "nw", "ne", "sw", "se"]
    rows = len(texture_grid)
    cols = len(texture_grid[0])

    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols







# Example usage:
texture_grid = [
    [1, 1, 1,1],
    [1, 1, 1,1],
    [1, 1, 1,1]
]
result = [
    ["nw","n","n","ne"],
    ["w","center","center","e"],
    ["sw","s","s","se"
]]

for x,row in enumerate(texture_grid):
    for y,_ in enumerate(row):
        result[x][y] =get_direction(x,y)
print(result)