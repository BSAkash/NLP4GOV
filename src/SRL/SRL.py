
import os, sys
import torch
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import random
np.random.seed(0)
random.seed(0)

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk import word_tokenize
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('universal_tagset')

all_words = []
tags = ['SCONJ','CCONJ','DET','INTJ','NUM']
for elem in brown.tagged_words(tagset="universal"):
  if elem[1] in tags:
    if elem[0].lower() not in ['no','not']: all_words.append(elem[0].lower()) ##all determiners except negation

all_words = list(set(all_words))

import sklearn
from sklearn.feature_extraction import _stop_words
from sklearn.feature_extraction.text import CountVectorizer
stopwords = list(sklearn.feature_extraction.text.ENGLISH_STOP_WORDS)
stopwords.extend(all_words)

import ast
import itertools
from tqdm import tqdm
tqdm.pandas()
import json

import re
import stanza
stanza.download('en')

# import spacy
# nlp_spacy = spacy.load("en_core_web_sm")

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse',use_gpu=True)
import string
import pprint


from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

import math
from scipy.spatial import distance
from scipy.signal import find_peaks
from scipy.stats import chi2_contingency
from scipy.special import eval_chebyc

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.patches as mpatches
plt.rcParams["figure.figsize"] = (11.7,8.27)
import seaborn as sns
sns.set(rc={'figure.figsize':(11.7,8.27)})

main_arguments = ['ARG' + str(idx) for idx in range(6)]

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging
import matplotlib.pyplot as plt

"""##**Extract Predicate Arguments**##"""

#Download AllenAI model
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz",cuda_device=torch.cuda.current_device())
#SRL arguments of interest
arg_types = ['ARGM-GOL','ARGM-COM','ARGM-NEG','ARGM-MOD','ARGM-DIR','ARGM-LOC','ARGM-MNR','ARGM-TMP','ARGM-ADV','ARGM-PRP','ARGM-ADJ','ARGM-LVB','ARGM-CAU' ,
             'ARGM-PNC','ARGM-EXT','ARGM-REC','ARGM-PRD','ARGM-DIS','ARGM-DSP','ARGM-RLC','ARG0','ARG1','ARG2','ARG3','ARG4','ARG5','ARG6','V']
predictor._model = predictor._model.cuda()

"""##**Class & Methods**##"""

class SRL:
  def __init__(self, agent=None):
        self.agent = agent
        self.fpc = False

  #pass list of sentences as [{'sentence':...},{'sentence':...}]
  def srl_arg(self, sentences):
    parsed = predictor.predict_batch_json(
        sentences
    )
    outcome = dict()
    for sentence,parse in zip(sentences,parsed):
      sentence = sentence['sentence']
      verb_list = []
      for elem in parse['verbs']:
        parsed_items = dict()
        for item in arg_types:
          arg_found = re.findall("\[{}: (.*?)]".format(item), elem['description'])
          if len(arg_found) : parsed_items[item] = arg_found
        if bool(parsed_items) and 'V' in parsed_items: verb_list.append(parsed_items)
      outcome[sentence] = verb_list
    return outcome

#############################################################################################################################################
                                          ### SIDDIKI'S METHODS START FROM BELOW ###
