import streamlit as st
import datetime
from datetime import date
import pandas as pd
import joblib
import requests
import json
import argparse
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import os
import seaborn as sns
import csv
import io, base64
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from lightgbm import LGBMClassifier
from dotenv import load_dotenv


load_dotenv()
# streamlit_url = os.environ.get('streamlit_url')

def main():
    st.title('Streamlit Dashboard')
    st.write('Welcome to my Streamlit Dashboard!')

if __name__ == "__main__":
    main()












'''
# ----------------------------------------------------
# Définition des fonctions

def get_days(date_value):
    today = date.today()
    delta = today - date_value
    return delta.days


def get_age(date_value):
    today = date.today()
    delta = today - date_value
    return delta.days / 365

# ----------------------------------------------------
# Chargement des variables environnementales

# Localhost, load the .env file 
load_dotenv()  # 'http://127.0.0.1:5000/api/'

# Heroku path
urlPath = os.environ.get('urlPath')  # 'http://credit-scoring-app-mdln.herokuapp.com/api/'  
    

# ----------------------------------------------------
# Building the streamlit app
# Documentation >> st.help(st.form)
# ----------------------------------------------------

def main():
    # Titre de l'application
    st.title("Simulateur de Prêt")

    tab1, tab2, tab3 = st.tabs(["Informations Client", "Performance Globale", "Tendances clients"])
    with tab1:  # ID client + resultats après réponse de l'API
        
        # Création d'un formulaire
        with st.form("Formulaire Credit Scoring", clear_on_submit=True):
            uff, col, buff2 = st.columns([1,3,1])
            
            # (SK_ID_CURR) Numéro client
            sk_id_curr = col.text_input('Entrez un numéro de client')

            submit = st.form_submit_button(label="Envoyer")

            try:
                # If submit button is pressed
                if submit:
                                
                    # app.py
                    # URL = "https://credit-scoring-app-mdln.herokuapp.com/api/predict"
                    URL = os.path.join(urlPath, "predict")

                    # Définition d'un dictionnaire de paramètres pour les paramètres à envoyer à l'API
                    PARAMS = {
                        "sk_id_curr": sk_id_curr
                            }
                    
                    # calcul du score client
                    # print(PARAMS)
                    # sending get request and saving the response as response object
                    r = requests.get(url=URL, params=PARAMS)
                    # extracting data in json format
                    
                    # Initialisation des dictionnaires devant contenir les informations du client
                    other_client_info = {}  # Dictionnaire devant contenir les autres informations du client
                    information_options = {}  # Dictionnaire devant contenir les informations du client sélectionnées par l'utilisateur

                    if r.status_code == 200:
                        try:
                            response = r.json()
                            print(f'\n \n \n **** \nRéponse de la requete r.json() :  \n{response}')

                            # Score du client
                            label = response['data']  # le score du client est retourné dans la variable label 
                            print(f'\n \n **** \nVariable label contenant les scores du client : {label}')
                            label2 = (label['score_1'], label['score_2'])
                            print(f'\nVariable label2 : {label2}')  
                            
                            other_client_info = response['other_data']  # Dictionnaire contenant les autres informations du client
                            # Creation d'un dataframe contenant les autres informations du client
                            df_client = pd.DataFrame.from_dict(other_client_info, orient='index', dtype='string')
                            print(f'\n \n \n **** \nDataframe df_client : \n{df_client}')

                            print(f'\n \n \n **** \nInfo de df_client : \n{df_client.info(verbose=True)}')

                            df_client = df_client.rename(columns={0: 'Valeur', 1: 'Description'})
                            # df_client['Valeur'] = df_client['Valeur'].astype(int)
                            df_client = df_client.transpose()
                            df_client_02 = df_client.drop(df_client.index[1])  # Suppression de la ligne 'Description'
                            print(f'\n \n \n **** \nDataframe df_client_02 : \n{df_client_02}')

                            df_client_02['FLAG_OWN_CAR'] = df_client_02['FLAG_OWN_CAR'].apply(lambda x: 'Oui' 
                                                                                            if x == 1 
                                                                                            else 'Non')
                            df_client_02['CODE_GENDER'] = df_client_02['CODE_GENDER'].apply(lambda x: 'Homme' 
                                                                                            if x == 1 
                                                                                            else 'Femme')
                            df_client_02['NAME_FAMILY_STATUS_Married'] = df_client_02['NAME_FAMILY_STATUS_Married'].apply(
                                                                                            lambda x: 'Oui' 
                                                                                            if x == 1 
                                                                                            else 'Non')
                            df_client_02['NAME_EDUCATION_TYPE_Secondary / secondary special'] = df_client_02['NAME_EDUCATION_TYPE_Secondary / secondary special'].apply(
                                                                                            lambda x: 'Oui'
                                                                                            if x == 1
                                                                                            else 'Non')                       

                            print((f"check the data type of the values inside the 'DAYS_BIRTH' : {df_client_02['DAYS_BIRTH'].dtypes}"))
                            
                            row_to_copy = df_client.iloc[1]  # index_of_row_to_copy =  1: 'Description'
                            df_client_02 = df_client_02.append(row_to_copy)  # Ajout de la ligne 'Description' en bas du dataframe
                            # df_client_02 = df_client_02.reset_index(drop=True)  # Réinitialisation de l'index du dataframe
                            df_client = df_client_02.transpose()
                            
                            print(f'\n \n \n **** \nDictionnaire contenant other_client_info : \n{other_client_info}')
                            print(f'\n \n \n **** \nInfo de df_client : \n{df_client.info(verbose=True)}')
                            
                        except json.JSONDecodeError:
                            print("Error parsing JSON")
                    else:
                        print(f"Request failed with status code {r.status_code}")

                    # ----------------------------------------------------
                    # Affichage des résultats de la requête API
                        
                    if submit:                  

                        st.header("Informations client")
                        # Customer score visualization
                        st.write("**Synthèse des informations du client n°{}**".format(sk_id_curr))            

                        # Affichage de la sélection
                        st.write("Affichage de votre score client")
                        # Display a pie chart for the selected key
                        fig, ax = plt.subplots(figsize=(5,5))
                        plt.pie(label2, explode=[0, 0.1], labels=['Good', 'Bad'], autopct='%1.1f%%', startangle=90)
                        st.pyplot(fig)
                        
                        st.write("*Votre score client : {}*".format(label['score_1']*100))  
                        seuil = 0.42500000000000004
                        if label['score_1'] >= seuil:
                            st.write("Votre profil **correspond** aux critères de solvabilité de la banque")
                        else:
                            st.write("Votre profil **ne correspond pas** aux critères de solvabilité de la banque")


                        st.write("Affichage de l'analyse de votre score")
                        # Local visualization
                        feature_importance_local = label['feature_importance_locale']
                        print(feature_importance_local)
                        feature_importance_local = pd.DataFrame(feature_importance_local.items(), columns=['Feature', 'Value'])
                        print('feature_importance_local :\n', feature_importance_local)
                        st.header("**Local features importances contribution**")
                        fig = plt.figure(figsize=(10, 8))  # , facecolor=('#262730'))
                        plt.barh(feature_importance_local['Feature'], sorted(feature_importance_local['Value']))
                        plt.xlabel("Value")
                        plt.ylabel("Feature")
                        plt.tight_layout()
                        st.pyplot(fig)


                        st.write("Affichage de vos informations additionnelles")
                        st.header("Informations diverses du client n°{}".format(sk_id_curr))
                        st.dataframe(df_client)
                                
                    
                
            except ValueError:
                st.error("Entrez un numéro de client valide")


        # ----------------------------------------------------
        # Onglet 2
                
        with tab2: # onglet performance du model
            # URL = "http://credit-scoring-app-mdln.herokuapp.com/api/model_performance"
            URL = os.path.join(urlPath, "model_performance")
            

            st.header("Performance globale")
            r = requests.get(url=URL)
            # extracting data in json format
            print(r)
            if r.status_code == 200:
                try:
                    response = r.json()
                    #   print(response)

                    # images-by-stream
                    image0 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['features_importances'], "utf-8"))))
                    st.image(image0, caption='Feature Importance Global')

                except json.JSONDecodeError:
                    print("Error parsing JSON")
            else:
                print(f"Request failed with status code {r.status_code}")


        # ----------------------------------------------------
        # Onglet 3
                
        with tab3:  # onglet comparaison avec les autres clients
            URL = os.path.join(urlPath, "client_comparison")
            st.header("Tendances clients")
            r = requests.get(url=URL)
            # extracting data in json format
            print(r)
            if r.status_code == 200:
                try:
                    response = r.json()
                    #   print(response)

                    image1 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['CODE_GENDER'], "utf-8"))))
                    st.image(image1, caption='Distribution des genres dans notre base de clients')    
                    
                    image2 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['NAME_FAMILY_STATUS_Married'], "utf-8"))))
                    st.image(image2, caption='Distribution des situations maritales dans notre base de clients')

                    image3 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['FLAG_OWN_CAR'], "utf-8"))))
                    st.image(image3, caption='Distribution des propriétaires de voiture dans notre base de clients')

                    image4 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['AMT_INCOME_TOTAL'], "utf-8"))))
                    st.image(image4, caption='Distribution des revenus dans notre base de clients')

                    image5 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['AMT_CREDIT'], "utf-8"))))
                    st.image(image5, caption='Distribution des montants de crédit dans notre base de clients')

                    image6 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['AMT_ANNUITY'], "utf-8"))))
                    st.image(image6, caption='Distribution des montants d\'annuités dans notre base de clients')

                    image7 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['DAYS_BIRTH'], "utf-8"))))
                    st.image(image7, caption='Distribution des âges dans notre base de clients')

                    image8 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['DAYS_EMPLOYED_PERC'], "utf-8"))))
                    st.image(image8, caption='Distribution du nombre de jours travaillés avant la demande de prêt dans notre base de clients')

                    image9 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['DAYS_REGISTRATION'], "utf-8"))))
                    st.image(image9, caption='Distribution du nombre de jours entre le dernier enregistrement et la demande de prêt dans notre base de clients')

                    image10 = Image.open(io.BytesIO(base64.decodebytes(bytes(response['NAME_EDUCATION_TYPE_Secondary_secondary_special'], "utf-8"))))
                    st.image(image10, caption='Distribution du nombre de diplômés du secondaire dans notre base de clients')
        

                except json.JSONDecodeError:
                    print("Error parsing JSON")
            else:
                print(f"Request failed with status code {r.status_code}")


if __name__ == "__main__":
    main()

'''