
import streamlit as st
import pandas as pd

# Import the news collection functions
from news_collector import collect_all_news

# Placeholder for NewsAPI key
NEWSAPI_KEY = 'YOUR_NEWSAPI_KEY'

def main():
    st.title("Dashboard de Notícias Financeiras")

    # Collect news data
    news_data = collect_all_news(api_key=NEWSAPI_KEY)

    # Convert news data to DataFrame for easier manipulation
    df = pd.DataFrame(news_data)

    # Sidebar filters
    st.sidebar.header("Filtros")
    sources = df['source'].unique()
    selected_sources = st.sidebar.multiselect("Selecionar Fonte:", options=sources, default=sources)

    # Apply filters
    if selected_sources:
        df = df[df['source'].isin(selected_sources)]

    # Display the news
    st.subheader("Notícias")
    for index, row in df.iterrows():
        st.markdown(f"### {row['title']}")
        st.markdown(f"**Fonte:** {row['source']}")
        st.markdown(f"[Leia mais]({row['url']})")

    # Info about total articles
    st.sidebar.info(f"Total de notícias exibidas: {len(df)}")

if __name__ == "__main__":
    main()
