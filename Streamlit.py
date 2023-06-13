import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from matplotlib.gridspec import GridSpec
import hydralit_components as hc
from streamlit.components.v1 import html
from streamlit_lottie import st_lottie
from PIL import Image, ImageOps
import plotly.express as px

st.set_page_config(layout="wide", page_title=None)

# Load the Parkinson's disease dataset
data = pd.read_csv("C:/Users/student/Downloads/parkinson.csv")

# Creating Navigation bar
menu_data = [{"label":"Demographic"}, {'label':'Medication'}, {'label':'Parkinson Facts'}, {'label':'Parkinson Death'}]
menu_id = hc.nav_bar(menu_definition=menu_data, sticky_mode='sticky')

if menu_id =="Demographic":
    st.header("Parkinson's Disease Data Analysis")
    st.subheader("Demographics Analysis")
    
    col1, col2 = st.columns(2)
    data= data.dropna(subset=['Demographic information: Gender'])
    # Gender distribution
    gender_counts = data["Demographic information: Gender"].value_counts()

    # Create a bar chart for gender distribution
    fig_gender = go.Figure(data=go.Bar(x=gender_counts.index, y=gender_counts.values))

    # Set chart layout
    fig_gender.update_layout(
        title='Gender Distribution for Parkinson',
        xaxis_title='Gender',
        yaxis_title='Count',
        showlegend=False)

    # Display the bar chart using Plotly
    col1.plotly_chart(fig_gender, use_container_width=True)

    # Create a select box for gender
    gender_options = ['All'] + data["Demographic information: Gender"].unique().tolist()
    selected_gender = col1.selectbox("Select Gender", gender_options)

# Remove the missing values represented by "-" and NaN
    age_of_onset = [int(age) for age in data['Age of disease onset (years)'] if not pd.isna(age) and age != '-']

    # Filter the data based on the selected gender
    if selected_gender == 'All':
        filtered_df_tremor = data
        filtered_df_age = age_of_onset
    else:
        filtered_df_tremor = data[data['Demographic information: Gender'] == selected_gender]
        filtered_df_age = [int(age) for age, gender in zip(data['Age of disease onset (years)'], data['Demographic information: Gender']) if not pd.isna(age) and age != '-' and gender == selected_gender]
    col3, col4= st.columns(2)
    # Calculate tremor counts for the filtered data
    tremor_counts = filtered_df_tremor['Tremor'].value_counts()

    # Create a pie chart for tremor distribution
    fig_tremor = go.Figure(data=[go.Pie(labels=tremor_counts.index, values=tremor_counts.values)])

    # Set chart layout
    fig_tremor.update_layout(
        title='Tremor Distribution',
        showlegend=True)

    # Display the pie chart using Plotly
    col3.plotly_chart(fig_tremor, use_container_width=True)

    # Plot the histogram in the second column
    with col4:
    # Create a histogram
        plt.hist(filtered_df_age, bins=10, edgecolor='black')

        # Set the plot labels and title
        plt.xlabel('Age of Disease Onset (years)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Age of Disease Onset')

    # Remove the border of the histogram
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        # Display the plot
        st.pyplot(plt)
    
if menu_id == "Medication":
    st.header("Parkinson's Disease Data Analysis")
    st.subheader("Medications")

    col5, col6 = st.columns(2)

    # Count the frequency of "Yes" and "No" values for Antidepressant therapy
    medication_counts1 = data['Medication: Antidepressant therapy'].value_counts()

    # Create a bar chart for Antidepressant therapy distribution
    fig_medication1 = go.Figure(data=go.Bar(x=medication_counts1.index, y=medication_counts1.values))

    # Set chart layout for Antidepressant therapy
    fig_medication1.update_layout(
        title='Distribution of Medication: Antidepressant therapy',
        xaxis_title='Medication',
        yaxis_title='Count',
        showlegend=False)

    # Display the bar chart for Antidepressant therapy using Plotly
    col5.plotly_chart(fig_medication1, use_container_width=True)

    # Count the frequency of "Yes" and "No" values for Antiparkinsonian medication
    medication_counts4 = data['Medication: Benzodiazepine medication'].value_counts()

    # Create a bar chart for Antiparkinsonian medication distribution
    fig_medication4 = go.Figure(data=go.Bar(x=medication_counts4.index, y=medication_counts4.values))

    # Set chart layout for Antiparkinsonian medication
    fig_medication4.update_layout(
        title='Distribution of Medication: Benzodiazepine medication',
        xaxis_title='Medication',
        yaxis_title='Count',
        showlegend=False)

    # Display the bar chart for Antiparkinsonian medication using Plotly
    col6.plotly_chart(fig_medication4, use_container_width=True)

    col9,col10= st.columns(2)
