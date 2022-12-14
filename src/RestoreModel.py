# -*- coding: utf-8 -*-
"""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XwFqESd-FED09TdXD8lcZkwYLAZ12j4M
"""
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
import string
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Input
from keras.models import Model, load_model

def encode_vars(expr):
  """ Function to map variables to a smaller set of alphabets """
  chars = string.ascii_lowercase
  d = dict()
  expr_list = list(expr)
  j = 0
  for i in range(len(expr)): 
    if expr[i].isalpha():
      if expr[i] not in d:
        d[expr[i]] = chars[j]
        j += 1
      expr_list[i] = d[expr[i]]

  return "".join(expr_list)

def decode_vars(out, inp):
  """ Function to map variables back acc. to input """
  d = dict()
  op = {'-':' -> ','^':'^','|':'v','~':'~'}
  alpha = [a for a in inp if a.isalpha()]
  j = 0
  l = list()
  
  for ch in out:
    
    if ch.isalpha(): # mapping back operand alphabets 
      if ch not in d:
        d[ch] = alpha[j]
        j += 1
      ch = d[ch]
    
    elif ch in op: 
      ch = op[ch]
 
    l.append(ch)
  
  return " ".join(l)

def dataset(path):
  """ Function to read the dataset and preprocess it """

  df = pd.read_csv(path) # read csv file 
  # print(df.columns)
  # input and output columns
  X = df["X"]
  y = df["post"]
  
  # preprocessing the output column 
  y = y.apply(lambda x:'(' + x +')')
  y = y.apply(lambda x: x.replace(' ', ''))
  y = y.apply(lambda x: x.replace('[', ''))
  y = y.apply(lambda x: x.replace(']', ''))
  y = y.apply(lambda x: encode_vars(x))

  X = X.apply(lambda x: encode_vars(x))

  # for i in range(10):
  #   print(X[i],y[i])
  
  # obtaining encoded inputs and outputs
  X_new = []
  y_new = []
  for i in range(len(X)):
    X_new.append(list(X[i]))
    y_new.append(list(y[i]))

  # print("Input output example: ", X_new[0], ",", y_new[0])

  return (X_new, y_new)

def generate_batch(X, y, batch_size = 64):
  """ Creates and returns a generator object on the train data """    
  while True:
        for j in range(0, len(X), batch_size):
            encoder_input_data = np.zeros((batch_size, max_length_src), dtype='float32')
            decoder_input_data = np.zeros((batch_size, max_length_tar), dtype='float32')
            decoder_target_data = np.zeros((batch_size, max_length_tar, num_decoder_tokens), dtype='float32')
            
            for i, (input_text, target_text) in enumerate(zip(X[j:j+batch_size], y[j:j+batch_size])):
                
                for t, ch in enumerate(input_text):
                    encoder_input_data[i, t] = input_token_index[ch] # encoder input seq
                
                for t, ch in enumerate(target_text):
                   
                    if t < len(target_text) - 1:
                        try:
                            decoder_input_data[i, t] = target_token_index[ch] # decoder input seq
                        except: 
                            print("!!! Error here", target_text, input_text, ord(ch), j * batch_size + i)
                            
                    if t>0:
                        # decoder target sequence (one hot encoded)
                        # does not include the START_ token
                        # Offset by one timestep
                        decoder_target_data[i, t - 1, target_token_index[ch]] = 1

            yield([encoder_input_data, decoder_input_data], decoder_target_data)

def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)    
    
    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1,1))
    
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0] = target_token_index['(']
    
    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)
        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence +=sampled_char
        
        # Exit condition: either hit max length or find stop token.
        if (sampled_char == ')' or len(decoded_sentence) >16 ):
            stop_condition = True
        
        # Update the target sequence (of length 1).
        target_seq = np.zeros((1,1))
        target_seq[0, 0] = sampled_token_index
        
        # Update states
        states_value = [h, c]
    decoded_sentence=decoded_sentence.replace(")","").replace("(","")
    
    return decoded_sentence

'''
# To read a dataset from Gdrive using Google Collab, use the below commands:

from google.colab import drive
drive.mount("/content/drive")

'''
path = "dataset.csv"
model_path = "model.h5"

