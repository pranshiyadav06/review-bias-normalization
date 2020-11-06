import sqlite3
import csv
import pandas as pd
import numpy as np
import nltk
import string
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, max_error

def bias_score(transform_score, beta, user_list, item_list):
    ni = user_list[0]
    nu = item_list[0]
    ru = user_list[1]
    ri = item_list[1]
    tu = user_list[2]
    ti = item_list[2]

    # print "ru:", ru,"ri: ",ri,"tu: ",tu,"ti: ",ti,"nu: ",nu,"ni: ",ni
    if tu >= 0 and ti >= 0: #CASE1
        if (ru+ti) >= (ri+tu): #case1_part1
            biased_score = (1/(ni+nu+1)) * ((transform_score*(nu+1)*(ni+1)) - ((ni+1)*(nu*ti)) - (ni*nu*ru))
        else: #case1_part2
            biased_score = (1/(ni+nu+1)) * ((transform_score*(nu+1)*(ni+1)) - ((nu+1)*(ni*tu)) - (ni*nu*ri))

    elif tu < 0 and ti < 0: #CASE2
        if (ru+ti) <= (ri+tu): #case2_part1
            biased_score = (1/(ni+nu+1)) * ((transform_score*(nu+1)*(ni+1)) - ((ni+1)*(nu*ti)) - (ni*nu*ru))
        else: #case2_part2
            biased_score = (1/(ni+nu+1)) * ((transform_score*(nu+1)*(ni+1)) - ((nu+1)*(ni*tu)) - (ni*nu*ri))

    elif tu <= 0 and ti >= 0 and ru <= ri: #CASE3
        if ru >= ((ri+tu)*beta + (ru + ti)*(1-beta)):
            if ru <= ri: #case3_part1
                biased_score = ((ni+1)*transform_score) - (ru*ni)
            else: #case3_part3
                biased_score = ((nu+1)*transform_score) - (ri*nu)
        else:
            if ((ri+tu)*beta + (ru + ti)*(1-beta)) <= ri: #case3_part2
                biased_score = (1/(ni+nu+1)) * ((transform_score*(nu+1)*(ni+1)) - (nu*(ru*ni)*(1-beta)) - ((ni+1)*(1-beta)*(nu*ti)) - (beta*ni*ri*nu) - (beta*(nu+1)*ni*tu))
            else: #case3_part3
                biased_score = ((nu+1)*transform_score) - (ri*nu)

    elif tu <= 0 and ti >= 0 and ru > ri: #CASE4
        biased_score = (1/((nu*(1-beta))+1+(beta*ni))) * (((nu+1)*(ni+1)*transform_score) - (beta*(ni+1)*(ri*nu)) - ((1-beta)*(nu+1)*(ru*ni)))
    
    elif tu >= 0 and ti <= 0 and ru >= ri: #CASE5
        if ri >=  (ru+ti)*beta + (ri+tu)*(1-beta):
            if ri <= ru:#case5_part1
                biased_score = ((nu+1)*transform_score) - (ri*nu)
            else:#case5_part3
                biased_score = ((ni+1)*transform_score) - (ru*ni)
        else:
            if (ru+ti)*beta + (ri+tu)*(1-beta) <= ru:#case5_part2
                biased_score = (1/(ni+nu+1)) * (((nu+1)*(ni+1)*transform_score) - (ni*(ri*nu)*(1-beta)) - ((nu+1)*(1-beta)*(ni*tu)) - (beta*nu*ru*ni) - (beta*(ni+1)*nu*ti))
            else:#case5_part3
                biased_score = ((ni+1)*transform_score) - (ru*ni)

    elif tu >= 0 and ti <= 0 and ru < ri:#CASE6
        biased_score = (1/((ni*(1-beta))+1+(beta*nu))) * (((nu+1)*(ni+1)*transform_score) - (beta*(nu+1)*(ru*ni)) - ((1-beta)*(ni+1)*(ri*nu)))

    else:
        print ("ru:", ru,"ri: ",ri,"tu: ",tu,"ti: ",ti,"nu: ",nu,"ni: ",ni)
        print("error in transformation")
        exit(0)

    return biased_score

def main():
    data_file=sys.argv[1]
    bias_file = sys.argv[2]
    test_data = pd.read_csv(data_file)

    user_dict = np.load("user_dict.npy",allow_pickle=True).item()
    item_dict = np.load("item_dict.npy",allow_pickle=True).item()

    biased = []
    beta = 0.5
    for i in range(len(test_data)):
        bias = bias_score(test_data['Unbiased_Score'][i], beta, user_dict[test_data['UserId'][i]],item_dict[test_data['ProductId'][i]])
        biased.append(bias)

    test_data['Biased_Score'] = biased

    print('MSE: ',mean_squared_error(test_data['Biased_Score'], test_data['Score']))
    print('MAE: ',mean_absolute_error(test_data['Biased_Score'], test_data['Score']))
    print('RMSE: ',(mean_squared_error(test_data['Biased_Score'], test_data['Score']))**0.5)

    test_data.to_csv(bias_file, index=False)

if __name__== "__main__":
    main()