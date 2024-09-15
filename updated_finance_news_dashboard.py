import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

# Obtém a chave da NewsAPI a partir dos "Secrets" do Streamlit
NEWSAPI_KEY = st.secrets["b99e24b789f043499c2fb89f2b73f7d5"]

# Function to get news from Google News using NewsAPI
def get_news_from_newsapi(api_key: str, query: str = "mercado financeiro", language: str = "pt") -> List[Dict[str, str]]:
    url = "https://newsapi.org/v2/everything"
    params = {
        'q': query,
        'language': language,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    news_data = []

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        for article in articles:
            news_data.append({
                'title': article.get('title'),
                'source': article.get('source', {}).get('name'),
                'date': article.get('publishedAt'),
                'url': article.get('url'),
                'image': article.get('urlToImage')
            })
    else:
        print(f"Error fetching news from NewsAPI: {response.status_code}")
    
    return news_data

# Function to get news from Valor Econômico via web scraping
def get_news_from_valor_economico() -> List[Dict[str, str]]:
    url = "https://valor.globo.com/"
    response = requests.get(url)
    news_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('div.feed-post-body')

        for article in articles[:10]:  # Limit to top 10 articles for simplicity
            title = article.find('a', class_='feed-post-link').get_text(strip=True)
            url = article.find('a', class_='feed-post-link')['href']
            news_data.append({
                'title': title,
                'source': 'Valor Econômico',
                'date': None,  # No date available on the main page
                'url': url,
                'image': None  # No image scraping implemented for simplicity
            })
    else:
        print(f"Error fetching news from Valor Econômico: {response.status_code}")
    
    return news_data

# Function to get news from Exame via web scraping
def get_news_from_exame() -> List[Dict[str, str]]:
    url = "https://exame.com/mercados/"
    response = requests.get(url)
    news_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('div.feed-item-wrapper')

        for article in articles[:10]:  # Limit to top 10 articles for simplicity
            title = article.find('h3').get_text(strip=True)
            url = article.find('a')['href']
            news_data.append({
                'title': title,
                'source': 'Exame',
                'date': None,  # No date available on the main page
                'url': url,
                'image': None  # No image scraping implemented for simplicity
            })
    else:
        print(f"Error fetching news from Exame: {response.status_code}")
    
    return news_data

# Function to get news from InfoMoney via web scraping
def get_news_from_infomoney() -> List[Dict[str, str]]:
    url = "https://www.infomoney.com.br/mercados/"
    response = requests.get(url)
    news_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('div.col-xs-12.col-sm-8.col-md-8.news-item')

        for article in articles[:10]:  # Limit to top 10 articles for simplicity
            title = article.find('h2').get_text(strip=True)
            url = article.find('a')['href']
            news_data.append({
                'title': title,
                'source': 'InfoMoney',
                'date': None,  # No date available on the main page
                'url': url,
                'image': None  # No image scraping implemented for simplicity
            })
    else:
        print(f"Error fetching news from InfoMoney: {response.status_code}")
    
    return news_data

# Collect news from all sources
def collect_all_news(api_key: str) -> List[Dict[str, str]]:
    news_data = []
    
    # Collect news from NewsAPI (Google News)
    news_data.extend(get_news_from_newsapi(api_key=api_key))
    
    # Collect news from Valor Econômico
    news_data.extend(get_news_from_valor_economico())
    
    # Collect news from Exame
    news_data.extend(get_news_from_exame())
    
    # Collect news from InfoMoney
    news_data.extend(get_news_from_infomoney())
    
    return news_data

# Streamlit code for displaying the news dashboard
def main():
    st.title("Dashboard de Notícias Financeiras")

    # Placeholder for market indicators (static for now)
    st.subheader("Indicadores de Mercado")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ibovespa", "134.881,95", "+0,64%")
    col2.metric("IGOVERN", "21.088,97", "+0,82%")
    col3.metric("IBRX BRA", "57.006,51", "+0,66%")
    col4.metric("Dow Jones", "41.393,78", "+0,72%")

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
    st.subheader("Notícias Recentes")
    for index, row in df.iterrows():
        st.markdown(f"### {row['title']}")
        if row['image']:
            st.image(row['image'], use_column_width=True)
        st.markdown(f"**Fonte:** {row['source']}")
        st.markdown(f"[Leia mais]({row['url']})")

    # Info about total articles
    st.sidebar.info(f"Total de notícias exibidas: {len(df)}")

if __name__ == "__main__":
    main()
