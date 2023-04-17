from csv import reader
from .collisions import bt


def import_csv_layout(path):
	blocks_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		#for i in range(4):   # i tried
		#	blocks_map += [[0]*5]
		for row in level:
			temp = [int(i) for i in row]
			blocks_map.append(temp)
		#print(blocks_map,'\n')
		return list(zip(*blocks_map[::-1]))   # blocks_map


if "__main__" == __name__:   # testing
    path = "./bloc_pics/map.csv"
    for i in import_csv_layout(path):
        print(i)