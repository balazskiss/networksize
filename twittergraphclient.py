import networksize

if __name__ == '__main__':
    crawler = networksize.RemoteGraphCrawler("http://localhost:5005")
    exp = networksize.Experiment(crawler, "node", "results/twitterds30m", 1000)
    exp.run()
