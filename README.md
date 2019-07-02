# Purchase-Analytics-InsightDataChallenge

## Implementation Summary
_by Joy Qi_

This repo has implemented submissions to the Insight Data Science Challenge 2019.

### Language

Python 3.7

### Problems
**Input Datasets** <br/>
`order_products.csv` <br/>
`products.csv`

**Output Dataset** <br/>
`report.csv`: Calculated information that for each department, the number of times a product was requested, number of times a product was requested for the first time, and a ratio of those two numbers.

### Steps

1. Load csv files from the `input` folder
2. Clean the DataFrame by filtering columns selectively 
3. Join the two cleaned DataFrame
4. Groupby `department_id` and aggregate twice to count for number of (first) orders
5. Apply column functions
    - Filter out `number_of_records` greater than 0
    - Calculate `percentage` column and round it to the second decimal 
    - Sort the result DataFrame by `department_id` in ascending order
6. Save the result DataFrame as a `.csv` file and into the `output` folder