# Count the frequency of medications for Medication: Antidepressant therapy across gender
    medication_gender_counts = data.groupby(['Demographic information: Gender', 'Medication: Antidepressant therapy']).size().unstack()

    # Create a stacked bar chart for Medication: Antidepressant therapy across gender
    fig_medication_gender = go.Figure(data=[
        go.Bar(name=medication, x=medication_gender_counts.index, y=medication_gender_counts[medication])
        for medication in medication_gender_counts.columns])

    # Set chart layout for Medication: Antidepressant therapy across gender
    fig_medication_gender.update_layout(
        title='Distribution of Medication: Antidepressant therapy across Gender',
        xaxis_title='Gender',
        yaxis_title='Count',
        showlegend=True)

    # Display the stacked bar chart for Medication: Antidepressant therapy across gender using Plotly
    col9.plotly_chart(fig_medication_gender, use_container_width=True)

    # Filter the data for Medication: Antidepressant therapy and select the necessary columns
    medication_tremor_data = data[['Tremor', 'Medication: Antidepressant therapy']]

    # Group the data by Tremor and Medication: Antidepressant therapy, and count the occurrences
    medication_tremor_counts = medication_tremor_data.groupby(['Tremor', 'Medication: Antidepressant therapy']).size().unstack()

    # Create a grouped bar chart for Medication: Antidepressant therapy across Tremor
    fig_medication_tremor = go.Figure(data=[
        go.Bar(name=medication, x=medication_tremor_counts.index, y=medication_tremor_counts[medication])
        for medication in medication_tremor_counts.columns])

    # Set chart layout for Medication: Antidepressant therapy across Tremor
    fig_medication_tremor.update_layout(
        title='Distribution of Medication: Antidepressant therapy across Tremor',
        xaxis_title='Tremor',
        yaxis_title='Count',
        showlegend=True)

    # Display the grouped bar chart for Medication: Antidepressant therapy across Tremor using Plotly
    col10.plotly_chart(fig_medication_tremor, use_container_width=True)

    col11,col12= st.columns(2)
# Count the frequency of medications for Medication: Benzodiazepine medication across gender
    medication_gender_counts = data.groupby(['Demographic information: Gender', 'Medication: Benzodiazepine medication']).size().unstack()

    # Create a stacked bar chart for Medication: Benzodiazepine medication across gender
    fig_medication_gender = go.Figure(data=[
        go.Bar(name=medication, x=medication_gender_counts.index, y=medication_gender_counts[medication])
        for medication in medication_gender_counts.columns])

    # Set chart layout for Medication: Benzodiazepine medication across gender
    fig_medication_gender.update_layout(
        title='Distribution of Medication: Benzodiazepine medication',
        xaxis_title='Gender',
        yaxis_title='Count',
        showlegend=True)

    # Display the stacked bar chart for Medication: Benzodiazepine medication across gender using Plotly
    col11.plotly_chart(fig_medication_gender, use_container_width=True)

    # Filter the data for Medication: Benzodiazepine medication and select the necessary columns
    medication_tremor_data = data[['Tremor', 'Medication: Benzodiazepine medication']]

    # Group the data by Tremor and Medication: Benzodiazepine medication, and count the occurrences
    medication_tremor_counts = medication_tremor_data.groupby(['Tremor', 'Medication: Benzodiazepine medication']).size().unstack()

    # Create a grouped bar chart for Medication: Benzodiazepine medication across Tremor
    fig_medication_tremor = go.Figure(data=[
        go.Bar(name=medication, x=medication_tremor_counts.index, y=medication_tremor_counts[medication])
        for medication in medication_tremor_counts.columns])

    # Set chart layout for Medication: Benzodiazepine medication across Tremor
    fig_medication_tremor.update_layout(
        title='Distribution of Medication: Benzodiazepine medication across Tremor',
        xaxis_title='Tremor',
        yaxis_title='Count',
        showlegend=True)

    # Display the grouped bar chart for Medication: Benzodiazepine medication across Tremor using Plotly
    col12.plotly_chart(fig_medication_tremor, use_container_width=True)


    # Define the medication columns
    medication_columns = ['Medication: Antidepressant therapy',
                      'Medication: Antiparkinsonian medication',
                      'Medication: Antipsychotic medication',
                      'Medication: Benzodiazepine medication',]

   # Convert medication columns to numeric
    data[medication_columns] = data[medication_columns].apply(pd.to_numeric, errors='coerce')

    # Create a stacked bar chart
    plt.figure(figsize=(10, 6))
    data[medication_columns].sum().plot(kind='bar', stacked=True)

    plt.xlabel('Patient')
    plt.ylabel('Number of Patients')
    plt.title('Medication Distribution of Patients')
    plt.legend(loc='upper right')
    plt.xticks(rotation=0)

    plt.show()

