import pandas as pd

def process_data(path: str):
    '''
    Load dataset from csv and return two dataframes to be used in app
    
    Returns-
    df -> Dataframe consisting of string values to display in app
    dataset -> Dataframe consisting of float values to be used for filtering
    '''
    
    dataset = pd.read_csv(path)
    
    # ------------------------------From data_cleaning.ipynb-----------------------------------
    
    # Selecting relevent columns
    dataset = dataset[["name", "calories", "total_fat", "cholesterol", "vitamin_a", "vitamin_b12", "vitamin_b6", "vitamin_c",
                        "vitamin_d", "vitamin_e", "vitamin_k", "calcium", "irom", "magnesium", "phosphorous", "potassium",
                        "zink", "protein", "carbohydrate", "fiber", "sugars", "glucose", "sucrose", "alcohol", "caffeine", "water"]]
    dataset = dataset.rename(columns = {"name":"item", "irom":"iron", "zink":"zinc"})

    # Creating a row containing units for each column
    units = ["cal", "g", "mg", "IU", "mcg", "mg", "mg", "IU", "mg", "mcg", "mg", "mg", "mg", "mg", "mg",
            "mg", "g", "g", "g", "g", "g", "g", "g", "mg", "g"]

    dataset.loc[-1] = ["units"] + units
    dataset.index = dataset.index + 1
    dataset = dataset.sort_index()
    
    def str2float(series):
        unit = series.iloc[0]
        
        for i in range(1, len(series)):
            if isinstance(series.iloc[i], float): continue
            
            if not isinstance(series.iloc[i], int):
                series.iloc[i] = series.iloc[i].replace(unit, "").strip()
                
            try:
                series.iloc[i] = float(series.iloc[i])
            except Exception:
                pass
                
        return series

    # Converting the whole dataframe to float values
    for i in range(1, len(dataset.axes[1])):
        str2float(dataset.iloc[:, i])
        
    for i in list(dataset.vitamin_a[dataset.vitamin_a == "0.00 mcg"].index):
        dataset.vitamin_a[i] = 0.0

    # 1 IU = 0.3 mcg (retinol)
    dataset.vitamin_a[dataset.vitamin_a == "89.00 mcg"] = 89/0.3
    dataset.vitamin_a[dataset.vitamin_a == "17.00 mcg"] = 17/0.3
    
    dataset = dataset.drop_duplicates()
    
    # Renaming columns
    dataset = dataset.rename(columns={"item": "Food Item"})
    for col in dataset.columns:
        dataset = dataset.rename(columns={col: col.replace("_", " ").title()})
    
    #-----------------------------------------------------------------------------------------------
    
    # Readding units to new copied dataframe
    df = dataset.copy().astype(str)
    for col in df:
        if col == 'Food Item': continue
        for i in range(len(df[col])):
            if not df[col][i].replace(".", "").isnumeric(): continue
            df[col][i] = f"{df[col][i]} {df[col][0]}"
    
    df = df.drop(index=0)
    return df, dataset

p, q = process_data("dataset/nutrition.csv")
p.to_csv("data/for_app.csv", index=False)
q.to_csv("data/to_analyze.csv", index=False)