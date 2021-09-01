import streamlit as st
import numpy as np
import pickle

def load_model():
    with open('saved_model.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']


def show_predict_page():
    html_temp_explore = """
    <div style ="background-color:rgb(60, 179, 113)";padding:10px">
    <h1 style="color:white;text-align:center;"> Software Developer Salary Prediction</h2>
    </div>
    """
    st.markdown(html_temp_explore,unsafe_allow_html=True)
    #st.title("Software Developer Salary Prediction")
    st.write('##')
    st.write("""### Enter the following Information to predict salary""")
    countries = ("United States",     
    "India",                 
    "United Kingdom",        
    "Germany",               
    "Canada",                
    "Brazil",                 
    "France",                 
    "Spain",                  
    "Australia",              
    "Netherlands",            
    "Poland",                 
    "Italy",                  
    "Russian Federation",     
    "Sweden")

    education = ("Bachelor's degree", "Master's degree", "Less than Bachelor's",
       'Post Grad')
    
    country = st.selectbox("Country",countries)
    education = st.selectbox("Education Level",education)

    experience = st.slider("Years of Experience",0,50,2)
    button = st.button("Predict Salary")
    if button:
        X = np.array([[country,education,experience]])

        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)[0]

        st.header(f"The estimate Salary is ${salary:.2f}")

