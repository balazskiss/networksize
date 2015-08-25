import networksize
import snap

if __name__ == '__main__':
    Rnd = snap.TRnd();
    network = snap.GenPrefAttach(1000000, 10, Rnd)
    server = networksize.GraphServer(network)
    server.run()