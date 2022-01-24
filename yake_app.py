import pandas as pd
import numpy as np
import yake

@st.cache(allow_output_mutation=True, ttl=60 * 5, max_entries=20, suppress_st_warning=True)
def load_data(article_ids):
    full = pd.read_csv('20newsgroups.csv')
    full['id'] = full['id'].astype(str)
    # isolate data to only article ID's specified in user input
    filtered = full[full['id'].isin(article_ids)]
    missings = [x for x in article_ids if x not in (full['id'].tolist())]
    return filtered, missings