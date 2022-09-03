import pandas as pd
import numpy as np
import warnings

from pandas.core.common import SettingWithCopyWarning

def to_cumulative(stream: list):
  # clean data and create dataframe
  list_clean = []
  for i in stream:
    list_clean.append(list(i.split(",")))

  df = pd.DataFrame.from_records(list_clean)

  UniqueTicker = df[1].unique()

  DataFrameDict = {elem: pd.DataFrame() for elem in UniqueTicker}

  for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df[1] == key]

  for key in DataFrameDict.keys():
    DataFrameDict[key][2] = DataFrameDict[key][2].astype(int)
    DataFrameDict[key][3] = DataFrameDict[key][3].astype(float)
    DataFrameDict[key]['notional'] = DataFrameDict[key][2] * DataFrameDict[key][3]
    DataFrameDict[key]['cum_qty'] = DataFrameDict[key][2].cumsum()
    DataFrameDict[key]['cum_not'] = DataFrameDict[key]['notional'].cumsum()

  # print(DataFrameDict['A'])

  df_new = pd.concat(DataFrameDict.values(), ignore_index=True)
  df_new.sort_values(by=[0], inplace=True)


  # print(df_new)

  unique_timestamp = df_new[0].unique()

  DataFrameDict1 = {elem: pd.DataFrame() for elem in unique_timestamp}

  for key in DataFrameDict1.keys():
    DataFrameDict1[key] = df_new[:][df_new[0] == key]

  return_list = []
  appending_string = ''

  for key in DataFrameDict1.keys():
    DataFrameDict1[key].sort_values(by=[1, 2], inplace=True)
    DataFrameDict1[key] = DataFrameDict1[key].reset_index(drop=True)
    print(DataFrameDict1[key])
    appending_string += str(DataFrameDict1[key].iloc[0, 0]) + ','
    for i in range(DataFrameDict1[key].shape[0]):
      appending_string += str(DataFrameDict1[key].iloc[i, 1]) + ',' + str(DataFrameDict1[key].iloc[i, 5]) + ',' + str(DataFrameDict1[key].iloc[i, 6])
      if i != DataFrameDict1[key].shape[0]-1:
        appending_string += ','
    return_list.append(appending_string)
    appending_string = ''
  return return_list
  
  # raise Exception

def to_cumulative_delayed(stream: list, quantity_block: int):
  list_clean = []
  for i in stream:
    list_clean.append(list(i.split(",")))

  df = pd.DataFrame.from_records(list_clean)

  UniqueTicker = df[1].unique()

  DataFrameDict = {elem: pd.DataFrame() for elem in UniqueTicker}

  for key in DataFrameDict.keys():
    DataFrameDict[key] = df[:][df[1] == key]
    DataFrameDict[key] = DataFrameDict[key].reset_index(drop=True)

  list_of_repeat_lists = []
  
  for key in DataFrameDict.keys():
    DataFrameDict[key][2] = DataFrameDict[key][2].astype(int)
    duplicate_indexes = list(np.where(DataFrameDict[key][2] > 1)[0])

    for i in duplicate_indexes:
      repeat = DataFrameDict[key].loc[i]
      repeat_value = repeat.iloc[2]

      repeat[2] = 1
      repeat_list = repeat.values.tolist()
      
      for j in range(repeat_value):
          list_of_repeat_lists.append(repeat_list)
    
    append_df = pd.DataFrame.from_records(list_of_repeat_lists)

    for i in duplicate_indexes:
      DataFrameDict[key] = DataFrameDict[key].drop([i])

    DataFrameDict[key] = pd.concat([DataFrameDict[key], append_df])
    DataFrameDict[key].sort_values(by=[0], inplace=True)
    DataFrameDict[key] = DataFrameDict[key].reset_index(drop=True)

    list_of_repeat_lists.clear()

  return_list = []

    
  for key in DataFrameDict.keys():
    DataFrameDict[key][2] = DataFrameDict[key][2].astype(int)
    DataFrameDict[key][3] = DataFrameDict[key][3].astype(float)
    DataFrameDict[key]['notional'] = DataFrameDict[key][2] * DataFrameDict[key][3]
    DataFrameDict[key]['cum_qty'] = DataFrameDict[key][2].cumsum()
    DataFrameDict[key]['cum_not'] = DataFrameDict[key]['notional'].cumsum()

    for i in DataFrameDict[key].index:
      if (i+1) % quantity_block == 0:
        return_list.append(DataFrameDict[key].loc[i].tolist())

  return_df = pd.DataFrame.from_records(return_list)
  return_df.sort_values(by=[0], inplace=True)

  appending_string = ''
  function_return = []
  return_list_of_lists = []

  for i in range(return_df.shape[0]):
    appending_string += str(return_df.iloc[i, 0]) + ',' + str(return_df.iloc[i, 1]) + ',' + str(return_df.iloc[i, 5]) + ',' + str(return_df.iloc[i, 6])
    function_return.append(appending_string)
    return_list_of_lists.append(function_return.copy())
    appending_string = ''
    return_list.clear()
  return function_return

  
#   raise Exception

# if __name__ == "__main__":
  