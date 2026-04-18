from newspaper import Article

def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()

        return article.title + "\n\n" + article.text

    except:
        return None