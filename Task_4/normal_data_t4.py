import numpy as np
from sklearn.preprocessing import MinMaxScaler
import data_dssi_t4 as ds
import pandas as pd
import joblib

import os
import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np
from torch import nn, Tensor
from typing import Optional, Any, Union, Callable, Tuple
import pandas as pd
from pathlib import Path
import glob, re, os
import cardiac_ml_tools as ct
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib

def read_normal_data():

    scaler_path = './save_model_t_4/'

    data = ds.read_data() # N rows of (x, y) tuples, x.shape = (500,12), y.shape = (500,75)

    # Column 1 (leads)

    li_1 = data['leads'].tolist()
    num_sub = len(li_1)
    li_1 = np.vstack(li_1) # shape = (N*500, 12)
    scalar_list = []

    path = scaler_path + 'leads_scaler'
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(li_1)
    joblib.dump(scaler, path)

    '''
    for i in range(li_1.shape[1]):
        path = scaler_path + 'leads_scaler_' + str(i)
        scaler = MinMaxScaler()
        b = li_1[:,i].reshape(-1,1)
        normalized_data = scaler.fit_transform(b)
        joblib.dump(scaler, path)
        #scalar_list.append(scaler)
        final_dat[:,i] = normalized_data[:,0]
    '''

    a_f = np.vsplit(normalized_data, num_sub) # list of N matrices, shape = (500, 12)    
    
    # Column 2 (act)

    li_2 = data['act'].tolist()
    li_2 = [i.reshape(-1, 1) for i in li_2]
    li_2 = np.vstack(li_2) # (N*500*75, 1)

    path = scaler_path + 'act_scaler'
    scaler = MinMaxScaler()
    normalized_data_label = scaler.fit_transform(li_2)
    joblib.dump(scaler, path)

    a_f2 = np.vsplit(normalized_data_label, num_sub) # list of N arrays, shape = (500*75, 1)
    a_f2 = [i.reshape(500,-1) for i in a_f2]

    df = pd.DataFrame({'leads': a_f, 'act': a_f2})
    return df


class Custom_dataset(Dataset):
    
    def __init__(self, annotations_file):
        self.img_labels = annotations_file

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):

        x = self.img_labels.iloc[idx, 0]
        x = torch.tensor(x, dtype =torch.float32)
        y = self.img_labels.iloc[idx, 1]
        y = torch.tensor(y, dtype =torch.float32)
        return x, y
        

'''
if __name__ == "__main__":

    #device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    data = read_normal_data()
    #print(df.head())

    #print('------------------------------')

    #first_entry = df.iloc[0]
    #print(first_entry)
    #print(first_entry[1].dtype)
'''


    



