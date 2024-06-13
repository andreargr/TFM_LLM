import pandas as pd #dataframe manipulation 
from openai import OpenAI #ChatGPT API
from dotenv import load_dotenv #environment control
import os #interact with the operating system
import json #use json data

from creation_ft import mappings_test #get test data from previous script

def add_new_row(df): #set columns names
    new_row = pd.DataFrame([df.columns], columns=df.columns)
    df = pd.concat([new_row, df], ignore_index=True)
    df.columns = ['Label', 'CLO_C', 'CL_C', 'UBERON_C', 'BTO_C', 'Type']
    return df

def load_environment(): #get the api key from .env
    load_dotenv()
    return os.environ.get("OPENAI_API_KEY")

def get_openai_response(df): #get the output from the model
    api_key = load_environment()
    client = OpenAI(api_key=api_key)
    dicc = {}
    for index, row in df.iterrows():
        label = row['Label']
        completion = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:ontogenix:ft1:9AaMtCVw", #fine-tuning model
            messages=[
                {"role": "system", "content": "You are going to assist me in a search of the identifiers of ontologies for a determined label."},
                {"role": "user", "content": f"For the label {label}, I need you to search the identifiers that better suit the label in the ontologies CLO, CL, UBERON, and BTO."}
            ]
        )
        out = completion.choices[0].message.content
    
        dicc[label] = out
    return dicc

def save_results(results): #save the output in JSON format
    with open('results_ft.json', 'w') as archivo_json:
        json.dump(results, archivo_json, indent=4)

def main():
    mappings_test_updated = add_new_row(mappings_test)
    results = get_openai_response(mappings_test_updated)
    save_results(results)

if __name__ == "__main__":
    main()
