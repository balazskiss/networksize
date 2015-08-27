import networksize

if __name__ == '__main__':
    # Twitter network sample
    # 41.7 million user profiles, 1.47 billion social relations
    importer = networksize.GraphImporter("/Volumes/Blaze\'s Disk/twitter/twitter_rv.net", 10000)
    network = importer.import_graph(False, 30000000)
    server = networksize.GraphServer(network)
    server.run()