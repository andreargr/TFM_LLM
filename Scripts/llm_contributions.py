import json #use json data
import pandas as pd #dataframe manipulation

from pattern_analysis import df_to_dicc 

def data_process(filename): #convert json to a dataframe
    with open(filename, 'r') as archivo:
        dicc_clases = json.load(archivo)
    df = pd.DataFrame.from_dict(dicc_clases, orient='index')
    nueva_fila = pd.DataFrame([df.columns], columns=df.columns)
    df_process = pd.concat([nueva_fila, df], ignore_index=True)
    df_process.columns = ['CLO_C','CLO_M', 'CL_C','CL_M', 'UBERON_C','UBERON_M','BTO_C','BTO_M']
    df_process = df_process.drop(0)

    claves=[]
    for clave in dicc_clases.keys():
        claves.append(clave)
    df_process['Label'] = claves #add label column
    
    df_process.fillna("", inplace=True) #replace 'Nonetype' values

    return df_process


def contribution(type): #obtain contribution of llm for each ontology
    if type == 'CL':
        df = data_process('pattern_file_CL.json')
        suffixes = ['CLO', 'CL', 'UBERON', 'BTO']
    elif type == 'CT':
        df = data_process('pattern_file_CT.json')
        suffixes = ['CL', 'UBERON', 'BTO']
    elif type == 'A':
        df = data_process('pattern_file_A.json')
        suffixes = ['UBERON', 'BTO']
    else:
        raise ValueError("Tipo no reconocido")

    for suffix in suffixes:
        true_col = f'{suffix}_C'
        pred_col = f'{suffix}_M'
        for index,row in df.iterrows():
            ref=row[true_col]
            pred = row[pred_col]
            if ref == '-' and pred != '-':
                print(index,suffix,row) 
                check = input('Is the contribution valid? Y/N \n')
                if check == 'Y':
                    df.at[index, true_col] = pred
    dicc = df_to_dicc(df)
    file_name = f'contribution_file_{type}.json'
    with open(file_name, 'w') as archivo_json:
        json.dump(dicc, archivo_json, indent=4)
    return 

contribution('A')
#contribution('CT')
#contribution('CL')

