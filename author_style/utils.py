import os
import pandas as pd
import csv


root_path = os.path.dirname(os.path.dirname(__file__))
path_folder = os.path.join(root_path, 'raw_data')


#clean data
def clean_texts():

    folders = [f for f in os.listdir(path_folder)]
    for folder in folders:
        path = os.path.join(path_folder, folder)

        book_names = [f for f in os.listdir(path) if f.endswith('.txt')]

        for book in book_names:
            with open(os.path.join(path, book)) as f:
                lines = f.readlines()
            #remove begining and ending (15 %)
            ten_percent = int(len(lines) * 0.15)
            del lines[len(lines) - ten_percent:len(lines)]
            del lines[0:ten_percent]

            #keeping the 300 biggest paragraphs
            lenghts = {}

            for line in lines:
                if len(line)<= 100:
                    continue
                index = lines.index(line)
                lenght = len(line)
                lenghts[index] = lenght
            indexes = list(k for k, v in sorted(lenghts.items(),
                                                key=lambda item: item[1],
                                                reverse=True))[0:300]

            new_lines = []
            for index in indexes:
                new_lines.append(lines[index])

            #create cleaned texts
            file = open(os.path.join(
                root_path, 'author_style', 'data', folder,
                ''.join([book.strip('.txt'),
                         '.csv']).strip('EBOOK-').strip('Ebook-')),
                        'w',
                        newline='')
            writer = csv.writer(file)
            writer.writerow(new_lines)


def csv_to_dataframes(output='ps'):
    ''' Returns 2 dataframes

    Extracts 1 dataframe with paragraphs and 1 dataframe with
    sentences from a csv file. The csv files names' are parsed
    assuming the following syntax:
    "author_name - title - publication_date.csv"
    '''
    ##########################b#####################
    ###y####  convert csv to df_paragraphs  ########
    ################################################

    # Get csv path ; the csv files are arrays of pre-selected* paragraphs
    # that were extracted from raw txt files by * (cf. Lilou)
    csv_path= os.path.join(root_path, 'author_style', 'data',
                                     'comp_aut')


    # Create a list of book names
    books = [
        csv_file for csv_file in os.listdir(csv_path)
        if csv_file.endswith('.csv')]


    # Parsing csv file names to get author names, book titles and publishing date
    # and putting these elements in lists that have the same index as the list 'books'
    authors = [csv_file.split(' ')[0]+' '+csv_file.split(' ')[1] for csv_file in books]
    titles = [csv_file.split(' - ')[1] for csv_file in books]
    book_dates = [csv_file.split(' - ')[2].replace('.csv','') for csv_file in books]

    # Initializing a list of dataframes
    dfs = []

    # For each book (in the list 'books'),
    ## 1. create a dataframe with 1 paragraph per row
    ## 2. create columns with fixed values for other features than text
    ## 3. append the dataframe in the list 'dfs' of dataframes
    ## containing the paragraphs from all books

    for book in books:
        ## 1.
        df_temp = pd.read_csv(os.path.join(root_path,'author_style','data', 'comp_aut',book), header=None).T
        ## 2.
        df_temp['author'] = authors[books.index(book)]
        df_temp['title'] = titles[books.index(book)]
        df_temp['book_date'] = book_dates[books.index(book)]
        ## 3.
        dfs.append(df_temp)

    ## Concatenate all dataframes in 'dfs' to get
    ## a single dataframe with paragraphs from all books
    df_paragraphs = pd.concat([df for df in dfs], ignore_index = True, axis=0)
    df_paragraphs.rename(mapper={0:"text"}, axis=1, inplace=True) # NB: The column name for the root_path text is explicitly called in a preprocessing function, it must be 'text'

    ###############y########################################
    ########  convert df_paragraphs to df_sentences  #######
    #######################################b################

    # Initializing a list of dataframes
    dfs = []

    # For each paragraph of our dataset (i.e. for each row in df_paragraph):
    for i in range(df_paragraphs['text'].count()):

        # Separate sentences with '. ' as a delimiter
        # (careful: "J. C.", "Mr.", [...]) ignore ?
        sentences = str(df_paragraphs.text[i]).split(". ")

        # Prepare columns with fixed values for Author_name, Title and Book_date,
        # to assign each sentence of a paragraph to the same Author_name, Title and Book_date.
        author_temp = [df_paragraphs.author[i] for k in range(len(sentences))]
        title_temp = [df_paragraphs.title[i] for k in range(len(sentences))]
        date_temp = [df_paragraphs.book_date[i] for k in range(len(sentences))]

        # Concatenate the 4 previous lists to build a single dataframe
        # containing all sentences of the i-th paragraph of df_paragraphs
        data = [sentences, author_temp, title_temp, date_temp]
        df_temp = pd.DataFrame(data).T

        # Build the list of dataframes containing all sentences of our dataset
        dfs.append(df_temp)

    # Assemble the dataframe containing all sentences of our dataset
    df_sentences = pd.concat(dfs, ignore_index = True, axis=0)
    df_sentences.rename(mapper={0:"text", 1: 'author', 2:'title', 3 : 'book_date'}, axis=1, inplace=True)

    if output == 'p':
        return df_paragraphs
    if output == 's':
        return df_sentences
    if output == 'ps':
        return df_paragraphs, df_sentences

if __name__=='__main__':
    clean_texts()
