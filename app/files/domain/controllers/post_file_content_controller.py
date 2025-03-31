from fastapi import UploadFile
import os

from app.files.domain.persistences.file_bo_interface import FileBOInterface
from app.files.domain.persistences.exceptions import BadTokenException, NotFoundException
from app.files.domain.persistences.file_storage_interface import FileStorageInterface
from app.files.external.authentication.authentication_api import AuthenticationApi


class PostFileContentController:
    def __init__(
            self,
            file_persistence_service: FileBOInterface,
            file_storage_persistence_service: FileStorageInterface
    ):
        self.file_persistence_service = file_persistence_service
        self.file_storage_persistence_service = file_storage_persistence_service

    async def __call__(self, file_id: int, token: str, input_file: UploadFile) -> dict[str, str]:
        auth_api = AuthenticationApi()
        try:
            user = await auth_api.auth_check(auth=token)

        except BadTokenException:
            raise BadTokenException

        try:
            file_data = await self.file_persistence_service.get_file_by_id(file_id=int(file_id))

        except NotFoundException:
            raise NotFoundException

        if file_data.owner != user['id']:
            raise BadTokenException

        prefix = 'files/'
        filename = str(file_id) + '.pdf'
        path = prefix + filename
        with open(path, "wb") as buffer:
            while chunk := await input_file.read(8192):
                buffer.write(chunk)

        new_path = self.file_storage_persistence_service.put_file(path, filename)
        os.remove(path)
        file_data.path = new_path

        await self.file_persistence_service.update_file(file_id=file_id, data=file_data)

        return {"path": new_path}
