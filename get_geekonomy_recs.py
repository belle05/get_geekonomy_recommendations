import urllib2
from bs4 import BeautifulSoup


def get_page(url):
	request = urllib2.Request(url)
	request.add_header('Accept-Encoding', 'utf-8')
	print "getting response..."
	response = urllib2.urlopen(request)
	return BeautifulSoup(response)


def load_all_pages():
	soups = {}
	url = 'https://geekonomy.net/category/%D7%A4%D7%A8%D7%A7%D7%99%D7%9D/'
	print "Going to fetch url %s ... " % (url)
	soups[0] = get_page(url)
	print "Page fetched successfully"
	can_load = True
	page_index = 1
	while(can_load):
		try:
			url = 'https://geekonomy.net/page/' + str(page_index+1) + '/'
			print "Going to fetch url %s ... " % (url)
			soups[page_index] = get_page(url)
			print "Page fetched successfully"
			page_index += 1
		except:
			can_load = False
	return soups

def get_all_links_by_episode(s):
	full_links = s.find_all('a')
	print "found all links"
	link_by_episode = {}
	episode_number = None
	for link in full_links:
		if 'geekonomy' in str(link) and '#' in link.get_text():
			episode_number = [int(v[1:]) for v in link.get_text().split(" ") if '#' in v][0]
			if not 'http' in str(link):
				continue
			link_by_episode[episode_number] = {'name': link.get_text(),
								   'episode_link': [v for v in str(link).split("\"") if 'http' in v][0],
								   'links': [],
								   }
		elif 'geekonomy' not in str(link) and episode_number is not None:
			link_by_episode[episode_number]['links'].append(link)
	return link_by_episode


def add_to_csv_table(csv, link_by_episode):
	for ep_num in link_by_episode.keys():
		for l in link_by_episode[ep_num]['links']:
			if 'twitter-timeline' not in str(l) and 'footer_blog' not in str(l) and 'Automattic' not in str(l) and 'cancel' not in str(l) and not 'utm' in str(l) and 'http' in str(l):
				link_name = l.get_text().replace(",","")
				link_url = [v for v in str(l).split("\"") if 'http' in v][0]
				print link_url
				csv.append([link_name, link_url, link_by_episode[ep_num]['name'].replace(",",""), link_by_episode[ep_num]['episode_link']])


soups = load_all_pages()
links_by_episode = {}
for s in soups.values():
	links = get_all_links_by_episode(s)
	links_by_episode.update(links)

csv = [['link_name', 'link_url', 'episode_name', 'episode_link']]
add_to_csv_table(csv, links_by_episode)
content = "\n".join([",".join(line) for line in csv]).encode('utf-8')
print content[:100]
f = open("./geekonomy_links.csv", "w")
f.write(content)
f.close()
print "tadam!"
