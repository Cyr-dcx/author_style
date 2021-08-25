import os
import pandas as pd
import csv

actual=os.getcwd()
path_folder=os.path.join(actual, 'raw_data')

#clean data
def clean_texts():

    folders=[f for f in os.listdir(path_folder)]
    for folder in folders:
        path=os.path.join(path_folder, folder)

        book_names=[f for f in os.listdir(path) if f.endswith('.txt')]

        for book in book_names:
            with open(os.path.join(path, book)) as f:
                lines = f.readlines()
            #remove begining and ending (10 %)
            ten_percent=int(len(lines)*0.1)
            del lines[len(lines)-ten_percent:len(lines)]
            del lines[0:ten_percent]

            #keeping the 300 biggest paragraphs
            lenghts={}

            for line in lines:
                index=lines.index(line)
                lenght=len(line)
                lenghts[index]=lenght
            indexes = list(k for k, v in sorted(lenghts.items(),
                                                key=lambda item: item[1],
                                                reverse=True))[0:300]

            new_lines=[]
            for index in indexes:
                new_lines.append(lines[index])

            #create cleaned texts
            file=open(os.path.join(actual, 'author_style', 'data',folder, ''.join([book.strip('.txt'), '.csv']).strip('EBOOK-').strip('Ebook-')), 'w', newline='')
            writer=csv.writer(file)
            writer.writerow(new_lines)



def csv_to_dataframes():
    ''' Returns 2 dataframes
    Extracts a dataframe with paragraphs and one for
    sentences from a csv file. The csv files names' are parsed
    assuming the following syntax:
    "Author_name - Title - Publication_date.csv"
    '''
    ################################################
    ########  convert csv to df_paragraphs  ########
    ################################################
    # Get csv path ; the csv files are arrays of pre-selected* paragraphs
    # that were extracted from raw txt files by * (cf. Lilou)
    csv_path = os.path.join(actual, '..', 'data')
    # Create a list of book names
    books = [
        csv_file for csv_file in os.listdir(csv_path)
        if csv_file.endswith('.csv')
    ]
    # Parsing text file names to get author names, book titles and publishing date
    # and putting these elements in lists that have the same index as the list 'books'
    authors = [
        csv_file.split(' ')[0] + ' ' + csv_file.split(' ')[1]
        for csv_file in books
    ]
    titles = [csv_file.split(' - ')[1] for csv_file in books]
    book_dates = [
        csv_file.split(' - ')[2].replace('.csv', '') for csv_file in books
    ]
    # Initializing a list of dataframes
    dfs = []
    # For each book (in the list 'books'),
    ## 1. create a dataframe with 1 paragraph per row
    ## 2. create columns with fixed values for other features than text
    ## 3. append the dataframe in the list 'dfs' of dataframes
    ## containing the paragraphs of all books
    for book in books:
        ## 1.
        df_temp = pd.read_csv(os.path.join(actual, '..', 'data', book),
                              header=None).T
        ## 2.
        df_temp['Author'] = authors[books.index(book)]
        df_temp['Title'] = titles[books.index(book)]
        df_temp['Book_date'] = book_dates[books.index(book)]
        ## 3.
        dfs.append(df_temp)
    ## Concatenate all dataframes in 'dfs' to get
    ## a single dataframe with paragraphs from all books
    df_paragraphs = pd.concat([df for df in dfs], ignore_index=True, axis=0)
    df_paragraphs.rename(
        mapper={0: "Text"}, axis=1, inplace=True
    )  # NB: The column name for the actual text is explicitly called in a preprocessing function, it must be 'Text'
    ########################################################
    ########  convert df_paragraphs to df_sentences  #######
    ########################################################
    # Initializing a list of dataframes
    dfs = []
    # For each paragraph of our dataset i.e. For each row in df_paragraph:
    for i in range(df_paragraphs['Text'].count()):
        # Separate sentences with '. ' as a delimiter
        # (careful: "J. C.", "Mr.", [...]) ignore ?
        sentences = str(df_paragraphs.Text[i]).split(". ")
        # Prepare columns with fixed values for Author_name, Title and Book_date,
        # to assign each sentence of a paragraph to the same Author_name, Title and Book_date.
        author_temp = [df_paragraphs.Author[i] for k in range(len(sentences))]
        title_temp = [df_paragraphs.Title[i] for k in range(len(sentences))]
        date_temp = [df_paragraphs.Book_date[i] for k in range(len(sentences))]
        # Concatenate the 4 previous lists to build a single dataframe
        # containing all sentences of the i-th paragraph of df_paragraphs
        data = [sentences, author_temp, title_temp, date_temp]
        df_temp = pd.DataFrame(data).T
        # Build the list of dataframes containing all sentences of our dataset
        dfs.append(df_temp)
    # Assemble the dataframe containing all sentences of our dataset
    df_sentences = pd.concat(dfs, ignore_index=True, axis=0)
    df_sentences.rename(mapper={
        0: "Text",
        1: 'Author',
        2: 'Title',
        3: 'Book_date'
    },
                        axis=1,
                        inplace=True)
    return df_paragraphs, df_sentences



if __name__=='__main__':
    clean_texts()
