import json #use json data
import pandas as pd #dataframe manipulation 

count=0 #get the count of related identifiers
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

def buscar_subcadenas_comunes(string1, string2): #search the pattern between strings
    longitud = min(len(string1), len(string2))
    for i in range(longitud, 0, -1):
        for j in range(len(string1) - i + 1):
            if string1[j:j+i] in string2:
                return string1[j:j+i]
    return ""

def comprobar_patron(df,index,columna,patron,string1,string2): #check if pattern is valid
    global count 
    print(columna)
    if len(patron) > 4 and patron != ' cell' and patron != ' of ':
        print(index,'The similarity between',string1,'-',string2,':',patron, len(patron))
        check = input('Is the pattern valid? Y/N \n')
        if check == 'Y':
            df.at[index, columna] = string1
            count +=1
    return df

def df_to_dicc(df): #convert DataFrame to dictionary
    dicc={}
    for index,row in df.iterrows():
        label = row['Label']
        identifiers = row[:8].tolist()
        dicc[label]=identifiers
    return dicc

def pattern_process(type): 
    if type == 'CL': #only ontologies of interest are considered
        df = data_process('classnames_CL.json')
        col_1 = 'CLO'
        col_2 = 'BTO'
    elif type == 'CT':
        df = data_process('classnames_CT.json')
        col_1 = 'CL'
        col_2 = 'BTO'
    elif type == 'A':
        df = data_process('classnames_A.json')
        col_1 = 'UBERON'
        col_2 = 'BTO'
    else:
        raise ValueError("Tipo no reconocido")

    control_1= f'{col_1}_C'
    control_2= f'{col_2}_C'
    prueba_1= f'{col_1}_M'
    prueba_2= f'{col_2}_M'  

    for index, row in df.iterrows():
        string1a = row[control_1]
        string2a = row[prueba_1]
        if string1a != string2a:
            patron = buscar_subcadenas_comunes(string1a,string2a)
            pattern_df = comprobar_patron(df,index,prueba_1,patron,string1a,string2a)
    
    for index, row in pattern_df.iterrows():
        string1b = row[control_2]
        string2b = row[prueba_2]
        if string1b != string2b:
            patron = buscar_subcadenas_comunes(string1b,string2b)
            pattern2_df =comprobar_patron(pattern_df,index,prueba_2,patron,string1b,string2b)
    dicc = df_to_dicc(pattern2_df)
    file_name = f'pattern_file_{type}.json'
    with open(file_name, 'w') as archivo_json:
        json.dump(dicc, archivo_json, indent=4)


#pattern_process('A')
#pattern_process('CL')
# pattern_process('CT')
print("El patrón fue válido", count, "veces.")