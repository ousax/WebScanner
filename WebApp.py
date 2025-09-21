from __future__ import annotations
try:
    import sys
    import os
    import time
    import json
    import argparse
    import re
    from random import choice
    import requests
    from bs4 import BeautifulSoup
    from rich.traceback import install
    from rich.console import Console
    from rich.table import Table
    from fake_useragent import UserAgent
    from pyfiglet import figlet_format
except ModuleNotFoundError:
    try:
        os.system("pip3 install requests rich bs4 faker_useragent pyfiglet")
        import requests 
        from bs4 import BeautifulSoup
        from rich.traceback import install
        from rich.console import Console
    except:
        print("You may want to install the required libraries manually \npip3 install requests rich bs4")
except Exception as ModuleErrors:
    exit(f"ModuleErrors:{ModuleErrors}")

install()
console = Console()

parser = argparse.ArgumentParser(
    description="Scan websites"
)
parser.add_argument("-t", help="The target main domain", type=str, required=True)
parser.add_argument("-delays", help="The delays between requests", default=4, type=int)
args = parser.parse_args()
domain = args.t
delays = args.delays
class WebScanner(object):
    """
    This is the main class for the 
    WebScanner script , scan for multiple 
    technologies used
    wordpress version
    users if it's a wp instance and if it's enabled through 'wp-json/wp/v2/users'
    drupal version
    joomla version
    sensitive information hidden or hardcoded in the javascript files
    crawl the robots.txt, sitemap.xml files
    inspect the code source for api keys
    tokens  
    btoa atob base64 strings
    everything that starts with 'eyJ...'
    """
    def __init__(self, domain, delays):
        self.urlBase =  domain
        self.delays = delays
        self.ua = UserAgent().random
        self.Headers = {
            "User-Agent":self.ua,
            "Accept-Language":"en-US",
            "Referer":self.urlBase,
            "Origin":self.urlBase.split("//")[1] if "http" in self.urlBase else self.urlBase
        }
        self.finalUrl = "https://"+self.urlBase if self.urlBase not in ["https://", "http://"] else self.urlBase
        self.urlBase = self.finalUrl
        self.session = requests.Session()
    def Banner(self):
        table = Table(title="Information")
        textToRender: str = "W3bScann3r"
        COLORS = choice(["green", "black", "white", "magenta", "red", "yellow", "cyan"])
        Bold = choice(["bold", ""])
        banner: str = figlet_format(textToRender, font="slant")
        console.print(f"[bold {COLORS}] {banner} [/bold {COLORS}]")
        table.add_column("Domain", justify="center", overflow="ellipsis")
        table.add_column("Delays (s)", justify="center", overflow="ellipsis")
        table.add_row(self.urlBase, str(self.delays))
        console.print(table)
        console.rule("End")
        console.print(self.IsOk())
        self.ParseHtml() # run 
        self.Robots()
    def IsOk(self) -> bool:
        # check if the domain is up 
        self.req = self.session.get(self.finalUrl, headers=self.Headers, timeout=10, allow_redirects=False)
        return True if self.req.status_code == 200 else False
    def ParseHtml(self) -> object:
        if self.IsOk():
            console.print("[bold green] We good to go[/ bold green]")
            self.parseHtml = BeautifulSoup(self.req.text, "html.parser")
            console.print("[bold gray]The request response has been parsed[/ bold gray]")
            self.fileName = f"{self.urlBase.replace("http", "_").replace(":", "_").replace("//", "_").replace('.', '_')}.txt"
            with open(self.fileName, "w", encoding="utf-8") as ff:
                try:
                    ff.writelines(self.req.text)
                    console.print(f"[bold green] Source code saved to {self.fileName} [/bold green]")
                except Exception as e:
                    print(f"[red] Catch(e): {e} [red]")   
        else:
            console.print(f"[red] {self.finalUrl} may not be up[/red]")
            console.print("[bold yellow]Try again later[/ bold yellow]")
            exit()
        #console.print("[bold red] Unable to parse the html response[/ bold red]")
        #console.print(f"Status code: [bold yellow] {self.req.status_code}")
        #self.ExtractEndpoints() this one 
    def ExtractEndpoints(self): # read the source code
        try:
            console.print("[green] Extracting endpoints[/green]")
            self.Endpoints = []
            endpointsPattern: str = r"<(link|meta|script).+/>" # inspect the code for websites, endpoints 
            FileEndpoints: str = "https?://(www\.)?.*$\.(js|php|py|html|css)" # js, php, py, html, css ... files
            Instt = open(self.fileName, "r", encoding="utf-8")
            
        except Exception as e:
            console.print(f"[bold yellow] An has occured while trying to extract to read the source code in the '[green]{self.fileName}[/ green]' file [/ bold yellow]")
            print(e)
    def Robots(self):
        # sitemap.xml , robots.txt
        self.robots = requests.get(self.finalUrl+"/robots.txt", headers=self.Headers, timeout=10, allow_redirects=False)
        time.sleep(delays)
        #self.sitemap = requests.get(self.finalUrl+"/sitemap.xml", headers=self.Headers, timeout=10, allow_redirects=False)
        if self.robots.ok:
            console.print("[bold green] Parsing robots endpoints response ...[/ bold green]")
            console.print("Printing robots ...")
            self.parseRobots = BeautifulSoup(self.robots.text, "html.parser") # extract endpoints
            print(self.parseRobots)
        else:
            console.print(f"Returned a [{self.robots.status_code}] status code")
        #if self.sitemap.ok:
         #   console.print("[bold green] Parsing sitemap response ... [/ bold green]")
          #  self.parseSitemap = BeautifulSoup(self.sitemap.text, "html.parser") 
           # print(self.parseSitemap)
        #else:
         #   console.print(f"Returned a [{self.sitemap.status_code}] status code")
            return ""
        return self.parseRobots #(self.parseRobots, self.parseSitemap) if all([self.parseRobots, self.parseSitemap]) else ""
    def InspectCodeSource(self):
        ...
    def IsWordpressSite(self) -> bool:
        ...
webscanner = WebScanner(domain, delays)
webscanner.Banner()
