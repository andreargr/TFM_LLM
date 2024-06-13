import pandas as pd #dataframe manipulation
from sklearn.model_selection import train_test_split #data division 
from openai import OpenAI #ChatGPT API
from dotenv import load_dotenv #environment control
import os #interact with the operating system
import json #use json data

mappings = pd.read_csv("biosamples.tsv", sep="\t") #data loading
mappings_train, mappings_test = train_test_split(mappings, test_size=0.25, random_state=17) #training/test data division

def get_formatted_data(data): #get the correct format for the fine-tuning
    formatted_data = []
    for row in data.itertuples(index=False):
        label = row[0]
        identifiers = list(row[1:5])
        formatted_data.append({
            "messages": [
                {"role": "system", "content": "You are going to assist me in a search of the identifiers of ontologies for a determined label."},
                {"role": "user", "content": f"For the label {label}, I need you to search the identifiers that better suit the label in the ontologies CLO, CL, UBERON and BTO."},
                {"role": "assistant", "content": str(identifiers)}
            ]
        })
    return formatted_data

def save_to_jsonl(dataset, file_path): #convert json to jsonl
    with open(file_path, 'w') as file:
        for ejemplo in dataset:
            json_line = json.dumps(ejemplo)
            file.write(json_line + '\n')

def jsonl_converter(mappings_train): #save the jsonl
  formatted_train = get_formatted_data(mappings_train)
  training_file_name = "formatted_train_pruebas2.jsonl"
  save_to_jsonl(formatted_train, training_file_name)

def load_environment():  #get the api key for openai
    load_dotenv()
    return os.environ.get("OPENAI_API_KEY")

def prepare_data_ft(): #upload training file to openai
  api_key=load_environment()
  client = OpenAI(api_key=api_key)
  
  training_file_id = client.files.create(
  file=open("formatted_train.jsonl", "rb"),
  purpose="fine-tune")
  
  print(f"Training File ID: {training_file_id}")
  return client,training_file_id

def create_job(): #create the fine-tuning job
  client,training_file_id = prepare_data_ft()
  response = client.fine_tuning.jobs.create(
    training_file=training_file_id.id, 
    model="gpt-3.5-turbo", 
    suffix='ft1',
    hyperparameters={
      "n_epochs": 15,
    "batch_size": 3,
    "learning_rate_multiplier": 0.3
    }
  )
  job_id = response.id
  status = response.status
  print(f'Fine-tunning model with jobID: {job_id}.')
  print(f"Training Response: {response}")
  print(f"Training Status: {status}")

if __name__ == "__main__":
    jsonl_converter(mappings_train)
    create_job()