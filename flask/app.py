import re
from click import prompt
from flask import Flask, render_template, request
import os
import openai
import requests

openai.api_key = "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"

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)

app.register_error_handler(404, page_not_found)



@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == 'POST':
        query = request.form['text']
        promptxt=("{}").format(query)
        print(promptxt)
        response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=promptxt,
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        )
        resp=response['choices'][0]['text']
        print(resp)
        split_string = resp.split("\n", 1)
        string1 = split_string[0]
        

    return render_template('index.html', **locals())


@app.route('/bugfix', methods=["GET", "POST"])
def bugfix():
    if request.method == 'POST':
            query = request.form['codefix']
            codetxt="""
            ##### Fix bugs in the below function
        
            ### Buggy Python
            {}
            ### Fixed Python
            """.format(query)

            response = openai.Completion.create(
            engine="davinci-codex",
            prompt=codetxt,
            temperature=0,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["###"]
            )
            print(response['choices'][0]['text'])

            openAIAnswer = response['choices'][0]['text']


    return render_template('bugfix.html', **locals())

@app.route('/codexp', methods=["GET", "POST"])
def codexp():
    if request.method == 'POST':
        query = request.form['codexp']
        codetxt="# Python 3 \n {} \n\n# Explanation of what the code does\n\n#".format(query)


        response = openai.Completion.create(
        engine="davinci-codex",
        prompt=codetxt,
        temperature=0,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#"]
        )
        print(response['choices'][0]['text'])
        

        print(query)
        openAIAnswer = response['choices'][0]['text']

    return render_template('codexp.html', **locals())

@app.route('/essayoutline', methods=["GET", "POST"])
def essayoutline():

    if request.method == 'POST':
        query = request.form['text']
        promptxt=("{} :\n\nI:").format(query)
        print(promptxt)
        response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=promptxt,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n\n"]
        )
        resp=response['choices'][0]['text']
        print(resp)
        split_string = resp.split("\n", 1)
        string1 = split_string[0]
        

    return render_template('essayoutline.html', **locals())


@app.route('/spreadsheet', methods=["GET", "POST"])
def spreadsheet():

    if request.method == 'POST':
        query = request.form['text']
        query1 = request.form['release']
        promptxt=("""
{}
                  
                  
{}
                  
                  
                  """).format(query,query1)
        print(promptxt)
        response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=promptxt,
        temperature=0.5,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n\n"]
        )
        resp=response['choices'][0]['text']
        print(resp)
        split_string = resp.split("\n", 1)
        string1 = split_string[0]
        

    return render_template('spreadsheet.html', **locals())

@app.route('/codegen', methods=["GET", "POST"])
def codegen():

    if request.method == 'POST':
        query = request.form['text']
        promptxt="""
--
Q: Write a Python program that calculates the sum of all positive integers smaller than 8.
A: sum(x for x in range(8))
--
Q: {}
A:
""".format(query)
        response = requests.post(
            "https://api.ai21.com/studio/v1/j1-jumbo/complete", # models- j1-large, j1-jumbo
            headers={"Authorization": "Bearer tADwpGNrHnbOtI8OhPPmzyZxiOwrXGsx "},
            json={
                "prompt": promptxt, 
                "numResults": 1, 
                "maxTokens": 200, 
                "stopSequences": ["--"], #where it should it end
                "topKReturn": 0,
                "temperature": 0.0
            }
        )
        resp=response.json()
        ans=resp['completions'][0]['data']['text']
        print(ans)
                

    return render_template('codegen.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


