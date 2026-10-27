from os.path import join, realpath, exists
from os import listdir, makedirs
import re
import nltk
import string
import config

nltk.download('punkt')  # for tokenization

def clean_txt(content):
    content = content.replace('doi', '').replace('et al', '')  # make it a one line text
    content = content.encode('ascii', 'ignore').decode()  # remove unicode chars
    content = re.sub(r'10\.\d+/[\w.\-]+', '', content)
    content = re.sub(r'https*\S+', '', content)  # remove links
    content = re.sub(r'http*\S+', '', content)
    content = re.sub(r'\s+', ' ', content)  # replace multiple spaces/tabs/..etc with single space
    content = re.sub(r'[0-9]+:[0-9]+', '', content)
    content = re.sub(r'\d+', '', content) # elsevier contains so many irrelevant numbers
    try:
        content = nltk.sent_tokenize(content)
        for i, sent in enumerate(content):
            sent = re.sub('[%s]' % re.escape(string.punctuation), ' ', sent)
            sent = re.sub(r'\s([a-zA-Z]\s)+', ' ', sent)  # remove single letters surrounded by space
            sent = re.sub(r'\s([0-9]\s)+', ' ', sent)  # remove single numbers surrounded by space
            sent = re.sub(r'\s+', ' ', sent)
            words = nltk.word_tokenize(sent)
            sent = ' '.join([w for w in words if
                             len(w) <= 45])  # longest english keyword length = 45 anything > 45 would be error in the txt
            content[i] = (sent[0:512],len(words))  # update the actual sentence in the cleaned content apply truncation here
        content = [sent_tup[0] for sent_tup in content if sent_tup[1] > 3]
        return content
    except Exception:
        return None  # return empty list in case of tokenization failure


def clean_dir(dir_path, save_to):
    filenames = listdir(dir_path)
    for filename in filenames:
        with open(join(dir_path, filename), 'r', encoding='utf-8', errors='ignore') as file:
            raw_content = file.read()
            clean_content = clean_txt(raw_content)
            if clean_content:
                print(dir_path + filename)
                with open(save_to, 'a', encoding='utf-8') as file:
                    file.write('\n'.join(clean_content))
            else:
                print("Failed to parse {}".format(dir_path))


if __name__ == '__main__':
    dir_path = join(realpath('.'), 'Data')
    target = '{}_full_txt'.format(config.API)
    print('Cleaning: {}'.format(target))
    save_to = join(dir_path, 'Cleaned_' + target)
    if not exists(save_to):
        makedirs(save_to)

    dir_path = join(dir_path, target)
    clean_dir(dir_path, join(save_to, target + '.txt'))
