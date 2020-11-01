import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def debias_score(beta, user_list, item_list):
    ni = user_list[0]
    nu = item_list[0]
    ru = user_list[1]
    ri = item_list[1]
    tu = user_list[2]
    ti = item_list[2]

    # print "ru:", ru,"ri: ",ri,"tu: ",tu,"ti: ",ti,"nu: ",nu,"ni: ",ni
    if tu >= 0 and ti >= 0:
        transform_score = max(ru+ti, ri+tu)
    elif tu < 0 and ti < 0:
        transform_score = min(ru+ti, ri+tu)    
    elif tu <= 0 and ti >= 0 and ru <= ri:
        transform_score  = min(max(ru,(ri+tu)*beta + (ru + ti)*(1-beta)),ri)
    elif tu <= 0 and ti >= 0 and ru > ri:
        transform_score = ri*beta + ru*(1- beta)
    elif tu >= 0 and ti <= 0 and ru >= ri:
        transform_score  = min(max(ri,(ru+ti)*beta + (ri+tu)*(1-beta)),ru)
    elif tu >= 0 and ti <= 0 and ru < ri:
        transform_score  = ru*beta + ri*(1-beta)
    else:
        print ("ru:", ru,"ri: ",ri,"tu: ",tu,"ti: ",ti,"nu: ",nu,"ni: ",ni)
        print("error in transformation")
        exit(0)

    return transform_score


def main():
    data_file=sys.argv[1]
    unbias_file = sys.argv[2]

    test_data = pd.read_csv(data_file)
    user_dict = np.load("user_dict.npy",allow_pickle=True).item()
    item_dict = np.load("item_dict.npy",allow_pickle=True).item()

    unbiased = []
    beta = 0.5
    for i in range(len(test_data)):
        unbias = debias_score(beta, user_dict[test_data['UserId'][i]],item_dict[test_data['ProductId'][i]])
        unbiased.append(unbias)

    test_data['Unbiased_Score'] = unbiased

    test_data.to_csv(unbias_file, index=False)

    #Unbias score data frequency distribution
    unbias_data = test_data.copy()

    unbias_data['unbias'] = unbias_data['Unbiased_Score'].round()
    n, bins, patches = plt.hist(x=unbias_data['Unbiased_Score'], bins='auto', color='#0504aa',
                                alpha=0.7, edgecolor='black')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Normalized (unbiased) Review Score')
    plt.ylabel('Frequency')
    plt.show()

if __name__== "__main__":
    main()