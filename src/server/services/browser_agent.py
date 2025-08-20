from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Browser, Page, Playwright

from .base import AbstractBrowserAgent
from core.logging import logger

class BrowserAgent(AbstractBrowserAgent):
    """Manages a headless browser for web inspection and interaction."""

    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def setup_browser(self, headless: bool = True, proxy_port: Optional[int] = None) -> bool:
        """Initializes Playwright and launches a browser instance."""
        logger.info(f"Setting up browser (headless: {headless})")
        try:
            self.playwright = await async_playwright().start()
            proxy_options = {"server": f"http://127.0.0.1:{proxy_port}"} if proxy_port else None
            self.browser = await self.playwright.chromium.launch(headless=headless, proxy=proxy_options)
            self.page = await self.browser.new_page()
            logger.info("Browser setup successful.")
            return True
        except Exception as e:
            logger.error(f"Failed to set up browser: {e}")
            return False

    async def navigate_and_inspect(self, url: str, wait_time: int = 5) -> Dict[str, Any]:
        """Navigates to a URL and inspects the page for key information."""
        if not self.page:
            return {"error": "Browser not initialized. Call setup_browser() first."}

        logger.info(f"Navigating to {url} and inspecting.")
        try:
            await self.page.goto(url, wait_until='networkidle', timeout=30000)
            await self.page.wait_for_timeout(wait_time * 1000)

            forms = await self.page.eval_on_selector_all('form', 'forms => forms.map(f => f.outerHTML)')
            links = await self.page.eval_on_selector_all('a', 'links => links.map(a => a.href)')
            scripts = await self.page.eval_on_selector_all('script', 'scripts => scripts.map(s => s.src)')

            result = {
                "url": url,
                "title": await self.page.title(),
                "forms": forms,
                "links": list(set(links)),
                "scripts": list(set(s for s in scripts if s)),
            }
            logger.info(f"Inspection of {url} successful.")
            return result
        except Exception as e:
            logger.error(f"Failed to navigate or inspect {url}: {e}")
            return {"error": str(e)}

    async def close_browser(self):
        """Closes the browser and stops Playwright."""
        logger.info("Closing browser.")
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.browser = None
        self.page = None
        self.playwright = None
        logger.info("Browser closed.")

browser_agent = BrowserAgent()
