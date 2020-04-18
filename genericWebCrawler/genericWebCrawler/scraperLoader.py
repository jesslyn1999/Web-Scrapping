from spiders.crawler import loadScraper
from pprint import pprint

def main():
    root = input("Root : ")
    allow_domains = input("Allowed Domain: ")
    depth = input("Max Depth : ")
    result = loadScraper(root, allow_domains, depth)
    # # print(result[0][2])
    # for paragraph in result:
    #     print("-------------------------------------")
    #     print("PAGE :", paragraph[0])
    #     print("[")
    #     for sentence in paragraph[2]:
    #         print("'"+sentence+"',")
    #     print("]")
    #     print("-------------------------------------")

if __name__ == '__main__':
    main()