import pandas as pd

def convert_to_min_max(project_name, binary=False):
    # cleanup columns
    df = pd.read_csv(rf'benchmark_data/{project_name}/churn/weighted-churn.csv', sep=';')
    cols = [x.strip() for x in df.columns.tolist()]
    df.columns = cols
    df = df.drop(['classname', 'nonTrivialBugs', 'majorBugs',
             'criticalBugs', 'highPriorityBugs'], axis=1)

    # prepare the class column
    df.bugs = df.bugs > 0
    df.bugs = df.bugs.astype(int)

    df.to_csv(rf'data/{project_name}_weighted_clean.csv', index=None)


    # trasform to Z1, Z2

    Z1 = df[df.columns[:-2]].copy()

    Z1 = (Z1.max()-Z1)/(Z1.max()-Z1.min())
    Z2 = 1-Z1
    Z1.columns = Z1.columns + '_min'
    Z2.columns = Z2.columns + '_max'

    Z = pd.concat([Z1, Z2], axis=1)

    if binary:
        B = Z.copy()
        B[B > 0.5] = 1
        B[B <= 0.5] = 0
        B['bugs'] = df.bugs
        B.to_excel(rf'data/{project_name}_weighted_bin_min_max.xlsx', index=None)
    else:
        Z['bugs'] = df.bugs
        Z.to_csv(rf'data/{project_name}_weighted_float_min_max.csv', index=None)


def main():
    convert_to_min_max('eclipse')
    # convert_to_min_max('equinox')
    # convert_to_min_max('lucene')
    # convert_to_min_max('mylyn')
    # convert_to_min_max('pde')

main()