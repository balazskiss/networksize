import networksize

crawler = networksize.RemoteGraphCrawler("http://localhost:5000")
exp = networksize.Experiment(crawler, "edge", "twitter", 1000)
exp.run()