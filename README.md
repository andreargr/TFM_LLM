# TFM - Application of Large Language Models to automate the processes of semantic integration of biological data.
Code used in the method and results obtained for the implementation of LLMs in semantics integration of biological data, specifically, OpenAI's GPT-3.5-turbo and GPT-4 models are used. In addition, an adjusted model was developed by performing a fine-tuning process on the GPT-3.5-turbo model. This project is developed as the Final Master's Degree Project at the University of Murcia during the academic year 2023/2024.

## Scripts
Scripts use one or more of the following libraries:
- **creation_ft.py**: Split data into a training set and a test set. Uploading data to OpenAI through its API and launching the fine-tuning job on the OpenAI GPT-3.5-turbo model.
- **get_response_modelsOpenAI.py**: Obtain the response of the models of OpenAI for a given task. In this case, the model is asked to display suitable identifiers for each of the ontologies under study for each label of interest.
- **get_response_ft.py**: The same as in the previous script, but using the previously built tuned model.
- **df_comparation-py**: Data manipulation and organization in order to compare the mappings proposed by the model and the reference mappings.
- **models_comparation.py**: Obtain the accuracy of each one of the models for each of the ontologies under study.
- **class_names.py**: Split data by label type and get the name of each identifier to analyze how the tuned model works.
- **pattern_analysis.py**: Look for a common pattern between the identifier class names and check if there is a valid relationship between them.
- **llm_contributions.py**: Filter out those cases where there is no reference identifier for a given tag but the model can propose a valid identifier.
- **match_analysis_accu.py**: Obtain tuned model accuracy for each of the ontologies by label type.
- **match_analysis_exhaust_f1.py**: Obtain tuned model exhaustiveness and F1-score for each one of the ontologies by label type.

## Dependencies
- **dotenv**: Read key-value pairs from a .env file and set them as environment variables
- **openai**: The OpenAI Python library provides convenient access to the OpenAI REST API from any Python 3.7+ application
- **sklearn.model_selection**: Tools for model selection, such as cross validation and hyper-parameter tuning.
- **json**: Work with JSON data
- **pandas**: Analysis and manipulation tool
- **os**: Provides a portable way of using operating system dependent functionality
- **matplotlib.pyplot**: Low level graph plotting library in python that serves as a visualization utility.
- **requests**: Allows you to send HTTP requests using Python

## Starting file
The starting file has the reference mappings made manually by the research group of the Computer Science and Systems Department of the University of Murcia.
- **biosamples.tsv**
