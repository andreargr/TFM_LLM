import pandas as pd #dataframe manipulation 
from openai import OpenAI #ChatGPT API
from dotenv import load_dotenv #environment control
import os #interact with the operating system
import json #use json data

from creation_ft import mappings_test #get test data from previous script

def add_new_row(df): #set columns names
    new_row = pd.DataFrame([df.columns], columns=df.columns)
    df = pd.concat([new_row, df], ignore_index=True)
    df.columns = ['Label', 'CLO', 'CL', 'UBERON', 'BTO', '']
    return df

def load_environment(): #get the api key from .env
    load_dotenv()
    return os.environ.get("OPENAI_API_KEY")

def read_prompt_file(file_path): #read the prompt file
    with open(file_path, 'r') as file:
        return file.read()

def format_prompt(prompt, label): #format the prompt file with the desired label
    return prompt.format(label=label)

def get_openai_response(df,model): #get the output from the model
    api_key=load_environment()
    client = OpenAI(api_key=api_key)
    dicc = {}
    for index,row in df.iterrows():
        label= row[0]
        prompt = read_prompt_file('prompt_search_id.txt')
        f_prompt = format_prompt(prompt,label)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are going to assist me in a search of the identifiers of ontologies for a determined label."},
                {"role": "user", "content": f_prompt }
            ]
        )
        out=completion.choices[0].message.content
        if label in dicc.keys():
            dicc[label].append(out)
        else:
            dicc[label]= out
    return dicc

def save_results(results,name): #save the output in JSON format
    with open(name, 'w') as archivo_json:
        json.dump(results, archivo_json, indent=4)

def main():
    mappings_test_updated = add_new_row(mappings_test)
    results_3_5 = get_openai_response(mappings_test_updated,"gpt-3.5-turbo-0125")
    results_4 = get_openai_response(mappings_test_updated,"gpt-4-turbo")
    save_results(results_3_5,'results__gpt3_5.json')
    save_results(results_4,'results__gpt4.json')

if __name__ == "__main__":
    main()

