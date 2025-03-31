from pypdf import PdfMerger
import os

from app.files.domain.bo.file_bo import FileBO
from app.files.domain.persistences.exceptions import BadTokenException, NotFoundException
from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.domain.persistences.file_storage_interface import FileStorageInterface
from app.files.external.authentication.authentication_api import AuthenticationApi


class MergeFilesController:
    def __init__(
        self,
        file_persistence_service: FileBOInterface,
        file_storage_persistence_service: FileStorageInterface
    ):
        self.file_persistence_service = file_persistence_service
        self.file_storage_persistence_service = file_storage_persistence_service

    async def __call__(self, file_id1: int, file_id2: int, token: str) -> FileBO:
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        try:
            file1 = await self.file_persistence_service.get_file_by_id(file_id=file_id1)
            file2 = await self.file_persistence_service.get_file_by_id(file_id=file_id2)

        except NotFoundException:
            raise NotFoundException

        user_id = user['id']
        if user_id != file1.owner or user_id != file2.owner:
            raise BadTokenException

        new_file = FileBO(
            filename='Merged.pdf',
            path='',
            owner=user_id,
            desc='Merged file, created from "' + file1.filename + '" and "' + file2.filename + '"',
            number_of_pages=file1.number_of_pages + file2.number_of_pages
        )

        file1_path = "files/to_merge1.pdf"
        file2_path = "files/to_merge2.pdf"

        self.file_storage_persistence_service.copy_file(local_path=file1_path, remote_path=file1.path)
        self.file_storage_persistence_service.copy_file(local_path=file2_path, remote_path=file2.path)

        new_file = await self.file_persistence_service.post_file(new_file)
        new_file.path = "files/" + str(new_file.id) + ".pdf"

        merged = new_file.path
        pdfs = [file1_path, file2_path]
        merger = PdfMerger()
        for pdf in pdfs:
            merger.append(pdf)
        name = merged
        merger.write(name)
        merger.close()

        new_path = self.file_storage_persistence_service.put_file(
            local_path=new_file.path,
            remote_path=str(new_file.id) + ".pdf"
        )
        path_to_delete = new_file.path
        new_file.path = new_path
        await self.file_persistence_service.update_file(file_id=new_file.id, data=new_file)

        os.remove(path_to_delete)
        os.remove(file1_path)
        os.remove(file2_path)

        return new_file.id
