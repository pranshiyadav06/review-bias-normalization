import sqlite3
import csv
import pandas as pd
import numpy as np
import nltk
import string
import matplotlib.pyplot as plt
import numpy as np
import sys

def freq(user_list, item_list):
    ni = user_list[0]
    nu = item_list[0]

    if ni>=12 and nu>=12:
        return 1
    else:
        return 0


def main():
    #user_id, item_id, summary, text, score
    data_file = sys.argv[1]
    correct = sys.argv[2]
    incorrect = sys.argv[3]
    fp_read = open(data_file,"r")
    fp_write1 = open(correct,"w+")
    fp_write2 = open(incorrect,"w+")

    user_dict = np.load("user_dict.npy",allow_pickle=True).item()
    item_dict = np.load("item_dict.npy",allow_pickle=True).item()

    i = 0
    fp_write1.write("ProductId,UserId,Summary,Text,Score\n")
    fp_write2.write("ProductId,UserId,Summary,Text,Score\n")
    for line in fp_read:
        if i == 0:
            i += 1
            continue
        line = line.strip("\n")
        line = line.split(",")
        # text_data = line[2] + " " + line[3]
        summary = line[2]
        text = line[3]
        user_id = line[1]
        item_id = line[0]
        orig_score = float(line[4])
        frequency = freq(user_dict[user_id],item_dict[item_id])
        if frequency == 1:
            write_str1 = item_id  +"," + user_id + "," + summary + "," + text + "," + str(orig_score) +"\n"
            fp_write1.write(write_str1)
        elif frequency == 0:
            write_str2 = item_id  +"," + user_id + "," + summary + "," + text + "," + str(orig_score) +"\n"
            fp_write2.write(write_str2)
        
    fp_write1.close()
    fp_write2.close()
    fp_read.close()


if __name__== "__main__":
    main()