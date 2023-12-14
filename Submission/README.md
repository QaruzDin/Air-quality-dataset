# Air Quality Data ☁☁

## Setup environment
```
pipenv install
pipenv shell
pip install numpy pandas matplotlib streamlit
```

## Download beijing_climateData.csv

in **notebook.ipynb** run:
```
all_df.to_csv('./dashboard/beijing_climateData.csv', index= False)
```
## Run steamlit app

in terminal run:
```
# if from Submission
streamlit run .\dashboard\dashboard.py
# if direct folder dashboard
streamlit run dashboard.py

```