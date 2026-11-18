class Repository:
    def load(self, name): return 'global'

class OrderService:
    def __init__(self, repository):
        self.repository = repository
    def get(self, name):
        repository = Repository()  # fake injection: injected repository is ignored
        return repository.load(name)
