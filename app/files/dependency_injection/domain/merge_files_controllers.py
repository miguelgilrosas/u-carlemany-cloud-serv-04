from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_storage_persistences import FileStoragePersistences
from app.files.domain.controllers.merge_files_controller import MergeFilesController
from app.files.dependency_injection.persistences.file_bo_persistences import FileBOPersistences


class MergeFilesControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        MergeFilesController,
        file_persistence_service=FileBOPersistences.carlemany(),
        file_storage_persistence_service=FileStoragePersistences.carlemany()
    )
