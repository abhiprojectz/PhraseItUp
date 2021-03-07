from flask import jsonify
from flask import Flask, render_template, url_for, request, redirect
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from random import randint
import nltk.data
from nltk.tokenize import sent_tokenize


app = Flask(__name__)


# paraphrase main function
def paraphrase(text):
    output = ""

    # Load the pretrained neural net
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    # Tokenize the text
    tokenized = tokenizer.tokenize(text)

    # Get the list of words from the entire text
    words = word_tokenize(text)

    # Identify the parts of speech
    tagged = nltk.pos_tag(words)


    for i in range(0,len(words)):
        replacements = []

        for syn in wordnet.synsets(words[i]):

            if tagged[i][1] == 'NNP' or tagged[i][1] == 'DT':
                break
            
            word_type = tagged[i][1][0].lower()
            if syn.name().find("."+word_type+"."):
                # extract the word only
                r = syn.name()[0:syn.name().find(".")]
                replacements.append(r)

        if len(replacements) > 0:
            # Choose a random replacement
            replacement = replacements[randint(0,len(replacements)-1)]
            output = output + " " + replacement
        else:
            output = output + " " + words[i]
       
    return output    



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/phrase', methods=['POST'])
def phrase():

    sen = request.get_json()
    print(sen['data'])
    pem = sen['data']
    text = paraphrase(pem)
    ata = {'name':text}
    return jsonify(ata)



if __name__ == '__main__':
   app.run(debug=True)