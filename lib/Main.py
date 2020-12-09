import os

from lib.repo.MemoryRepository import MemoryRepository
from pathlib import Path

from lib.services.AnalyzerService import AnalyzerService
from scipy.stats import pearsonr
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

MemoryRepository.get_instance()
dataframe=MemoryRepository.get_instance().get_all_data_dataframe()

# dataframe=AnalyzerService.get_instance().fill_missing_attr(dataframe=dataframe,key='country',categorical_indices=[0,1],default='mean')

# dataframe=AnalyzerService.get_instance().delete_missing_attr_column(dataframe=dataframe)
dataframe=AnalyzerService.get_instance().delete_missing_attr_row(dataframe=dataframe)
i=0
# print(dataframe.iloc[0:,0].to_numpy())

dataframe=AnalyzerService.get_instance().delete_categorical_columns(dataframe=dataframe,del_col=['country','Name','Name.1'])
# print(dataframe)



# dataframe=AnalyzerService.get_instance().categorical_to_numeric(dataframe=dataframe)
# dataframe=AnalyzerService.get_instance().normalize_data(dataframe=dataframe)
dataframe=AnalyzerService.get_instance().normalize_data(dataframe=dataframe)

print(dataframe)
# print(dataframe.iloc[0:,0])
# print(dataframe.iloc[0:,3])
# corr2=stats.pointbiserialr(dataframe[0:,0], dataframe[0:,1])
# print(corr2)
# dataframe=pd.DataFrame(data=dataframe)
# for i in range(17):
#     print("---------------------------------")
#     print("asdasd")    # print(dataframe[i])
#
#     corr=dataframe.corr()
#     # corr = pearsonr(dataframe[0:,i], dataframe[0:,1])
#     print(corr)
#     sns.heatmap(corr,xticklabels=corr.columns,yticklabels=corr.columns,annot=True)
#     print("----------------------------------")



corr=dataframe.corr()
print(corr)
# plt.imshow(corr, cmap='hot', interpolation='nearest')

sns.heatmap(corr,xticklabels=corr.columns,yticklabels=corr.columns,annot=True,cmap='Greys')
plt.show()




# model=PredictorService.train_linear_reg_model(self=None,train=x_train[0:int(len(x_train)*80/100)],test=y_train[0:int(len(x_train)*80/100)])
# PredictorService.predict_linear_reg_model(self=None,test=x_train[int(len(x_train)*80/100):len(x_train)],test_target=y_train[int(len(x_train)*80/100):len(y_train)],model=model)


# model=PredictorService.train_linear_reg_model(self=None,train=x_train[0:int(len(x_train)-10)],test=y_train[0:int(len(y_train)-10)])
# PredictorService.predict_linear_reg_model(self=None,test=x_train[int(len(x_train)-10):len(x_train)],test_target=y_train[int(len(y_train)-10):len(y_train)],model=model)

