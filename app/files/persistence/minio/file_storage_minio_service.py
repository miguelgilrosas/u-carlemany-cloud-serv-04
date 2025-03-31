from minio import Minio

from app.files.domain.persistences.file_storage_interface import FileStorageInterface


class FileStorageMinioService(FileStorageInterface):
    def __init__(self):
        self.minio_client = Minio(
            "minio-server:9000",
            access_key="minio",
            secret_key="minio123",
            secure=False
        )
        self.bucket_name = "backend-carlemany-s3-bucket"

    def put_file(self, local_path: str, remote_path: str) -> str:
        self.minio_client.fput_object(
            self.bucket_name,
            object_name=remote_path,
            file_path=local_path
        )
        return "localhost:9000/" + self.bucket_name + "/" + remote_path

    def remove_file(self, remote_path: str):
        self.minio_client.remove_object(
            self.bucket_name,
            self.translate_path(remote_path=remote_path)
        )

    def copy_file(self, local_path: str, remote_path: str):
        self.minio_client.fget_object(
            self.bucket_name,
            object_name=self.translate_path(remote_path),
            file_path=local_path
        )

    def translate_path(self, remote_path: str) -> str:
        idx = remote_path.index(self.bucket_name) + len(self.bucket_name) + 1
        return remote_path[idx:]
