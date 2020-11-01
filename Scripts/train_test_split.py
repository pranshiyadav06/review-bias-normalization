import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    data_file=sys.argv[1]
    training_data = sys.argv[2]
    testing_data = sys.argv[3]

    data = pd.read_csv(data_file)
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    train = train_data.copy()
    test = test_data.copy()

    #Remove products that are not present in training data but present in test data
    cond_prod = ~test['ProductId'].isin(train['ProductId'])
    test.drop(test[cond_prod].index, inplace = True)

    #Remove users that are not present in training data but present in test data
    cond_user = ~test['UserId'].isin(train['UserId'])
    test.drop(test[cond_user].index, inplace = True)

    train.to_csv(training_data, index=False)
    test.to_csv(testing_data, index=False)

if __name__== "__main__":
    main()