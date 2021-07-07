import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import telebot # Importamos las librería
TOKEN ='1807736786:AAF-3ojW8KBq-S5SvIt65lc3SipXV96MoOY' # Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN)  #Creamos nuestra instancia "bot" a partir de ese TOKEN
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


import credentials
import tweepy
import random

auth = tweepy.OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
def tweepy(message):
    

    id = None
    count = 0
    lista_topics=[]
    while count <= 20:
    	tweets = api.search(q=message, lang='es', tweet_mode='extended', max_id=id)
    	for tweet in tweets:
            if tweet.full_text.startswith('RT'):
            	count += 1
            	continue
            lista_topics.append(tweet.full_text)
            f = open('./holamundo.txt', 'a', encoding='utf-8')
            f.write(tweet.full_text + '\n')
            f.close
            count += 1
    	id = tweet.id
    	print(count)
    return lista_topics[random.randrange(10)]
#Creating GUI with tkinter
#import tkinter
#from tkinter import *


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res
@bot.message_handler(commands=['buscar', 'help'])
def send_welcome(message):
    print(message)
    bot.message_handler(func=lambda message: True) 
    bot.reply_to(message,tweepy(message.text))
@bot.message_handler(func=lambda message: True)    
def conversabot(message):
    bot.reply_to(message,chatbot_response(message.text))

bot.polling()
user = bot.get_me()
print(user)

#Es equivalente a esto 
#https://api.telegram.org/bot<TU_TOKEN>/getMe
# Saber información de los grupos del Bot
updates = bot.get_updates()
print(updates)
#Es equivalente a esto 
#https://api.telegram.org/bot<TU_TOKEN/getUpdates

#def send():
    #msg = EntryBox.get("1.0",'end-1c').strip()
    #EntryBox.delete("0.0",END)

    #if msg != '':
        #ChatLog.config(state=NORMAL)
        #ChatLog.insert(END, "You: " + msg + '\n\n')
        #ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        #res = chatbot_response(msg)
        #ChatLog.insert(END, "Bot: " + res + '\n\n')
            
        #ChatLog.config(state=DISABLED)
        #ChatLog.yview(END)
 

#base = Tk()
#base.title("Hello")
#base.geometry("400x500")
#base.resizable(width=FALSE, height=FALSE)

#Create Chat window
#ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

#ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
#scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
#ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
#SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    #bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    #command= send )

#Create the box to enter message
#EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
#scrollbar.place(x=376,y=6, height=386)
#ChatLog.place(x=6,y=6, height=386, width=370)
#EntryBox.place(x=128, y=401, height=90, width=265)
#SendButton.place(x=6, y=401, height=90)

#base.mainloop()
