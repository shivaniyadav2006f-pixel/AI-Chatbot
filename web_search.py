from duckduckgo_search import DDGS


def web_search(query):

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return ""

        text = ""

        for i, result in enumerate(results, 1):
            text += f"{i}. {result['title']}\n"
            text += f"{result['body']}\n"
            text += f"Source: {result['href']}\n\n"

        return text

    except Exception as e:
        return f"Web search error: {e}"