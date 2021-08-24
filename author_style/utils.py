import os
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


if __name__=='__main__':
    clean_texts()
