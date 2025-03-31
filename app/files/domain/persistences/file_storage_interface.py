from abc import ABC, abstractmethod


class FileStorageInterface:
    @abstractmethod
    def put_file(self, local_path: str, remote_path: str) -> str:
        pass

    @abstractmethod
    def remove_file(self, remote_path: str):
        pass

    @abstractmethod
    def copy_file(self, local_path: str, remote_path: str):
        pass