#############################################################################################################################################

  #read a file and apply preprocessing
  def process_aim(self, x):
      if x == '<skipped>': return x

      types = [word.lemma for sent in nlp(x).sentences for word in sent.words if 'verb' in word.upos.lower()]
      if types: return ", ".join(set(types))
      else: return x

  def find_root(self,text):
      candidates = [word.text for sent in nlp(text).sentences for word in sent.words if word.deprel == 'root' and any(it in word.xpos.lower() for it in ['aux','vb'])]
      if candidates: return candidates[0]
      else:
          return "<longest>"

  def truncate(self,x):
    tokens = tokenizer.tokenize(x)
    return tokenizer.convert_tokens_to_string(tokens[:100])

  def file_read(self,file_name):
    if isinstance(file_name,str):
        data = pd.read_csv(file_name)
    else: data = file_name

    data.columns = map(str.lower, data.columns)

    # drop missing entries and size up sentences to token limit
    data.dropna(subset=['raw institutional statement'], how='any', inplace=True)
    data['raw institutional statement'] = data['raw institutional statement'].apply(lambda x: self.truncate(x))

    data = data.applymap(lambda x : str(x).lower().strip())

    data.replace("", np.nan, inplace=True)
    data.replace("nan", np.nan, inplace=True)
    #statement needs to contain aim and recipient of action at the least
    if self.agent == "eval":
        # if not self.fpc:
        data.dropna(subset=['attribute', "deontic", "aim", "object"], how='all', inplace=True)
        print("Dataset after removing uncoded statements: ", data.shape[0])

    data['sentences'] = data['raw institutional statement'].apply(lambda x : [sentence.text.lower() for sentence in nlp(x).sentences][0])
    # data = data.explode('sentences')
    # data['sentences'] = data['raw institutional statement'].apply(lambda x : x.lower())

    #find root verb through stanza
    # data['ROOT'] = data['sentences'].apply(lambda x : [word.text for sent in nlp(x).sentences for word in sent.words  if word.deprel == 'root'][0])
    data['ROOT'] = data['sentences'].apply(lambda x : self.find_root(x))

    data['srl_ip'] = data['raw institutional statement'].apply(lambda x : [{'sentence': x}])
    data['srl_parsed'] = data.apply(lambda x: self.srl_arg(x['srl_ip'])[x['raw institutional statement']],axis=1)
    # data = data[data['srl_parsed'].map(lambda d: len(d)) > 0]
    data['srl_parsed'] = data['srl_parsed'].apply(lambda x : [{'ARG0': [''], 'ARG1': [''], 'V': [''], 'ARGM-MOD': ['']}] if not len(x) else x)
    data['ROOT'] = data.apply(lambda x: "<longest>" if x.ROOT not in [it['V'][0] for it in x.srl_parsed] else x.ROOT, axis=1)

    data = data.explode('srl_parsed')
    data['srl_verb'] = data['srl_parsed'].apply(lambda x : x['V'][0])
    #keep best parsing
    data['arg_len'] = data['srl_parsed'].apply(lambda x : len(x))
    data.sort_values(by=['arg_len'], inplace=True, ascending=False)

    #only keep frame parsed for root verbs and has agents/objects  & (any(elem in x['srl_parsed'] for elem in main_arguments))
    data['keep'] = data.apply(lambda x : x['ROOT'] == x['srl_verb'] or x['ROOT'] == "<longest>", axis=1)

    ret_val = data[data['keep']]
    ret_val.drop_duplicates(subset=['raw institutional statement'], keep = 'first', inplace=True)
    # data[~data['raw institutional statement'].isin(ret_val['raw institutional statement'].to_list())].drop_duplicates(
    #                                 subset=['raw institutional statement']).to_csv("/content/testing.csv", index=False)
    return ret_val

  def detect_sub(self,text):
      doc = nlp(text)
      # sub_toks = [word.text for sent in doc.sentences for word in sent.words if 'subj' in word.deprel]
      sub_toks = [word.text for sent in doc.sentences for word in sent.words if word.deprel in ["nsubj"]]
      if sub_toks: return True
      else: return False
  #argument matching
  def argmatch(self, x, text, arg):

    keys = sorted(list(set(main_arguments) & set(x.keys())))
    if arg == 'attribute_inf':
        if 'ARG0' in x:
            return ", ".join(x['ARG0'])

        ##object present
        if len(keys) > 1 and (self.detect_sub(text) and 'ARG1' in x):
            return ", ".join(x['ARG1'])

        return ""



    if arg == 'object_inf':
        if 'ARG0' not in x and (self.detect_sub(text) and 'ARG1' in x) and len(keys) > 1:
            keys.remove('ARG1')

        if 'ARG0' in x:
            keys.remove('ARG0')

        if keys: return ", ".join(x[keys[0]])
        # if keys:
        #     return ", ".join([" ".join(x[k]) for k in keys])
        else: return ""

    if arg == 'aim_inf': return " ".join(x['V'])
    if arg == 'deontic_inf':
        if 'ARGM-MOD' in x and 'ARGM-NEG' in x:
            return " ".join([x['ARGM-MOD'][0], x['ARGM-NEG'][0]])
        elif 'ARGM-MOD' in x:
            return x['ARGM-MOD'][0]
        else:
            return ""

  # normalize the texts
  def normalize_text(self, s, col):
      """Removing articles and punctuation, and standardizing whitespace are all typical text processing steps."""

      def tokens(text, colname):
          doc= nlp(text)
          return ([word.lemma for sent in doc.sentences for word in sent.words if not word.text in all_words]) #exclude stop words

          # if colname in ['attribute','object']:
          #  return ([word.lemma for sent in doc.sentences for word in sent.words if not word.text in all_words]) #exclude stop words
          # else: ##verbs and modals may be stopwords so screening not applied for AIM/DEONTIC
          #  return ([word.lemma for sent in doc.sentences for word in sent.words])

      def remove_punc(text):
          exclude = set(string.punctuation)
          return "".join(ch for ch in text if ch not in exclude)

      def lower(text):
          return text.lower().strip()

      return tokens(remove_punc(lower(s)),col)

  def compute_exact_match(self,prediction, truth):
      return int(self.normalize_text(prediction) == self.normalize_text(truth))

  #F1 score computation
  def compute_f1(self,truth, prediction, col_name):
    pred_tokens = self.normalize_text(prediction, col_name)
    truth_tokens = self.normalize_text(truth, col_name)
    # print(pred_tokens,truth_tokens)

    # if either the prediction or the truth is no-answer then f1 = 1 if they agree, 0 otherwise
    if len(pred_tokens) == 0 or len(truth_tokens) == 0:
        return int(pred_tokens == truth_tokens)

    common_tokens = set(pred_tokens) & set(truth_tokens)

    # if there are no common tokens then f1 = 0
    if len(common_tokens) == 0:
        return 0

    prec = len(common_tokens) / len(pred_tokens)
    rec = len(common_tokens) / len(truth_tokens)

    return 2 * (prec * rec) / (prec + rec)

  def remove_outliers(self, data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    cleaned_data = [x for x in data if lower_bound <= x <= upper_bound]
    return cleaned_data

  def inference(self,file_name,out_path=None):
    if not out_path : out_path = file_name
    data = self.file_read(file_name)
    data.fillna('', inplace=True)


    # data.columns = map(str.lower, data.columns)

    ##exclude empty entries
    # data.dropna(subset=['raw institutional statement'],inplace=True)
    # data = data[(data['raw institutional statement'] != "")]

    #exclude from analysis if span not included in statement or span is abstractive
    if self.agent =='eval':
        # remove inferred coding
        for col_name in ['attribute', 'object', 'aim', 'deontic']:
            ##remove inferred coding re.sub("[\(\[].*?[\)\]]", "<skipped>",x)
            pattern = r'\[[^\]]*\]'

            #some preprocessing for aquaculture and national organic datasets (see paper appendix)
            if not self.fpc:
             data[col_name] = data[col_name].apply(lambda x: "<skipped>" if x.startswith('[') else x)
             data[col_name] = data[col_name].apply(lambda x: re.sub("[\(\[].*?[\)\]]", "", x))
             ##Look for whether annotation is span level (ABDICO value annotated is present in institutional statement)
             data[col_name] = data.apply(lambda x: "<skipped>" if x[col_name] and (
                    x[col_name] not in x['raw institutional statement']) else x[col_name], axis=1)

        # data['attribute'] = data.apply( lambda x : "<skipped>" if x.attribute and (x.attribute not in x['raw institutional statement']) else x.attribute, axis=1)
        # data['object'] = data.apply( lambda x : "<skipped>" if x.object and (x.object not in x['raw institutional statement']) else x.object, axis=1)

        #atleast Actor or object is span
        if not self.fpc:
            # data = data[(data['aim'] != '<skipped>')]
            # print("Dataset after removing abstractive aims: ", data.shape[0])
            print("Abstractive coding in one or more fields:", data[(data['attribute'] != '<skipped>') | (data['object'] != '<skipped>')
                        | (data['aim'] != '<skipped>') | (data['deontic'] != '<skipped>')].shape[0])

            # data = data[(data['attribute'] != '<skipped>') | (data['object'] != '<skipped>') | (data['aim'] != '<skipped>') | (data['deontic'] != '<skipped>')]

            #lemmatize aims
            # data.dropna(subset=['aim'],inplace=True)
            # print("Dataset after removing non-actionable statements [no Aim coded]: ", data.shape[0])

        data['aim'] = data['aim'].apply(lambda x: self.process_aim(x))

    #SRL inference
    for arg in ['attribute_inf','object_inf','aim_inf','deontic_inf']:
        data[arg] = data.apply(lambda x : self.argmatch(x.srl_parsed, x.sentences, arg),axis=1)


    data.to_csv(out_path,index=False)

  def srl_eval(self, store='/content/NLP4GOV/src/SRL/data'):
    column_names = ['attribute', 'object', 'deontic', 'aim']
    eval_scores = {name:[] for name in column_names}

    datasets = list(os.listdir(store))
    datasets.sort()
    # file_names = ['NationalOrganicProgramRegulations_Siddiki.xlsx - Econ Development Mechanisms.csv']

    for subdata in datasets:
        sub_path = os.path.join(store, subdata)
        if 'Food' in subdata: self.fpc = True
        else: self.fpc = False

        sets = []
        for file_name in os.listdir(sub_path):
            eval_name = os.path.join(store, subdata, file_name)
            temp = pd.read_csv(eval_name)
            temp.columns = map(str.lower, temp.columns)
            sets.append(temp) #[['raw institutional statement','attribute','deontic','aim','object']]

        df1 = pd.concat(sets)
        print(subdata, "Dataset: ", df1.shape[0])
        if not all(item in df1.columns for item in column_names):
            print("Please check if file(s) have ground truth ABDICO labels")
            return

        out_path = os.path.join('/content',f"{subdata}_data_new.csv")
        self.inference(df1, out_path)
        df1 = pd.read_csv(out_path)
        df1 = df1[['raw institutional statement','attribute','deontic','aim','object','attribute_inf','object_inf','aim_inf','deontic_inf']]


        df1.fillna('', inplace=True)
        df1 = df1.applymap(lambda x : x.lower().strip())

        # #also lemmatize predicted aims
        # df1['aim_inf'] = df1['aim_inf'].apply(lambda x: self.process_aim(x))


        for col_name in column_names:
            df = df1.copy()

            #exclude abstractive coding from evaluation 
            df = df[df[col_name] != '<skipped>']
            values1 = df[col_name].tolist()
            values2 = df[col_name + '_inf'].tolist()

            #do we need to compare missing entries?
            values1 = [str(x).replace('nan', '') for x in values1]
            values2 = [str(x).replace('nan', '') for x in values2]

            f1_score = []
            for x,y in zip(values1,values2):
                f1_score.append((self.compute_f1(x,y,col_name)))
                eval_scores[col_name].append(self.compute_f1(x,y,col_name))

            print(f" F1 score for {col_name}: {np.mean(f1_score)}")
        # df1.to_csv(out_path,index=False)

    for k, v in eval_scores.items():
        print(f"Mean F1 score for {k}: {np.mean(v)}")
    # Create a 2x2 subplot
    # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
    # for idx, col_name in enumerate(column_names):
    #     # eval_scores[col_name] = self.remove_outliers(eval_scores[col_name])
    #
    #     # Plot each boxplot in a different subplot
    #     row, col = int(idx/2),int(idx%2)
    #     axes[row, col].boxplot(eval_scores[col_name])
    #     axes[row, col].set_title(f"{col_name}")
    #
    # fig.suptitle("Span selection match (F1) across multiple datasets")
    # return plt

