import requests
from bs4 import BeautifulSoup
from ..Tools.Tool import Tool
from ..utils.print_utils import log_tool_action

class ScraperTool(Tool):

    def __init__(self, show_tool_call: bool = False):
        self.__name = "web_scraper"
        self.__description = (
            "This tool extracts the full, raw text content from a given list of URLs. It can handle various website structures, "
            "including dynamically loaded content (JavaScript). Use this tool when you need to access the complete information present on a webpage, "
            "beyond what is available in search result snippets."
            )
        
        self.show_tool_call = show_tool_call
    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    def _run_implementation(self, urls: list[str]):

        url_contents = dict()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        if self.show_tool_call:
            log_tool_action("Scraping URLs:", urls, "📄", "magenta")

        for url in urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")
                anchors = soup.find_all("body")[0].find_all("a")
                content = []
                for p in paragraphs:
                    content.append(p.get_text(strip=True))
                
                internal_links = []
                for a in anchors:
                    internal_links.append((a.get_text(strip=True), a.get("href")))
                

                
                
                url_contents[url] = {"content": "\n".join(content), "internal_links": internal_links}
            except Exception as e:
                url_contents[url] = f"[ERROR]: {e}"
        
        return url_contents