import os
dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir, "input.txt")

with open(file_path, 'r') as reader:
    grid = [line.rstrip('\n') for line in reader]

MAX_X = len(grid[0])
MAX_Y = len(grid)

def get_atenna_coords(grid: list[str]) -> dict[str, set[tuple[int, int]]]:
    coords: dict[str, set[tuple[int, int]]] = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            if cell != '.':
                if cell not in coords:
                    coords[cell] = set()
                coords[cell].add((row, col))
    return coords


def get_mirror_coords(first_coord: tuple[int, int], second_coord: tuple[int, int]) -> tuple[int, int]:
    c1x, c1y = first_coord
    c2x, c2y = second_coord
    return (c1x - (c2x - c1x), c1y - (c2y - c1y))

def is_in_bounds(coord: tuple[int, int]) -> bool:
    x, y = coord
    return 0 <= x < MAX_X and 0 <= y < MAX_Y

locations = set()
locations_p2 = set()

for coords in get_atenna_coords(grid).values():
    for i, first_coord in enumerate(list(coords)):
        for second_coord in list(coords)[i+1:]:
            for mirror_coord in [get_mirror_coords(first_coord, second_coord), get_mirror_coords(second_coord, first_coord)]:
                if is_in_bounds(mirror_coord):
                    locations.add(mirror_coord)

            # part 2
            mirror_coord_1 = get_mirror_coords(first_coord, second_coord)
            mirror_coord_2 = get_mirror_coords(second_coord, first_coord)

            #if we're looking for all points along a line then these 2 are always on that line too            
            locations_p2.add(first_coord)
            locations_p2.add(second_coord)

            #mirroring forwards and backwards
            mirroring_point_1 = first_coord
            mirroring_point_2 = second_coord

            while is_in_bounds(mirror_coord_1):
                locations_p2.add(mirror_coord_1)
                temp = mirror_coord_1
                mirror_coord_1 = get_mirror_coords(mirror_coord_1, mirroring_point_1)
                mirroring_point_1 = temp
            
            while is_in_bounds(mirror_coord_2):
                locations_p2.add(mirror_coord_2)
                temp = mirror_coord_2
                mirror_coord_2 = get_mirror_coords(mirror_coord_2, mirroring_point_2)
                mirroring_point_2 = temp


print(len(locations)) #part 1 answer
print(len(locations_p2)) #part 2 answer