X_new, y_new = dataset(path)
# input characters 
inpchars = list(string.ascii_lowercase)
inpchars.extend(['|','-','~','^'])

# output characters 
outchars = inpchars.copy()
outchars.extend(['(',')'])

  # Max Length of source sequence
lenght_list=[]
for l in X_new:
    lenght_list.append(len(l))
max_length_src = np.max(lenght_list)
#print("Source max length: ", max_length_src)

# Max Length of target sequence
lenght_list=[]
for l in y_new:
    lenght_list.append(len(l))
max_length_tar = np.max(lenght_list)

#print("Target max length: ", max_length_tar)
input_words = inpchars
target_words = outchars

# Calculate Vocab size for both source and target
num_encoder_tokens = len(inpchars)
num_decoder_tokens = len(outchars)
num_decoder_tokens += 1 # For zero padding
#print("Input vocabulary Size:", num_encoder_tokens)
#print("Target vocabulary Size:", num_decoder_tokens)

# Create word to token dictionary for both source and target
input_token_index = dict([(word, i+1) for i, word in enumerate(input_words)])
target_token_index = dict([(word, i+1) for i, word in enumerate(target_words)])

# Create token to word dictionary for both source and target
reverse_input_char_index = dict((i, word) for word, i in input_token_index.items())
reverse_target_char_index = dict((i, word) for word, i in target_token_index.items())

# ----------------------------------------------LOADING MODEL -----------------------------------
# Restore the model and construct the encoder and decoder.
model = load_model(model_path)
#model.summary()
latent_dim=20
encoder_inputs = model.input[0]   # input_1
encoder_outputs, state_h_enc, state_c_enc = model.layers[4].output   # lstm_1
encoder_states = [state_h_enc, state_c_enc]
encoder_model = Model(encoder_inputs, encoder_states)


# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the
# return states in the training model, but we will use them in inference.

decoder_inputs = model.input[1]   # input_2
dec_emb_layer = model.layers[3]
dec_emb = dec_emb_layer(decoder_inputs)

decoder_state_input_h = Input(shape=(latent_dim,), name='input_3')
decoder_state_input_c = Input(shape=(latent_dim,), name='input_4')
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_lstm = model.layers[5]


decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
      dec_emb, initial_state=decoder_states_inputs)
decoder_states = [state_h_dec, state_c_dec]
decoder_dense = model.layers[6]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
       [decoder_inputs] + decoder_states_inputs,
       [decoder_outputs] + decoder_states)

# -------------------------------------------------------- USER INPUT ---------------------------------------------------
def predict_postfix(infix):
  #print("Input: ",infix)
  inp = encode_vars(infix)
  inp_list = list(inp.replace(' ','').replace('->','-'))
  
  for i in range(len(inp_list)):
    inp_list[i] = input_token_index[inp_list[i]]

  output = decode_sequence([inp_list])
  final = decode_vars(output, infix)
  #print("Output (postfix notation): ", final)
  
  return final

def user_input(infix):
  # preprocess the input string
  
  #print("Input: ", infix)
  infix = infix.replace("->","-")
  d = {'&': '^', '-':'-', 'v':'|','!':'~'}
  input = ""  
  for char in infix: 
    if char in d:
      input += d[char]
    else:
      input += char
  return predict_postfix(input)



f1 = open('data.pkl', 'rb')
model_input = pickle.load(f1)
f1.close()
print()
print("model_input : " , model_input)

conditionals , questions = model_input
conditionals_postfix = []
questions_postfix = []

print("Conditionals ")
for exp in conditionals:
  print("Input: ", exp)
  ans = user_input(exp)
  print("Output (postfix notation): ", ans)
  conditionals_postfix.append( ans )

print()
print("Questions")
for exp in questions:
  print("Input: ", exp)
  ans = user_input(exp)
  print("Output (postfix notation): ", ans)
  questions_postfix.append( ans )

model_output = [conditionals_postfix, questions_postfix]

f2 = open('data.pkl', 'wb')
pickle.dump(model_output, f2)
f2.close()