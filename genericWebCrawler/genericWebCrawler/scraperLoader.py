from spiders.urlExtractor import loadScraper

def main():
    root = input("Root : ")
    allow_domains = input("Allowed Domain: ")
    depth = input("Max Depth : ")
    result = loadScraper(root, allow_domains, depth)
    print(result)

if __name__ == '__main__':
    main()