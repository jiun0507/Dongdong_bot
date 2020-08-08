class GithubUseCase:
    def __init__(self, repository) -> None:
        self._repo = repository
    def get(self):
        return self._repo.get()