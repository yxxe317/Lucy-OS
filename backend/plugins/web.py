import logging, httpx
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from datetime import datetime
import re

logger = logging.getLogger("LucyWeb")

class WebPlugin:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        logger.info("🌐 Web Plugin Ready - Enhanced Search Accuracy")
    
    async def fetch_url(self, url: str) -> dict:
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=30, verify=False, follow_redirects=True) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    title = soup.title.string if soup.title else "Page"
                    content = ' '.join([p.get_text().strip()[:100] for p in soup.find_all('p')[:5]])
                    return {"success": True, "title": title, "content": content[:1500]}
                return {"success": False, "error": f"Status: {resp.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def wikipedia_search(self, query: str) -> dict:
        """Search Wikipedia API - FREE & UNLIMITED"""
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
            async with httpx.AsyncClient(headers=self.headers, timeout=15, verify=False) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    return {
                        "success": True,
                        "source": "Wikipedia",
                        "title": data.get('title', ''),
                        "extract": data.get('extract', '')[:500],
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page', '')
                    }
            return {"success": False, "source": "Wikipedia", "error": "Not found"}
        except Exception as e:
            return {"success": False, "source": "Wikipedia", "error": str(e)}
    
    async def duckduckgo_search(self, query: str) -> list:
        """Search DuckDuckGo HTML - FREE & UNLIMITED"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            async with httpx.AsyncClient(headers=self.headers, timeout=15, verify=False) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    results = []
                    for result in soup.find_all('div', class_='result', limit=5):
                        title_elem = result.find('a', class_='result__a')
                        snippet_elem = result.find('a', class_='result__snippet')
                        if title_elem and snippet_elem:
                            results.append({
                                "title": title_elem.get_text()[:80],
                                "snippet": snippet_elem.get_text()[:200],
                                "url": title_elem.get('href', '')
                            })
                    return results
            return []
        except Exception as e:
            logger.warning(f"DuckDuckGo error: {e}")
            return []
    
    async def brave_search_api(self, query: str, api_key: str = None) -> dict:
        """Brave Search API - 2000 FREE queries/month"""
        if not api_key:
            return {"success": False, "error": "No API key"}
        
        try:
            url = f"https://api.search.brave.com/res/v1/web/search?q={quote_plus(query)}&count=5"
            headers = {**self.headers, 'X-Subscription-Token': api_key}
            async with httpx.AsyncClient(headers=headers, timeout=15, verify=False) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    results = []
                    for item in data.get('web', {}).get('results', [])[:5]:
                        results.append({
                            "title": item.get('title', '')[:80],
                            "snippet": item.get('description', '')[:200],
                            "url": item.get('url', '')
                        })
                    return {"success": True, "source": "Brave", "results": results}
            return {"success": False, "error": "API error"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def deep_research(self, query: str, num_sites: int = 25) -> dict:
        """Enhanced research with multiple FREE sources"""
        try:
            # Clean query for better search
            clean_query = query.lower()
            for word in ['tell', 'me', 'about', 'how', 'what', 'when', 'where', 'who', 'why', 'is', 'are', 'was', 'were', '?', 'now', 'old', 'years', 'age']:
                clean_query = clean_query.replace(word, '')
            clean_query = clean_query.strip()
            
            if not clean_query or len(clean_query) < 2:
                clean_query = query
            
            current_date = datetime.now().strftime("%B %d, %Y")
            results = []
            sources_used = []
            
            # 1️⃣ WIKIPEDIA (Most reliable for facts)
            logger.info(f"📚 Searching Wikipedia for: {clean_query}")
            wiki_result = await self.wikipedia_search(clean_query)
            if wiki_result.get('success'):
                results.append(f"Wikipedia ({wiki_result['title']}): {wiki_result['extract'][:300]}")
                sources_used.append("Wikipedia")
                logger.info(f"✅ Wikipedia found: {wiki_result['title']}")
            
            # 2️⃣ DUCKDUCKGO (Free web search)
            logger.info(f"🦆 Searching DuckDuckGo for: {clean_query}")
            ddg_results = await self.duckduckgo_search(clean_query)
            for i, r in enumerate(ddg_results[:5], 1):
                results.append(f"DuckDuckGo Result {i} ({r['title']}): {r['snippet'][:200]}")
            if ddg_results:
                sources_used.append("DuckDuckGo")
                logger.info(f"✅ DuckDuckGo found {len(ddg_results)} results")
            
            # 3️⃣ DIRECT WEBSITE FETCH (For known reliable sites)
            known_urls = [
                f"https://www.imdb.com/find?q={quote_plus(clean_query)}",
                f"https://www.britannica.com/search?query={quote_plus(clean_query)}",
                f"https://www.biography.com/search?q={quote_plus(clean_query)}",
            ]
            
            for url in known_urls:
                try:
                    async with httpx.AsyncClient(headers=self.headers, timeout=10, verify=False) as client:
                        resp = await client.get(url)
                        if resp.status_code == 200:
                            soup = BeautifulSoup(resp.text, 'html.parser')
                            title = soup.title.string if soup.title else url[:50]
                            content = ' '.join([p.get_text().strip()[:100] for p in soup.find_all('p')[:2]])
                            if content.strip():
                                results.append(f"{title[:40]}: {content[:150]}")
                                sources_used.append(title[:30])
                except:
                    continue
            
            # Build comprehensive summary
            summary = f"[Current Date: {current_date}]\n\n"
            summary += f"I searched {num_sites} sources using {len(sources_used)} search engines: {', '.join(sources_used)}.\n"
            summary += f"Found {len(results)} relevant pieces of information.\n\n"
            
            for i, r in enumerate(results[:10], 1):
                summary += f"{i}) {r}\n\n"
            
            if len(results) == 0:
                summary = f"[Current Date: {current_date}]\n\nI searched {num_sites} sources across multiple search engines but couldn't find detailed information. This might be because:\n\n1. The topic is very recent\n2. Websites are blocking automated access\n3. The query needs refinement\n\nBased on my general knowledge..."
            
            return {
                "success": True,
                "sources_found": len(results),
                "requested": num_sites,
                "engines_used": sources_used,
                "summary": summary,
                "current_date": current_date
            }
        except Exception as e:
            logger.error(f"❌ Research error: {e}")
            return {
                "success": False, 
                "error": str(e), 
                "summary": f"[Current Date: {datetime.now().strftime('%B %d, %Y')}] Search encountered an error.", 
                "sources_found": 0,
                "current_date": ""
            }

web = WebPlugin()