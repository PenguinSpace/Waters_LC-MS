def format_sample(file_path='', return_path='', sep_files=False, file_names=None):
    """
    This function basically transforms the output file after integrating all the sample peaks in the LC-MS
    to a more readable .csv format. This new format allows the data to become more manipulable. Specifically,
    The empty spacing of the dataset is removed and a new column containing the compound name being scanned for
    by the MS is added. This allows for the search of all the compounds being scanned for across all the samples
    being easily accessible using the loc[] function. The function can also split each dataset by the compounds
    being scanned into separate files as well. Keep in mind splitting requires a for loop so excessive compounds
    leads to longer run times.

    :param path: This is path to the .csv file from the LC-MS that needs to be formatted

    :param return_path: This is the path to return all the files created in this function. Include
    the file name at the end to specify the name of the csv file

    :param sep_files: if True, then all compounds that you scan for will be place in a separate
    dataframe and exported to separate csv files. The names of the csv files are specified in
    file_names. If file_names is None, then a set of files with the compound_name.csv will be made

    :param file_names: Takes in a list of file names if sep_files=True. If no list is assigned and
    sep_files=True, then an automatic list of csv file names will be made using the compound_names.
    If sep_files=None, then this variable should be None and ignored. The number of compounds scanned
    should equal the length of the file_names list. The file names should be in the same order
    presented in the csv

    :return: 0 means program ran correctly, 1 means there was file path error, and 2 means there
    is an error in the parameters input into the function
    """
    if file_path == '':
        print('Please specify a correct file or file path to the file being read')
        return 1

    import pandas as pd

    # reads in the csv and adds in the column names
    samples = pd.read_csv(file_path)
    columns = samples.iloc[5].tolist()
    columns[0] = 'Index'
    samples.columns = columns

    # drops all the unecessary spaces in csv and resets the index
    samples = samples.dropna(subset=['Index'])
    samples = samples.reset_index(drop=True)

    # drops off the date to the file
    data = samples.drop([0], axis=0)
    data = data.reset_index(drop=True)

    # this helps separates all the rows that have the compound names
    compound_null = data['Name'].isnull()
    compound_names = data[compound_null]

    # Splits the compound name up into the parts and stores the dataframe in target
    target = compound_names['Index'].str.extract(r'(Compound)(\s)(\d*:)(\s{2})'
                                                 r'(\w*[0-9]?[\:\-]?[0-9]?\:?[\s]*?[0-9]*?\s?\w*?\w*\s?\w*\-?\w*)',
                                                 expand=True)
    # print(target[4])

    # rename the column in target which are numbers into actual name
    target.rename(columns={4: 'compound_name'}, inplace=True)
    new_series = target['compound_name'].repeat(59).reset_index(drop=True)

    # add onto the dataset to show compound names and set the index
    data.insert(1, 'compound_name', new_series)
    data.set_index('Index')

    # checks if user wants the file to be separated
    if sep_files is True:
        i = 0
        # if user didn't input file_names, then automated make some file_names for each compound
        if file_names is None:
            file_names = []
            for compound in target['compound_name']:
                new_file = str(compound) + '.csv'

        # this for loop writes all the dataframes to their respective file names
        for compound in target['compound_name']:
            mask = data['compound_name'] == compound
            temp = data.loc[mask]
            # with pd.ExcelWriter('output.xlsx') as writer:
            #     temp.to_excel(writer, sheet_name=file_names[i])
            temp.to_csv(file_names[i], index=False)
            i += 1

        return 0

    else:
        # this saves whatever we are doing to a csv file
        data.to_csv(path_or_buf=return_path, index=False)
        return 0


if __name__ == '__main__':
    format_sample(file_path='/Users/nelsonyeung/Documents/Penguin Files/Penguin Stuff/EPA/Michigan_Samples/New_MI_samples.csv',
                   return_path='/Users/nelsonyeung/Documents/Penguin Files/Penguin Stuff/EPA/Michigan_Samples/format_MI_samples.csv',
                  sep_files=False)
