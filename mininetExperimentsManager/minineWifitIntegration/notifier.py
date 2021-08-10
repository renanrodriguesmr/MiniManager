class ResultNotifier():
    _observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, subject):
        for observer in self._observers:
            observer.update(subject)