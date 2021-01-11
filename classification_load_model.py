from myconfig import *
# create testing comment
import ast
import autosklearn.classification, csv, math, re
import numpy as np
import pandas as pd
import pickle
import spacy
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.metrics import classification_report

# TODO: change file name according to your file name and accept only csv file
input_file = "all_comments"

nlp = spacy.load('en_core_web_md')
inp = pd.read_csv(DATA_SOURCE+'/'+input_file+'.csv',encoding = "ISO-8859-1")
comment_summary = dict()
y_true = [] # collect true value from human label

# data preprocessing
def lemma(comment):
    lemma_comment = []
    doc = nlp(comment)    
    for token in doc:
        lemma_word = token.lemma_
        if(lemma_word == "-PRON-"):
            lemma_word = "pron"
        lemma_comment.append(lemma_word.lower())
    comment_out = ' '.join(lemma_comment)    
    comment_out = re.sub(r'[^A-Za-z0-9]+','   ', comment_out, flags=re.IGNORECASE)
    comment_out = re.sub(r'\s+',' ',comment_out)
    return comment_out

for ind,col in inp.iterrows():
    comment = str(col['comment']) # convert any type to str
    annotation = col['Human Label']
    y_true.append(annotation)
    keywords = ast.literal_eval(col['keyword'])
    for keyword in keywords:
        # print('comment before ', comment, 'type', type(comment))
        # print('keyword ', keyword, 'type ', type(keyword))
        comment = comment.replace(keyword, 'abstractkeyword')
    comment = re.sub(r'[^A-Za-z0-9.\']+',' ',comment)
    comment = re.sub(r'\s+',' ',comment)
    # print('comment after ', comment, '\n')
    inp.loc[ind,'commenttext'] = lemma(comment)
    comment_summary[ind] = dict()
    comment_summary[ind]['comment'] = lemma(comment)

# inp.to_csv(DATA_SOURCE+'/'+input_file+'.csv',index=False, quoting=2)

N_GRAM_LENGTH = 10
TOTAL_TYPE = 2
summary = dict()
total_n_gram = 0
total_document = len(comment_summary)
score = dict()
id_n_gram_mapping = dict()
top_vector = list()
n_grams = dict()

# print('Y_true ', y_true)

# weight = log(|D|/sdf) * gtf
csv.field_size_limit(100000000)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1   
    
#read data from n_gram
def read_n_gram():
    n_gram_id = 0
    total_n_gram = file_len(DATA_SOURCE+"/combine_on_hold_n_gram")
    print("total_n_gram",total_n_gram)
    with open(DATA_SOURCE+"/combine_on_hold_n_gram") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in reader:
            words = row[5].strip()
            term = tuple(row[5].strip().split(' '))
            if term not in summary:
                summary[term] = dict()
            summary[term] = {'id':n_gram_id,'len':row[1],'gtf':row[2],'df':row[3],'sdf':row[4], 'term':row[5]}
            weight1 = total_document / int(row[4])
            summary[term]['score'] = math.log10(weight1) * int(row[2])
            score[n_gram_id] =  math.log10(weight1) * int(row[2])
            n_grams[n_gram_id] = term
            n_gram_id += 1
# function top_score_vector
def top_score_vector():
    percent = int(len(score) * 100 / 100)
    top_vector.extend(sorted(score,key=score.get,reverse=True)[:percent])
    print("top_vector",len(top_vector))

# add comment
def n_gram_split():
    for comment_index in comment_summary:
        comment = comment_summary[comment_index]['comment']
        comment_summary[comment_index]['vector'] = dict()
        comment_post_process = re.sub("\s+"," ",re.sub(r"[^A-Za-z0-9]+"," ",comment.replace("\t"," ").replace("\r\n"," ").lower())).split(" ")
        for i in range(len(comment_post_process)):
            for j in range(i,min(i+N_GRAM_LENGTH+1,len(comment_post_process))):
                if(tuple(comment_post_process[i:j+1]) in summary):
                    if(summary[tuple(comment_post_process[i:j+1])]['id'] in top_vector):
                        if summary[tuple(comment_post_process[i:j+1])]['id'] in comment_summary[comment_index]['vector']:
                            comment_summary[comment_index]['vector'][summary[tuple(comment_post_process[i:j+1])]['id']] = 1
                        else: 
                            comment_summary[comment_index]['vector'][summary[tuple(comment_post_process[i:j+1])]['id']] = 1
                            
def vector_idf():
    for i in comment_summary:
         for v in comment_summary[i]['vector']:
            comment_summary[i]['vector'][v] *= score[v]
    
# read_raw_data()
read_n_gram()
top_score_vector()
n_gram_split()
print("finish")
#vector_idf()


# In[16]:


# currently we have top_score_vector and comment&vector
# create x and y -> x contains vector and y contains result
X = []
y = []
print("test")
for comment_index in comment_summary:
    vector = [0] * len(top_vector)
    for vector_index in comment_summary[comment_index]['vector']:
        vector[top_vector.index(vector_index)] = comment_summary[comment_index]['vector'][vector_index]
    X.append(vector)
    # y.append(comment_summary[comment_index]['type'])
print("finish")

np_X = np.asarray(X)  # convert input into an array


# add model file
with open('dump_autosk.pkl', 'rb') as input_file:
    automl = pickle.load(input_file)

print(automl)
predict = automl.predict(np_X)
print('predict= ', predict, 'length ', len(predict))
# print('Y_true ', y_true, 'length ', len(y_true))
# print('============')
print('best model= ', automl.show_models())
# print('============')
acc = accuracy_score(y_true ,predict, normalize=True)
print("Accuracy: %.3f" % acc)
print('precision ',precision_score(y_true ,predict))
print("recall ", recall_score(y_true ,predict))
print('f1 ', f1_score(y_true ,predict))
print('classification report \n', classification_report(y_true ,predict))
print('confusion matrix \n', confusion_matrix(y_true, predict, labels=[0, 1]))


# In[40]:


# print(predict[0])

# with open('dataset/predict.csv','w') as csvout:
#     writer = csv.DictWriter(csvout,fieldnames=['index','comment', 'predict'])
#     writer.writeheader()
#     for ind,value in enumerate(predict):
#         if value == 1:
#             writer.writerow({'index':ind, 'comment':inp.iloc[ind]['comment']})
#             print(ind,inp.iloc[ind]['comment'])


# write result to csv file
with open('dataset/predict.csv','w') as csvout:
    writer = csv.DictWriter(csvout,fieldnames=['index','comment', 'predict'])
    writer.writeheader()
    for ind,value in enumerate(predict):
        writer.writerow({'index':ind, 'comment':inp.iloc[ind]['comment'], 'predict':value})
#             print(ind,inp.iloc[ind]['comment'])



# In[ ]:




