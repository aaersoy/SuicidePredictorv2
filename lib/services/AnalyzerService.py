from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import pandas as pd
class AnalyzerService:

    __instance = None

    def __init__(self):
        if AnalyzerService.__instance is None:
            AnalyzerService.__instance = self
        else:
            raise Exception("PredictorService object exist.")

    @staticmethod
    def get_instance():
        if not AnalyzerService.__instance:
            __instance=AnalyzerService()

        return AnalyzerService.__instance


    def prepare_for_predict(self,dataframe):
        dataframe = dataframe.drop(["suicides/100k pop"], axis=1)
        dataframe=dataframe.drop(["_key"], axis=1)
        dataframe = dataframe.drop(["Period"], axis=1)
        dataframe = dataframe.drop(["Name"], axis=1)
        # dataframe = dataframe.dropna(axis=1)
        X = dataframe.drop(["suicide no"], axis=1)
        Y = dataframe["suicide no"]

        return X,Y



    """Delete categorical columns that contains missing value"""
    def delete_categorical_columns(self, dataframe,del_col):

        dataframe=dataframe.drop(del_col,axis=1)
        print(dataframe.keys())

        return dataframe

    """Delete rows that contains missing value"""
    def delete_missing_attr_row(self,dataframe):
        return dataframe.dropna(axis=0)



    """Delete columns that contains missing value"""
    def delete_missing_attr_column(self,dataframe):

        return dataframe.dropna(axis=1)


    """Filling missinig values with mean of their categorie represented with key.
        If there is no value their category, put mean of all categories for that value."""
    def fill_missing_attr(self,dataframe,key,categorical_indices,begin_index=0,default='mean'):
        dataframe=dataframe.reset_index()
        dataframe=dataframe.drop(columns=['index'],axis=1)

        i=begin_index+1
        previous=dataframe[key][0]
        previous_index=0
        while i< len(dataframe):
            if previous != dataframe[key][i] or i == len(dataframe)-1:

                k=0
                while k < len(dataframe.keys()):
                    if k not in categorical_indices:
                        if default=='mean':
                            dataframe.iloc[previous_index:i, k]= dataframe.iloc[previous_index:i, k].fillna(dataframe.iloc[previous_index:i, k].mean())
                        elif default=='median':
                            dataframe.iloc[previous_index:i, k] = dataframe.iloc[previous_index:i, k].fillna(dataframe.iloc[previous_index:i, k].median())
                    k=k+1

                previous_index=i
                previous = dataframe[key][i]
            i=i+1

        k = 0
        while k < len(dataframe.keys()):
            if k not in categorical_indices:
                if default == 'mean':
                    dataframe.iloc[begin_index:, k] = dataframe.iloc[begin_index:, k].fillna(dataframe.iloc[begin_index:, k].mean())

                elif default == 'median':
                    dataframe.iloc[begin_index:, k] = dataframe.iloc[begin_index:, k].fillna(
                        dataframe.iloc[begin_index:, k].median())
            k = k + 1

        return dataframe





    """Normalize numerical data"""
    def normalize_data(self,dataframe):

        columns=dataframe.keys();

        dataframe=preprocessing.normalize(dataframe)


        print("Dataset contains non-numeric variables")

        print(dataframe)
        dataframe=pd.DataFrame(data=dataframe,columns=columns)
        return dataframe


    def train_linear_reg_model(self,train,test):
        logReg = LogisticRegression()
        logReg.fit(train,test)
        return logReg

    def predict_linear_reg_model(self,test,test_target,model):

        prediction=model.predict(test)
        print(prediction-test_target)

    def categorical_to_numeric(self,dataframe):

        dataset=dataframe.to_numpy()
        onehot_encoder=OneHotEncoder(sparse=False)
        dataset = dataset[0:,2].reshape(len(dataset), 1)
        onehot_encoded = onehot_encoder.fit_transform(dataset)

        return dataset




