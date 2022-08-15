# -*- coding: utf-8 -*-
# MYAPP 
# Copyright (c) 2022, Tristan Vanrullen - all rights reserved.
# Streamlit demo for project P09 / AI engineer path

import streamlit as st
import requests 
import json

def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}
# end function


# url du backend Azure Function qui délivre les recommendations pour un user_id donné : 'http://***'

def main():
    sample_url = "https://mycfrecommendergh.azurewebsites.net/api/HttpTrigger1"    
    sample_user_id = 50254 
    
    st.set_page_config(page_title="Recommender System", page_icon="🤖")


    st.title("Recommend articles with Azure Serverless backend function")
    st.image("./img/my_content_logo.png")

    session = requests.Session()

    # When making an external URL call, it is recommended to wrap it inside a st.form widget. 
    # This is mainly because Streamlit will re-execute the script every time a user interacts with your application, 
    # causing unnecessary HTTP requests calls. 
    # st.form helps to tackle this issue as it will batch all of the widgets inside it together and execute them only once on submission.
    # Create a new st.form widget and fill it with the following widgets:
    # st.number_input
    # st.form_submit_button

    with st.form("my_form"):
        service_url=st.text_input('Enter recommender system backend function url here',sample_url)
        
        test_input = st.text_input('Enter a user_id here (int number).',str(sample_user_id))
        submitted = st.form_submit_button("Recommend some articles")
    if submitted: 
        
        # sample_user_id = int(test_input)  
        if not test_input.isnumeric(): 
            st.error("Error : an int value is required !")   
        else:
            sample_user_id = int(test_input)
            input_data=json.dumps({"data": sample_user_id})

            headers = {'Content-Type':'application/json'}

            st.write("Connecting serverless backend :", service_url)

            try:
                resp = requests.post(service_url+"?code="+st.secrets["httpTrigger1_default_key"], input_data, headers=headers)
                try:
                    results_dic = resp.json() # json.loads(resp.json())
                    #print(results_dic)  
                    if results_dic['result']:
                        recommendations =results_dic['result']  
                        st.write('Here are the recommended articles :')
                        st.write(recommendations)
                        if results_dic['message']:
                            st.write(results_dic['message'])
                    else:
                        if results_dic['error']:
                            st.error("Error : ")    
                            st.code(results_dic['error'])
                except json.decoder.JSONDecodeError as e:
                        st.error("JSONDecodeError in the response received")
                        st.error(resp)
                # except json.decoder.RequestsJSONDecodeError as e:
                #        st.error("RequestsJSONDecodeError status: {}, msg: {}".format(e.status_code, e.msg))
            except requests.exceptions.ConnectionError:
                st.error("Connexion error")
# end main() function        
        
        
if __name__ == '__main__':
    main()