if menu_id =="Parkinson Facts":
    st.header("Parkinson's Facts")
    
    # Add space between the header and the facts
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    image1_path = r"C:\Users\student\Desktop\download.jpg"
    image2_path = r"C:\Users\student\Desktop\parkinsons.jpg"
    image3_path = r"C:\Users\student\Desktop\Substantia-nigra.png"
    image4_path = r"C:\Users\student\Desktop\download.png"
    image5_path = r"C:\Users\student\Desktop\poisoning-pill-bottle.jpg"
    col1, col2, col3 = st.columns(3)
    image_width = 200
    with col1:
        image1 = Image.open(image1_path)
        st.image(image1, width=image_width)
    with col2:
        image2_path = Image.open(image2_path)
        st.image(image2_path, width=image_width)
    with col3:
        image3_path = Image.open(image3_path)
        st.image(image3_path, width=image_width)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("<h6 style='text-align: center; color: blue;'>Parkinson's disease is a neurodegenerative disorder.</h6>", unsafe_allow_html=True)

    with col5:
        st.markdown("<h6 style='text-align: center; color: blue;'>It affects movement and is characterized by tremors, stiffness, and impaired balance</h6>", unsafe_allow_html=True)

    with col6:
        st.markdown("<h6 style='text-align: center; color: blue;'>Parkinson's disease is caused by a loss of dopamine-producing cells in the brain</h6>", unsafe_allow_html=True)

    col7, col8= st.columns(2)
    with col7:
        image4_path = Image.open(image4_path)
        st.image(image4_path, width= image_width)
    with col8:
        image5_path = Image.open(image5_path)
        st.image(image5_path, width= image_width)

    col9,col10= st.columns(2)
    with col9: 
        st.markdown("<div style='display: flex; flex-direction: column; align-items: center;'>"
                "<h6 style='color: blue;'>The exact cause of the disease is unknown, but both genetic and environmental factors play a role</h6>"
                "</div>", unsafe_allow_html=True)
    with col10:
        st.markdown("<div style='display: flex; flex-direction: column; align-items: center;'>"
                "<h6 style='color: blue;'>There is currently no cure for Parkinson's disease, but treatment options are available to manage symptoms</h6>"
                "</div>", unsafe_allow_html=True)


if menu_id =="Parkinson Death":
    st.header("Parkinson's Disease Data Analysis")
    st.subheader("Death Analysis")   
    df = pd.read_csv("C:/Users/student/Downloads/WHOMortalityDatabase_Deaths_sex_age_a_country_area_year-Parkinson disease_11th June 2023 14_19 (1).csv")
    df = df.dropna(subset=['Death rate per 100 000 population'])
    # Create two columns using st.columns()
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Select Country", df['Country Name'].unique())
    filtered_data = df[df['Country Name'] == country]

    # Plot line chart in the first column
    with col2:
        tab = st.selectbox("Select Gender", df['Sex'].unique())

    col3, col4= st.columns(2)
    with col3: 
        st.subheader(f"Death of {tab} in {country}")
        fig, ax = plt.subplots()
        ax.plot(filtered_data['Year'], filtered_data['Death rate per 100 000 population'])
        ax.set(xlabel='Year', ylabel='Death', title=f"{tab} Death rate per 100 000 population Over Time in {country}")
        ax.grid()

    # Display line chart
        st.pyplot(fig)
    # Create the figure
    with col4:
        st.subheader("Death per 100 000 population by Age Group")
        fig = go.Figure()

# Iterate over the age groups and add bar traces
        for age_group in df['Age Group'].unique():
            filtered_data = df[df['Age Group'] == age_group]
            fig.add_trace(
                go.Bar(x=filtered_data['Age Group'],
                y=filtered_data['Death rate per 100 000 population'],
                name=age_group
                ))
# Update the layout
        fig.update_layout(xaxis_title="Age Group",
            yaxis_title="Death per 100 000 population")

# Display the chart
        st.plotly_chart(fig, use_container_width=True)

# Death bar chart
    st.subheader("")
    st.subheader(f'Percentage of cause-specific deaths out of total deaths')

        # Filter data based on selections
    df3_filtered = df[df['Country Name'] == country].copy()

        # Convert Year to string using .loc
    df3_filtered.loc[:, 'Year'] = df3_filtered['Year'].astype(str)
    df3 = df3_filtered.dropna(subset=["Percentage of cause-specific deaths out of total deaths"])

        # Create a horizontal bar chart with animation
    fig = px.bar(df, x="Percentage of cause-specific deaths out of total deaths", y="Country Name",
            animation_frame="Year", orientation="h", color="Country Name")

        # Set chart layout
    fig.update_layout(xaxis_title="Percentage",
    yaxis_title="Country",
    yaxis_categoryorder="total ascending",
    height=600
    )

        # Display the chart
    st.plotly_chart(fig)
        
        # Remove the color legend
    fig.update_traces(showlegend=False)

        # Hide the x-axis
    fig.update_xaxes(showline=False, showticklabels=False)

# Creating the Choropleth map with animation over the years
    st.subheader(f'Death rate per 100 000 population across countries throughout the years')
    fig1 = px.choropleth(
    df, 
    locations='Country Code',
    color='Death rate per 100 000 population',
    hover_name='Country Name',
    animation_frame='Year',  # animation over the years
    color_continuous_scale=px.colors.sequential.Plasma,
    height=600  # adjust as needed
    )
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000  # set the duration of the transition between frames
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500  # set the duration of the transition between frames

    st.plotly_chart(fig1, use_container_width=True)  # make the plot use the full container width
