if __name__ == '__main__':
    import pandas as pd
    import sys

    USAGE = 'Usage: python merge_csv.py <file1.csv> <file2.csv> <output.csv>'

    if len(sys.argv) < 3:
        print(USAGE)
        exit(1)

    output_name = 'merged.csv'
    if len(sys.argv) == 4:
        output_name = sys.argv[3]

    # Read the files into two dataframes.
    df1 = pd.read_csv(sys.argv[1])
    df2 = pd.read_csv(sys.argv[2])

    # Merge the two dataframes, using _ID column as key
    df3 = pd.merge(df1, df2, on='id')
    df3.set_index('id', inplace=True)

    # Write it to a new CSV file
    df3.to_csv(output_name)
