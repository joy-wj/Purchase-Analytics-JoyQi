import pandas as pd
import sys
import numpy as np


def load_clean(file_path, name):
    """
    :param file_path: a string object of the file path that stores the csv file
    :param name: a string object indicating filter condition
    :return: a DataFrame read from Pandas
    """
    df = pd.read_csv(file_path)

    # filter out irrelevant columns for space constrain
    if name == 'products':
        df = df[['product_id', 'department_id']]
    elif name == 'order_products':
        df.drop(['add_to_cart_order'], axis=1, inplace=True)
    return df


def get_order_counts(input_df_1, input_df_2):
    """
    :param input_df_1: DataFrame object created from input file
    :param input_df_2: DataFrame object created from input file
    :param common_cols: a list object of Common column names between the two DataFrames
    :return: a joined Dataframe object for output file
    """
    common_cols = np.intersect1d(input_df_1.columns, input_df_2.columns)
    df_join = pd.merge(input_df_1, input_df_2, how='left', on=[col for col in common_cols])

    # create two separate count DataFrames below:
    # 1) counts for number_of_orders
    by_dep = df_join.groupby(by='department_id')
    by_dep_count = by_dep['reordered'].count()
    by_dep_count = pd.DataFrame(by_dep_count)
    by_dep_count.rename(index=str, columns={'reordered': 'number_of_orders'}, inplace=True)

    # 2) counts for number_of_first_orders
    by_dep_first = df_join[df_join['reordered'] == 0].groupby(by='department_id')
    by_dep_first_count = by_dep_first['reordered'].count()
    by_dep_first_count = pd.DataFrame(by_dep_first_count)
    by_dep_first_count.rename(index=str, columns={'reordered': 'number_of_first_orders'}, inplace=True)

    # full join the above two DataFrames
    df_result = pd.merge(by_dep_count, by_dep_first_count, how='outer', left_index=True, right_index=True)

    # replace NaN to 0 and convert column types back to Int
    df_result.replace({np.NaN: 0}, inplace=True)
    df_result['number_of_orders'] = df_result['number_of_orders'].astype(int)
    df_result['number_of_first_orders'] = df_result['number_of_first_orders'].astype(int)

    # listed only if number_of_orders is greater than 0
    df_result = df_result[df_result['number_of_orders'] > 0]

    # percentage column rounded to the second decimal
    df_result['percentage'] = df_result['number_of_first_orders'] / df_result['number_of_orders']
    df_result['percentage'] = df_result['percentage'].apply(lambda x: '%.2f' % x)

    # sort by department_id and ascending order
    df_result = df_result.reset_index()
    df_result['department_id'] = df_result['department_id'].astype(int)
    df_result = df_result.sort_values(by=['department_id'], ascending=True)

    return df_result


if __name__ == '__main__':

    input_file_1 = sys.argv[1]
    input_file_2 = sys.argv[2]
    output_file = sys.argv[3]

    products = load_clean(input_file_1, 'products')
    order_products = load_clean(input_file_2, 'order_products')

    df_result = get_order_counts(products, order_products)
    df_result.to_csv(output_file, index=False)
