from HTMLParser import HTMLParser
import requests
import sys


'''
LinkFinder subclasses HTMLParser. While parsing an HTML string, <handle_starttag> appends all hyperlinks to the local list <links>
'''
class LinkFinder(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = []

	def handle_starttag(self, tag, attrs):
		if tag == 'a' or tag == 'link':
			for name, value in attrs:
				if name == "href":
					self.links.append(value)

'''
Takes a start url: <base>, and prints all the links found at that url. Recurses through this process for all links that fall under the same domain.
'''
def mapSite(base, current_page, visited, site_map):
	if current_page not in site_map:
		print current_page
		r = requests.get(current_page)
		parser = LinkFinder()
		parser.feed(r.text)
		site_map[current_page] = parser.links
		for link in parser.links:
			print('\t' + link)
		for link in site_map[current_page]:
			if base in link:
				mapSite(base, link, visited, site_map)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: \n$ python crawler.py <start_url>'
		exit()
	url = sys.argv[1]
	try:
		r = requests.get(url)
	except requests.exceptions.MissingSchema:
		print 'The URL schema (e.g. http or https) is missing.'
		sys.exit()
	site_map = mapSite(url,url, [], {}, )
