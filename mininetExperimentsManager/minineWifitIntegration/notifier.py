from asgiref.sync import async_to_sync
class ResultNotifier():
    _observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, subject):
        for observer in self._observers:
            async_to_sync(observer.update)(subject)