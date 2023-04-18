import json
from duckduckgo_search import ddg
from utils.browse import scrape_links, scrape_text, summarize_text

def web_search(query, num_results=8):
    """Return the results of a web search"""
    search_results = []
    for j in ddg(query, max_results=num_results):
        search_results.append(j)
    return json.dumps(search_results, ensure_ascii=False, indent=4)

def get_hyperlinks(url):
    """Return the results of a web search"""
    link_list = scrape_links(url)
    return link_list

def extract_hyperlinks(soup):
    """Extract hyperlinks from a BeautifulSoup object"""
    hyperlinks = []
    for link in soup.find_all('a', href=True):
        hyperlinks.append((link.text, link['href']))
    return hyperlinks

def get_text_summary(url, question):
    """Summarize the text of a webpage"""
    text = scrape_text(url)
    summary = summarize_text(text, question)
    return """ "Result" : """ + summary

def browse_website(url, question):
    """Browse a website and return the summary and links"""
    summary = get_text_summary(url, question)
    # links = get_hyperlinks(url)

    # # Limit links to 5
    # if len(links) > 5:
    #     links = links[:5]

    # result = f"""Website Content Summary: {summary}\n\nLinks: {links}"""
    result = f"""Website Content Summary: {summary}"""

    return result

def stalk_user(user_name):
    """Stalk a user"""
    web_search_res = web_search(user_name, num_results=8)
    urls = [res["href"] for res in json.loads(str(web_search_res))]
    website_data = []
    for url in urls:
        website_data.append(browse_website(url, f"Extract information about the user {user_name} in a paragraph of 3 sentences."))
    # concat the website data
    website_data = " ".join(website_data)
    website_data = website_data.replace('Website Content Summary: "Result" : ', "").replace("Error: No text to summarize", "")
    return website_data, urls