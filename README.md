# Team REcurse
# Credit Suisse 2022 Entry Submission 

## Introduction
Hello! We are Team REcurse and this repo consists of our solution to the Credit Suisse CodeIT 2022 Entry Challenge submission. This solution is built using Python in conjunction with Python Pandas and Numpy library. Through this README, we will provide you with a brief walkthrough of our solution as well 

## Assumptions
Besides the assumptions stated in the challenge statement, here are some additional assumptions put in place while architecting this solution: 
1. Assume that there are no duplicate entries, i.e. no statements such as ```['00:01,A,5,5.5','00:01,A,5,5.5',''00:01,A,5,5.5']``` for execution of to_cumulative function
2. Assume that there are no empty or invalid function calls, as shown in the following:

```
//Empty calls (example below) are assumed to be excluded from test cases
to_cumulative() 
to_cumulative_delayed()

//Erroneous calls (examples below) with invalid input parameters are assumed to be excluded from test cases 
//Calls must be made with specified input parameters 
to_cumulative('4')  
to_cumulative_delayed('00:01,A,5,5.5) 
```
3. Quantity block for ```to_cumulative_delayed function is a positive, non-zero integer

##Description
### ```to_cumulative``` function Walkthrough
1. Clean data and create main dataframe
2. Split main dataframe into smaller dataframes by unique ticker
3. Store dataframe with unique ticker into dictionary
4. Calculate notional, cumulative notional and cumulative quantity for each row of data in each dataframe for each specific ticker
5. Concatenate smaller dataframes together and sort by timestamp
6. Split concatenated dataframe into smaller dataframes by unique timestamp
7. Extract rows from smaller dataframes and convert type into string to store in list
8. Return list as output

### ```to_cumulative_delayed``` function Walkthrough
1. Clean data and create main dataframe
2. Split main dataframe into smaller dataframes by unique ticker
3. Store dataframe with unique ticker into dictionary
4. Replicate rows with quantity more than 1 and explode these rows into row with same values but quantity 1 (illustrated in codeblock below). This is to segment rows such that quantity block can be evaluated accurately

```
// row before processing
['00:02,A,3,5.5'] 

// rows after processing
[['00:02,A,1,5.5'],
['00:02,A,1,5.5'] 
['00:02,A,1,5.5']]
``` 
5. Calculate notional, cumulative notional and cumulative quantity for each row of data in each dataframe for each specific ticker
6. Append return list with rows that are in multiples of quantity block
7. Return list

## Authors and acknowledgement
Lim Sui Kiat (NTU REP)
