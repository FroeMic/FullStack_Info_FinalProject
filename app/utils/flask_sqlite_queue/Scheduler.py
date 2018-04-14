
from threading import Thread
from time import sleep

class Scheduler(object):

    def __init__(self):
        self.interval = 1.0 #by default check every second
        self._running = False
        self._thread = None
        self._queues = {}

    def _notify(self):
        ''' Notifies all register queues '''
        for key, queue in self._queues.items():
            queue.run_due_jobs()

    def _cycle(self):
        while self._running:
            self._notify()
            sleep(self.interval)

    def is_running():
        ''' Returns whether the scheduler is currently running '''
        return self._running
        
    def stop(self, immediate = False):
        ''' Stops the Scheduler '''
        if self._thread:
            self._thread.exit()
            self._thread = None
        self._running = False

        if immediate:
            for key, queue in self._queues.items():
                queue.abort_running_jobs()       

    def start(self):
        ''' Starts the Scheduler if not started yet '''
        self._running = True
        if self._thread and self._thread.is_alive():
            pass
        elif self._thread and not self._thread.is_alive():
            self._thread.exit()
            self._thread = Thread(target=self._watch)
            self._thread.start()
        else:
            self._thread = Thread(target=self._cycle)
            self._thread.start()
        
    def register(self, queue):
        self._queues[id(queue)] = queue

    def deregister(self, queue):    
        if self._queues.get(id(queue)) is not None:
            self._queues.pop(id(queue))
