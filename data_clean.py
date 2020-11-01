import sys
import os
import numpy as np

def main():
	#user_id, item_id, score
	data_file = sys.argv[1]
	clean_data_file = sys.argv[2]
	fp_read = open(data_file,"r")
	fp_write = open(clean_data_file,"w+")
	for line in fp_read:
		line = line.strip("\n")
		line = line.split(",")
		userId = line[2]
		productId = line[1]
		score = line[-4]
		summary = line[-2]
		text = line[-1]
		write_str = productId +"," + userId + "," + summary + "," + text + "," + score +"\n"
		fp_write.write(write_str)
	fp_write.close()
	fp_read.close()


if __name__== "__main__":
	main()