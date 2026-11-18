class OrderService:
    def __init__(self, repository): self.repository = repository
    def get(self, name): return self.repository.load(name)
