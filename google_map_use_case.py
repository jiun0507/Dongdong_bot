class GoogleMapUseCase:
    def __init__(self, repository) -> None:
        self._repo = repository
    def get(self):
        result = self._repo.get()
        print(result)
        return result