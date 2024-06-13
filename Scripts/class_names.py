import requests #send HTTP requests
import json #use json data

from df_comparation import df_comparation_ft

def group_and_return_dfs(df): # Group the dataframe by the 'Type' column and create a dataframe for each group
    dfs = {}
    for group_name, group_df in df.groupby('Type'):
        dfs[group_name] = group_df
    return dfs

dfs = group_and_return_dfs(df_comparation_ft)

df_CL = dfs['CL']  # DataFrame where Type is 'CL'
df_CT = dfs['CT']  # DataFrame where Type is 'CT'
df_A = dfs['A']    # DataFrame where Type is 'A'
df_dash = dfs['-']    # DataFrame where Type is '-'

def get_class_name(ontology_acronym,class_id): #get class name for each identifier
    url = f'http://data.bioontology.org/ontologies/{ontology_acronym}/classes/{class_id}'
    api_key = "3a884577-7cac-4830-b241-61cbe4ebf5d4"
    headers = {
        'Authorization': f'apikey token={api_key}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        class_name = data.get('prefLabel')  # or another key based on the structure
        print("Class Name:", class_name)
        return class_name
    else:
        print("Failed to retrieve data:", response.status_code, class_id)

def get_classes(df):
    dicc_clases={}
    for label,identifiers in df.items():      
        for element in identifiers:
            element_formatted=element.replace("_",":") #change underscore for a colon
            if element_formatted.startswith("CL:"):
                class_name=get_class_name("CL",element_formatted)
            elif element_formatted.startswith("CLO:"):
                class_name=get_class_name("CLO",element_formatted)
            elif element_formatted.startswith("UBERON:"):
                class_name=get_class_name("UBERON",element_formatted)
            elif element_formatted.startswith("BTO:"):
                class_name=get_class_name("BTO",element_formatted)
            else:
                class_name="-"
            if label in dicc_clases:
                dicc_clases[label].append(class_name)
            else:
                dicc_clases[label]=[class_name]
    return dicc_clases

def df_to_dicc(df): #convert DataFrame to dictionary
    dicc={}
    for index,row in df.iterrows():
        label = row['Label']
        identifiers = row[2:].tolist()
        dicc[label]=identifiers
    return dicc

def get_class_names(df,type): #get the classes and save the output in JSON format
    dicc_df = df_to_dicc(df)
    print(dicc_df)
    dicc_clases = get_classes(dicc_df)
    file_name = f'classnames_{type}.json'
    with open(file_name, 'w') as archivo_json:
        json.dump(dicc_clases, archivo_json, indent=4) 


# get_class_names(df_A,'A')
# get_class_names(df_CL,'CL')
# get_class_names(df_CT,'CT')



