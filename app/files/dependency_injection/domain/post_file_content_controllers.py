from dependency_injector import containers, providers

from app.files.dependency_injection.persistences.file_storage_persistences import FileStoragePersistences
from app.files.domain.controllers.post_file_content_controller import PostFileContentController
from app.files.dependency_injection.persistences.file_bo_persistences import FileBOPersistences


class PostFileContentControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        PostFileContentController,
        file_persistence_service=FileBOPersistences.carlemany(),
        file_storage_persistence_service=FileStoragePersistences.carlemany()
    )
