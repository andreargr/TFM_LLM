import json #use json data
import pandas as pd #dataframe manipulation 

from get_response_ft import add_new_row
from creation_ft import mappings_test


def process_json_results(file_path): #convert the result.json to a dataframe
    # Read and load the JSON file
    with open(file_path, 'r') as archivo:
        results_modelft = json.load(archivo)

    l_l = []
    # Process data from the JSON file
    for label, identifiers in results_modelft.items():
        list_elements = identifiers.strip('][').split(', ')  # Convert to list
        list_elements = [element.strip("'") for element in list_elements]
        list_elements.insert(0, label)
        l_l.append(list_elements)
    
    l_l_filtered = [sublist for sublist in l_l if len(sublist) == 5] #check the correct format
    
    mappings_model = pd.DataFrame(l_l_filtered,columns=["Label", "CLO_M", "CL_M", "UBERON_M", "BTO_M"])
    
    model_error = [sublist for sublist in l_l if len(sublist) != 5]
    
    print('Total of correct data outputs:', len(mappings_model))
    print('The following number of model outputs do not meet the required format:', len(model_error))
    return mappings_model

def get_df_comparation(path): #obtain a unique data frame for comparing reference identifiers and model identifiers.
    mappings_model = process_json_results(path) #obtain model mappings dataframe
    mappings_control = add_new_row(mappings_test) #obtain reference mappings dataframe

    df_comparation = pd.merge(mappings_model, mappings_control, on='Label', how='inner') #merge both dataframes
    orden_columnas= ["Label","Type","CLO_C", "CLO_M","CL_C","CL_M","UBERON_C", "UBERON_M","BTO_C","BTO_M"]
    df_comparation = df_comparation[orden_columnas]

    for columna in df_comparation:
        df_comparation[columna] = df_comparation[columna].fillna('unknown') #replace na values with the string 'unknown'
    return df_comparation

df_comparation_ft= get_df_comparation('results_ft.json')
df_comparation_gpt3_5= get_df_comparation('results_gpt3_5.json')
df_comparation_gpt4= get_df_comparation('results_gpt4.json')


