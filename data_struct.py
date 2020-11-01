import sys
import os
import numpy as np

def main():
	#user_id, item_id, score
	data_file = sys.argv[1]
	fp = open(data_file,"r")
	users_dict = {}
	items_dict = {}
	i = 0
	for line in fp:
		if i == 0:
			i += 1
			continue
		line = line.strip("\n")
		line = line.split(",")
		line[4] = float(line[4])

		if line[0] in items_dict:
			items_dict[line[0]][0] += 1
			items_dict[line[0]][1] += line[4]
		else:
			items_dict[line[0]] = [1, line[4], 0]
		if line[1] in users_dict:
			users_dict[line[1]][0] += 1
			users_dict[line[1]][1] += line[4]
		else:
			users_dict[line[1]] = [1, line[4], 0]
	fp.close()

	#mean calculation
	for key in items_dict:
		items_dict[key][1] /= items_dict[key][0]
	for key in users_dict:
		users_dict[key][1] /= users_dict[key][0]

	#tendency calculation
	fp = open(data_file,"r")
	i = 0
	for line in fp:
		if i == 0:
			i += 1
			continue
		line = line.strip("\n")
		line = line.split(",")
		line[4] = float(line[4])
		items_dict[line[0]][2] += (line[4] - users_dict[line[1]][1])/(items_dict[line[0]][0])
		users_dict[line[1]][2] += (line[4] - items_dict[line[0]][1])/(users_dict[line[1]][0])
	fp.close()

	# Save the dictionary
	np.save("item_dict.npy", items_dict)
	np.save("user_dict.npy", users_dict)


if __name__== "__main__":
  main()