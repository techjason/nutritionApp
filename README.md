# [IntelliNutritor](https://intellinutritor.streamlit.app/) 🌾🍒🍓 <img src="icon.png" width="100" height="100" align="right">

Find food items with right nutritional values for you.

This is a Streamlit <img src="https://docs.streamlit.io/logo.svg" width="22"> based app which fetches data from a large nutritional dataset and shows you food items according to your preferences.

<img src="https://i.ibb.co/pL3xSJx/intelli-home.png" title="Preview">

## How to run

*Visit [intellinutritor.streamlit.app](https://intellinutritor.streamlit.app/) to directly use this app.*

For local installation:

1. Clone this repository.

2. Inside the root folder, type this in command line to install all dependencies:  
`pip install -r requirements.txt`  

3. Enter `streamlit run app.py` in command line to run the app locally.

## Dataset used

[Nutritional values for common foods and products (Kaggle)](https://www.kaggle.com/datasets/trolukovich/nutritional-values-for-common-foods-and-products)

## Preprocessing of data

I did initial data cleaning in the jupyter notebook ***'data_cleaning.ipynb'*** which generates a cleaned dataframe and saves it as ***'to_analyze.csv'*** in data folder.

After that I copied all the cleaning operations done in notebook to ***'data_cleaning.py'*** script and added one more operation to output another dataframe with string values to be displayed on the frontend. I saved the second dataframe as ***'for_app.csv'***.

Now ***'data_cleaning.py'*** takes the ***'nutrition.csv'*** and outputs both ***'to_analyze.csv'*** and ***'for_app.csv'*** in data folder.