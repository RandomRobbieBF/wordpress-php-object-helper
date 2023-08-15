#!/usr/bin/env python3
import argparse
import requests
import concurrent.futures
import os
from tqdm import tqdm
session = requests.Session()
http_proxy = ""

#
# wordpress-php-object-helper - got a plugin with a known php object exploit but no lib to use?
# use this script to bruteforce all the plugins on the system and have it give you suggestions of with lib to use and which plugin is helping.
#
# By RandomRobbieBF
#





MAX_THREADS = 10  # Set the maximum number of concurrent threads

# Set the desired user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
session.headers.update({"User-Agent": user_agent})


def check_gcc(results,plugin_slug):
    plugin_slug = plugin_slug.replace("/","")
    print("Checking for known libraries for phpgcc inside vendor folder.")
    search_strings = ["zend","yii","PHPExcel","WooCommerce","Guzzle","Dompdf","ThinkPHP","TCPDF","Symfony","SwiftMailer","Spiral","Snappy","Smarty","slim","Pydio","PHPWord","PHPSecLib","PHPCSFixer","Phalcon","Monolog","Magento","Laravel","Laminas","Kohana","Drupal","Doctrine","CodeIgniter4","CakePHP"]
    # Loop through each string in the search_strings array
    for st in search_strings:
        # Check if the string is present in the results variable
        if st.lower() in results.lower():
           # If the string is found, print it
           print("You may be able to use the following "+st+" with this "+plugin_slug+" plugin.")

def check_url(url, line):
    full_url = url + line.strip()

    response = session.get(full_url, verify=False)  # Disabling SSL warnings

    if response.status_code == 200 and 'DOCTYPE' not in response.text and 'Stable tag' in response.text:
        return full_url
    return None
    
def check_svn(valid_urls,url):
    for plugin_slug in valid_urls:
        plugin_slug = plugin_slug.replace(url,"")
        plugin_slug = plugin_slug.replace("/wp-content/plugins/","")
        plugin_slug = plugin_slug.replace("readme.txt","")
        response = session.get("http://plugins.svn.wordpress.org/"+plugin_slug+"trunk/vendor/", verify=False)
        if response.status_code == 200:
           print("Vendor Folder found at "+response.url+"")
           check_gcc(response.text,plugin_slug)
        response2 = session.get("http://plugins.svn.wordpress.org/"+plugin_slug+"trunk/includes/vendor/", verify=False)
        if response2.status_code == 200: 
           print("Vendor Folder found at "+response2.url+"")
           check_gcc(response2.text,plugin_slug)
  
    
    

def process_file(url, filename):
    valid_urls = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_url = {executor.submit(check_url, url, line): line for line in lines}

        with tqdm(total=len(lines), desc='Processing URLs') as pbar:
            for future in concurrent.futures.as_completed(future_to_url):
                line = future_to_url[future]
                result = future.result()
                if result is not None:
                    valid_urls.append(result)
                pbar.update(1)

    return valid_urls
    



def main():
    parser = argparse.ArgumentParser(description='Check URLs for specific requirements')
    parser.add_argument('--url', '-u', required=True, type=str, help='Base URL')
    parser.add_argument('--filename', '-f', required=True, type=str, help='Input text file')

    args = parser.parse_args()

    requests.packages.urllib3.disable_warnings()  # Disable SSL warnings
    session.proxies = {'http': http_proxy, 'https': http_proxy}  # Set up proxy
    valid_urls = process_file(args.url, args.filename)

    print('Found the following plugins:')
    for urlz in valid_urls:
        print(urlz)
    print("Checking Wordpress SVN for vendor folder.")
    url = args.url
    check_svn(valid_urls,url)    

if __name__ == '__main__':
    main()
