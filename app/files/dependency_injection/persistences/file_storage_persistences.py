from dependency_injector import containers, providers

from app.files.persistence.minio.file_storage_minio_service import FileStorageMinioService


class FileStoragePersistences(containers.DeclarativeContainer):
    minio = providers.Singleton(FileStorageMinioService)
    carlemany = minio
