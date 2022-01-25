import pandas as pd
import streamlit as st
from yake import KeywordExtractor


@st.cache(allow_output_mutation=True, ttl=60 * 5, max_entries=20, suppress_st_warning=True)
def load_data(article_ids):
    full = pd.read_csv('20newsgroups.csv')
    full['id'] = full['id'].astype(str)
    # isolate data to only article ID's specified in user input
    filtered = full[full['id'].isin(article_ids)]
    missings = [x for x in article_ids if x not in (full['id'].tolist())]
    return filtered, missings


def main():
    if proplist:
        # load the dataset
        df, bad_ids = load_data(proplist)
        proposals = df['content'].tolist()
        # create yake settings
        language = "en"
        deduplication_algo = 'seqm'
        windowsize = 1
        yake_list = []
        kw_extractor = KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                        dedupFunc=deduplication_algo,
                                        windowsSize=windowsize, top=numOfKeywords, features=None)
        for j in range(len(proposals)):
            keywords = kw_extractor.extract_keywords(text=proposals[j])
            keywords = [x for x, y in keywords]
            yake_list.append(keywords)
        df['yake_keywords'] = yake_list

        # create a filtered dataframe to display
        display_cols = ['id', 'title', 'publication', 'author', 'date', 'yake_keywords']
        df_display = df[display_cols]

        # create streamlit app code
        st.markdown('IDs not processed: {}'.format(bad_ids))
        st.download_button(label='Download Search Results as CSV', data=df_display.to_csv(), file_name='keywords.csv')
        st.header('Top Article Keywords')
        st.table(df_display)


# streamlit opening page template code

st.set_page_config(layout="wide")

st.title('Article Keyword Extraction with YAKE')
st.sidebar.header('Inputs for Keyword Extraction')
proplist = st.sidebar.text_area('Enter Article IDs')
proplist = [x.strip() for x in proplist.split(',')]
numOfKeywords = st.sidebar.number_input('Number of Keywords', min_value=3, max_value=20, value=5, step=1)

st.sidebar.subheader('Optional Parameters')
max_ngram_size = st.sidebar.slider('Max n-gram size', min_value=1, max_value=3, value=2, step=1)
deduplication_thresold = st.sidebar.slider("Deduplication Threshold", min_value=0.1, max_value=0.9,
                                           value=0.9, step=0.1)

st.sidebar.subheader('Instructions: ')
st.sidebar.markdown('1. Enter comma delimited Article IDs into the text box')
st.sidebar.markdown('2. Choose number of Keywords to extract from proposal text')
st.sidebar.markdown(
    '3. Optional: Adjust any other parameters as desired (max ngram size, deduplication threshold, etc.')
st.sidebar.markdown('4. Modify the settings and iterate as needed!')
st.sidebar.subheader('Info on Optional Parameters:')
st.sidebar.markdown('**Max n-gram size:** Specifies the maximum size of the word or phrase to be returned as a keyword '
                    '(i.e. 1 returns single words, 2 returns single words as well as 2 word phrases, etc.')
st.sidebar.markdown(
    '**Deduplication Threshold:** Can help limit the duplication of keywords.  A value of 0.1 will avoid '
    'duplicate keywords (but may possibly extract keywords that are less indicative of the overall document theme), '
    'while a value of 0.9 will allow repetition of words in the keyword extraction process.')

if __name__ == "__main__":
    try:
        main()
    except:
        st.header('Enter Article IDs to start clustering!')
