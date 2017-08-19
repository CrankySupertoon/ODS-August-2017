# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toonbase.ThreadPool
from Queue import Queue
from threading import Thread
import traceback

class ThreadPool(object):
    running = True
    workers = []
    queue = Queue()

    def __init__(self):
        self.createWorkerThreads()

    def worker(self):
        while self.running:
            item = self.queue.get()
            try:
                item()
            except:
                traceback.print_exc()

            self.queue.task_done()

    def createWorkerThreads(self):
        if self.workers:
            return
        self.running = True
        for i in xrange(4):
            thread = Thread(target=self.worker)
            thread.daemon = True
            thread.start()
            self.workers.append(thread)

    def stopThreads(self):
        self.workers = []
        self.running = False

    def addFunction(self, func):
        self.queue.put(func)