import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories,cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    elif x == 'Less than 1 year':
        return 0.5
    else:
        return float(x)


def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor's degree"
    elif "Master’s degree" in x:
        return "Master's degree"
    elif "Professional degree" in x or "Other doctoral degree" in x:
        return "Post Grad"
    else:
        return "Less than Bachelor's"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCodePro","Employment","ConvertedComp"]]
    df = df.rename({'ConvertedComp':'Salary'},axis=1)
    df = df[df['Salary'].notna()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed full-time']
    df = df.drop("Employment",axis=1)

    country_map = shorten_categories(df['Country'].value_counts(),400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] > 10000]
    df = df[df['Country']!='Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    html_temp_explore = """
    <div style ="background-color:rgb(12,12,12)";padding:10px">
    <h1 style="color:white;text-align:center;"> Explore Software Engineer Salary</h2>
    </div>
    """
    st.markdown(html_temp_explore,unsafe_allow_html=True)
    html_temp_stack = """
    <div style ="background-color:Tomato";padding:10px">
    <h2 style="color:white;text-align:center;"> Stack Overflow Developer Survey 2020</h2>
    </div>
    """
    st.markdown(html_temp_stack,unsafe_allow_html=True)
    st.write("##")
    x = np.array(df['Country'].value_counts().index)
    y = np.array(df['Country'].value_counts().values)
    fig1 , ax1 = plt.subplots()
    '''ax1.pie(data,labels=data.index,autopct="%1.1f%%",shadow=True,startangle=90)
    ax1.axis("equal")'''
    percent = 100.*y/y.sum()

    patches, texts = ax1.pie(y, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
                                            key=lambda x: x[2],
                                            reverse=True))

    ax1.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
            fontsize=8)

    st.markdown("<h1 style='text-align: center;'>Percent of developers from different countries</h1>", unsafe_allow_html=True)

    #plt.tight_layout()

    st.pyplot(fig1)
    st.write("#")

    st.markdown("<h1 style='text-align: center;'>Mean Salary based on Country</h1>", unsafe_allow_html=True)
    st.write("#")
    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending = False)
    st.bar_chart(data)

    st.markdown("<h1 style='text-align: center;'>Mean Salary based on Experience</h1>", unsafe_allow_html=True)
    st.write("#")
    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending = False)
    st.line_chart(data)

