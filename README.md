This repository contains the source code to reproduce the results of the [AACL-IJCNLP'20](https://aacl2020-srw.github.io/)
paper [Unbiasing Review Ratings with Tendency based Collaborative Filtering](https://www.aclweb.org/anthology/2020.aacl-srw.8).

Appendix contains the derivation of the reverse tendency function used in our paper.

## Dataset
  ### We have tested the model on two datasets
  [Amazon electronics dataset (5 core)](https://jmcauley.ucsd.edu/data/amazon/)
  
  [Amazon fine food review dataset](https://www.kaggle.com/snap/amazon-fine-food-reviews)

## Implementation details

All input and output file paths are to be given in the command window, except dictionary file (user_dict and item_dict) path. The scripts should be implemented in the following order

json_to_csv.py
  - Input: Input data_file_name.json (eg. reviews_Electronics_5.json) data file (format: Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text)
  - Output: data.csv data file (format: Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text)
  - running command: 
  ```sh
  $ python json_to_csv.py reviews_Electronics_5.json data.csv
  ```

### Preprocessing
preprocess.py
  - Input: data.csv data file (format: Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text)
  - Output: preprocessed_data.csv data file (format: Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text)
  - running command: 
  ```sh
  $ python preprocess.py data.csv preprocessed_data.csv
  ```

data_clean.py
  - Input: preprocessed_data.csv data file (format: Id,ProductId,UserId,ProfileName,HelpfulnessNumerator,HelpfulnessDenominator,Score,Time,Summary,Text)
  - Output: clean_data.csv data file (format: ProductId,UserId,Summary,Text,Score)
  - running command: 
  ```sh
  $ python data_clean.py preprocessed_data.csv clean_data.csv
  ```

data_struct.py
  - Input: clean_data.csv data file (format: ProductId, UserId, Summary, Text, Score)
  - Output: Dictionary user_dict.npy (user_id: [n_i, user_mean_score, user_tendency], product_id: [n_u, item_mean_score, item_tendency])
  - running command: 
  ```sh
  $ python data_struct.py clean_data.csv
  ```

pruning.py (the minimum value for pruning should be updated for other datasets. In the file it is set at 12)
  - Input: clean_data.csv data file (format: ProductId, UserId, Summary, Text, Score)
  - Output: pruned_data.csv, extra.csv (not on this data) data files(format: ProductId, UserId, Summary, Text, Score)
  - running command: 
  ```sh
  $ python pruning.py clean_data.csv pruned_data.csv extra.csv
  ```

train_test_split.py
  - Input: pruned_data.csv data file (format: ProductId,UserId,Summary,Text,Score)
  - Output: Training train_data.csv file, test test_data.csv file (format: ProductId, UserId, Summary, Text, Score)
  - running command: 
  ```sh
  $ python train_test_split.py pruned_data.csv train_data.csv test_data.csv
  ```

data_struct.py
  - Input: train_data.csv data file (format: ProductId, UserId, Summary, Text, Score)
  - Output: Dictionary user_dict.npy (user_id: [n_i, user_mean_score, user_tendency], product_id: [n_u, item_mean_score, item_tendency])
  - running command: 
  ```sh
  $ python data_struct.py pruned_data.csv
  ```

### Normalization of review score
unbias.py
  - Input: test_data.csv data file (format: ProductId, UserId, Summary, Text, Score)
  - Output: unbiased_data.csv data file (format: ProductId, UserId, Summary, Text, Score, Unbiased_Score)
  - running command:
  ```sh
  $ python unbias.py train_data.csv.csv unbiased_data.csv
  ```
### Prediction of review score using reverse tendency function
predict_bias.py
  - Input: unbiased_data.csv data file (format: ProductId, UserId, Summary, Text, Score, Unbiased_Score)
  - Output: predicted_data.csv data file (format: ProductId, UserId, Summary, Text, Score, Unbiased_Score, Biased_Score)
  - running command:
  ```sh
  $ python predict_bias.py unbiased_data.csv predicted.csv
  ```

### Analysis of predicted review score
Further analysis on the data is done in iPython notebooks for better visualization of result. The location for input and output files should be changed accordingly. The notebook was written in Google Colab and has to be modified to run on other softwares

## Citing this Work

If you use this method in your research, please cite:

```
@inproceedings{yadav-etal-2020-unbiasing,
    title = "Unbiasing Review Ratings with Tendency Based Collaborative Filtering",
    author = "Yadav, Pranshi  and
      Yadav, Priya  and
      Nokhiz, Pegah  and
      Gupta, Vivek",
    booktitle = "Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing: Student Research Workshop",
    month = dec,
    year = "2020",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.aacl-srw.8",
    pages = "50--56",
    abstract = "User-generated contents{'} score-based prediction and item recommendation has become an inseparable part of the online recommendation systems. The ratings allow people to express their opinions and may affect the market value of items and consumer confidence in e-commerce decisions. A major problem with the models designed for user review prediction is that they unknowingly neglect the rating bias occurring due to personal user bias preferences. We propose a tendency-based approach that models the user and item tendency for score prediction along with text review analysis with respect to ratings.",
}
```
