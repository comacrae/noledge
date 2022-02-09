from bs4 import BeautifulSoup as BS
from bs4 import Comment
import json
import re
import os

def get_file_names(dir_path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dir_path) for f in filenames if os.path.splitext(f)[1] == '.html']
    return result

def remove_abs_path(filename):
    return filename.split('/home/colinm/websites/scrape_3/www.cs.fsu.edu/')[1]

def exclude_files(regex, files, dir_path='/home/colinm/websites/scrape_3/www.cs.fsu.edu/'):
    verified = []
    for f in files:
        f = remove_abs_path(f)
        if re.match(regex, f) == None:
            f = os.path.join(dir_path, f)
            verified.append(f)
    print(f'Removed {len(files) - len(verified)} files')
    return verified

def get_soup(html_path):
    with open(html_path, 'r') as fp:
        return BS(fp,'lxml')

def get_comments(soup):
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    return comments

def get_url(soup):
    comments = get_comments(soup)
    url = ""
    regex = re.compile('.*Mirrored from .* by.*')
    for c in comments:
        string = str(c.string)
        if regex.match(string):
            url = string
    url_splits = url.split()
    for split in url_splits:
        if 'cs.fsu.edu' in split:
            url = split
    return url

def get_p_text(soup):
    text = ""
    p_tags = soup.find_all('p')
    for tag in p_tags:
        if tag.string is not None:
            text = text + tag.string + '\n'
    return text

def get_table_text(soup):
    text = ""
    table = soup.find(lambda tag: tag.name=='table' and tag.has_attr('id'))
    if table is not None:
        rows = table.find_all(lambda tag: tag.name=='tr')
        for row in rows:
            if row is not None:
                text = text + str(row.string) + '\n'
    return text

def get_list_text(soup):
    text = ""
    lists = soup.find_all(lambda tag: tag.name=='ul')
    if lists is not None:
        for ul in lists:
            lis = ul.find('li')
            if lis is not None:
                for li in lis:
                    text = text + str(li.string) + '\n'
    return text

def get_all_text(soup):
    header = '| Computer Science 850-644-2644 Facebook Twitter RSS Facebook Twitter RSS Florida State University Systems Group Admissions Why FSU CS Undergraduate Admissions Graduate Admissions Graduate Financial Support Policy and Statistics Financial Aid Academics Undergraduate Programs Combined BS/MS Pathways Graduate Programs Advising Financial Aid Women in Computer Science Research Research Area Coverage Graduate Faculty Research Areas Research Labs and Groups Current Research Funding Recent Completed Research Funding Technical Reports PhD Graduates People Faculty Staff Student Alumni Advisory Board Position Openings Department Chair’s Greeting Contacts & Addresses Department Awards Student Organizations Visitor Information Internal Resources News Department News Student Achievements E-Newsletters Select Page'
    text = soup.get_text(' ' ,strip=True)
    if re.match('.*404 Not Found.*|.*Access Denied.*', text):
        return None
    else:
        text = re.sub(header,'', text)
        text = re.sub('.* {2, }.*', ' ', text)
        text = re.sub('.*\n{2, }.*', '\n', text)
    return text

def get_all_text_by_tag(soup):
    text = ""
    if soup.p is not None:
        text = soup.p.get_text() + '\n'
    if soup.tr is not None:
        text = text + soup.tr.get_text() + '\n'
    if soup.li is not None:
        text = text + soup.li.get_text()
    
    return text

def print_files(files):
    for f in files:
        try:
            soup = get_soup(f)
            text = get_table_text(soup)#get_all_text(soup) + '\n' + get_table_text()
            if len(text) > 0:
                print('TEXT------------------------------')
                print(text)
                url = get_url(soup)
                print("URL-----------------------")
                print(url)
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        except UnicodeError:
            print(f"UNICODE ERROR: filename {f}")
    
def save_scraped_data(files, dir_path = '/home/colinm/Documents/hitm/scraped_documents/httrack_docs'):
    for f in files:
        soup = get_soup(f)
        text = get_all_text(soup)
        if text is not None:
            url = get_url(soup)
            f = remove_abs_path(f)
            if '/' in f:
                f = f.split('/index.html')[0]
                f = f.replace('/', '-')
                if '.html' in f:
                    f = f.replace('.html', '.json')
                else:
                    f = f + '.json'
                filename = os.path.join(dir_path, f)
                file_dict = {'url': url, 'text':text}
                with open(filename, "w+") as fp:
                    try:
                        json.dump(file_dict, fp)
                        print(f"File {f} created in {dir_path}")
                    except:
                        print(f"Failed to write {f}")
    return


def get_comparison_dicts(files,sort=False):
    comparisons = []
    sum_diffs = 0
    for f in files:
        comparison_dict = {'get_all_text':"", 'get_p_text':'', 'diff':0, 'url':''}
        soup = get_soup(f)
        url = get_url(soup)
        comparison_dict['url'] = url
        all_text = get_all_text(soup)
        specific_text = get_p_text(soup)
        if all_text is None:
            all_text =""
        if specific_text is None:
            specific_text = ""
        comparison_dict['get_all_text'] = get_all_text(soup)
        comparison_dict['specific_text'] = get_p_text(soup)
        diff = abs(len(all_text) - len(specific_text))
        comparison_dict['diff'] = diff
        sum_diffs = sum_diffs + diff
        comparisons.append(comparison_dict)
    print(f"avg diff:{sum_diffs/len(files)}")
    if sort:
        comparisons = comparisons.sort(reverse=True, key= lambda x: x['diff'])
    return comparisons

if __name__=="__main__":
    files = get_file_names('/home/colinm/websites/scrape_3/www.cs.fsu.edu/')
    files = exclude_files('forms/|_.*|reference/|sitemap|index(\d|\w)|.*feed.*|author/', files)
    save_scraped_data(files)
    
