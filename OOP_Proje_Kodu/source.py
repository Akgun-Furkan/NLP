import os
import fitz
sayac = 0
words_math = []
words_of_math, words_of_science, words_of_history = [],[],[]
with open("stop_words_english.txt",'r') as stop_words:
    stopwords = stop_words.read()
    stopwords = stopwords.split()
    #print(r) #stop words print


filedir = os.path.dirname(__file__)# bu dosyanin pathi
test_p = os.path.join(filedir, 'test')# test dosyasinin pathi relative
train_p = os.path.join(filedir, 'train')# teach dosyasinin pathi relative

paths_in_train = [os.path.join(train_p,i) for i in os.listdir(train_p)]
paths_in_test = [os.path.join(test_p,i) for i in os.listdir(test_p)]

bad_chars = [';', ':', '!',',', "(", ")" , "#" ,"[","]","{","}","&","¥","£","-","_", "."]

for folder in paths_in_train:
    full_text = []
    print(folder)
    for file in os.listdir(folder):
        print("Okunan Dosya: ", file)
        dosya_konumu = os.path.join(folder, file)
        with fitz.open(dosya_konumu) as f:
            text_get = ""
            for page in f:
                text_get += page.get_text()
            last_words = text_get.split("\n")
            for words in last_words:
                words = words.lower()
                text = words.split(' ')
                for new in text:
                    full_text.append(new)
    clean_text = []
    for i in full_text:
        i = ''.join((filter(lambda k: k not in bad_chars, i)))
        if i != '' and len(i) >3:
            if i not in stopwords:
                clean_text.append(i)
    print(clean_text)
    #ÖĞRENDİĞİ BİLGİLERİ KATEGORİZE ETME
    if os.listdir(train_p)[sayac] == "matematik":
        print("Matematiğe aktarılıyor")
        words_of_math = list(set(clean_text))
    elif os.listdir(train_p)[sayac] == "tip":
        print("Tıpa aktarılıyor")
        words_of_science = list(set(clean_text))
    elif os.listdir(train_p)[sayac] == "tarih":
        print("Tarihe aktarılıyor")
        words_of_history = list(set(clean_text))

    sayac += 1

#ÖĞRENME AŞAMASI TAMAMLANDI

#TEST ZAMANI
print("TEST BAŞLIYOR")
for test_folder in paths_in_test:
    clean_text = []
    text = []
    full_text = []
    for test_file in os.listdir(test_folder):
        print("Okunan test dosyası: ", test_file)
        science_possibility, history_possibility, math_possibility = 0, 0, 0
        dosya_konumu = os.path.join(test_folder, test_file)
        with fitz.open(dosya_konumu) as fi:
            text_get = ""
            for page in fi:
                text_get += page.get_text()
            last_words = text_get.split("\n")
            for words in last_words:
                words = words.lower()
                text = words.split(' ')
                for new in text:
                    full_text.append(new)

        for h in full_text:
            h = ''.join((filter(lambda k: k not in bad_chars, h)))
            if h != '' and len(h) > 3:
                if h not in stopwords:
                    clean_text.append(h)

        for word in set(clean_text):
            for word_science in words_of_science:
                if word == word_science:
                    science_possibility += 1
            for word_math in words_of_math:
                if word == word_math:
                    math_possibility += 1
            for word_history in words_of_history:
                if word == word_history:
                    history_possibility += 1

        science_possibility = science_possibility / (len(set(words_of_science + clean_text)))
        history_possibility = history_possibility / (len(set(words_of_history + clean_text)))
        math_possibility = math_possibility / (len(set(words_of_math + clean_text)))

        print("Kitap adi: " + test_file)
        print("Tıp: " + str(science_possibility))
        print("Tarih: " + str(history_possibility))
        print("Mat: " + str(math_possibility))
        if science_possibility > math_possibility and science_possibility>history_possibility:
            print("Tıp kitabıdır")
        elif math_possibility > science_possibility and math_possibility >history_possibility:
            print("Matematik kitabıdır")
        elif history_possibility > science_possibility and history_possibility > math_possibility:
            print("Tarih kitabıdır")
        else:
            print("Kitap türü tespit edilemedi")
