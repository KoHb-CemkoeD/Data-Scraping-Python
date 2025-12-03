from DataCollector import collect_data, filter_data

if __name__ == '__main__':
    with open("foxtrot_urls.txt") as fx:
        links = fx.read()
    # collect_data(links.split('\n')[342:])
    filter_data()
