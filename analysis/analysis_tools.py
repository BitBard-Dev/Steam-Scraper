# analysis/analysis_tools.py

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sqlite3

def generate_wordcloud(df_column, title, filename):
    text = " ".join(df_column.dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="black").generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.savefig(filename)
    plt.show()

def generate_price_histogram(df, filename, max_price=200):
    df = df[(df["price_usd"] > 0) & (df["price_usd"] <= max_price)]
    df["price_usd"].hist(bins=50)
    plt.xlabel("Price (USD)")
    plt.title("Price Distribution")
    plt.savefig(filename)
    plt.show()
