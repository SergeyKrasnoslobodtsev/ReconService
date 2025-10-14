
class ProcessIdNotFoundError(Exception):
    """Исключение, возникающее, когда процесс с указанным ID не найден."""
    def __init__(self, id: int):
        super().__init__(f"процесс с ID {id} не найден.")
        self.id = id

