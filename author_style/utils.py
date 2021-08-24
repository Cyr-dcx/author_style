import os

actual=os.getcwd()
path=os.path.join(actual, 'raw_data', 'fichiers_txt', 'comp_aut')

#clean data
def clean_texts():

    book_names=[f for f in os.listdir(path) if f.endswith('.txt')]

    for book in book_names:
        with open(os.path.join(path, book)) as f:
            lines = f.readlines()
        #remove begining
        for line in lines:
            if line in ['I\n', '1\n', 'Gallimard\n', 'PREMIÈRE PARTIE\n', 'CHAPITRE PREMIER\n', 'Chapitre 1\n', '> Digitalizzazione a cura di Yorikarus @ forum.tntvillage.scambioetico.org <\n', 'LES CHEVAUX\n', 'SAINT-JUST\n']:
                index=lines.index(line)
                del lines[0:index+1]
                break

        #remove ending
        index =int(len(lines)*(1-0.1))
        del lines[index:len(lines)]

        #remove spaces at the end and begining
        lines=''.join(lines).strip()

        #create cleaned texts
        file=open(os.path.join(actual, 'author_style', 'data', book), 'w')
        file.write(lines)

if __name__=='__main__':
    clean_texts()
