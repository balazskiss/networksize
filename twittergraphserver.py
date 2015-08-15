import networksize

# Twitter network sample
# 41.7 million user profiles, 1.47 billion social relations
importer = networksize.GraphImporter("/Users/balazs/Desktop/twitter_rv.net", 10000)
network = importer.importGraph(False, 100000)

if __name__ == '__main__':
    server = networksize.GraphServer(network)
    server.run()