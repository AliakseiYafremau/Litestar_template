from typing import ClassVar
from uuid import UUID

from litestar import Response
from litestar.controller import Controller
from litestar.di import Provide
from litestar.handlers.http_handlers.decorators import delete, get, post
from litestar.status_codes import HTTP_400_BAD_REQUEST

from litestar_todo.todo.dto import (
    ListCreateScheme,
    ListReadDTO,
    NoteCreateScheme,
    NoteReadDTO,
)
from litestar_todo.todo.servicies import (
    ListService,
    NoteService,
    provide_list_service,
    provide_note_service,
)


class ListController(Controller):
    """Controller for managing todo lists."""

    path: ClassVar[str] = "/list"
    dependencies: ClassVar[dict[str, Provide]] = {
        "list_service": Provide(provide_list_service)
    }

    @get()
    async def get_list(
        self, list_id: UUID, list_service: ListService
    ) -> list[ListReadDTO]:
        """Endpoint for retrieving a single todo list."""
        return await list_service.get_by_id(list_id=list_id)

    @get("/all")
    async def get_all(self, list_service: ListService) -> list[ListReadDTO]:
        """Endpoint for retrieving all todo lists."""
        return await list_service.get_all()

    @post()
    async def create_list(
        self, data: ListCreateScheme, list_service: ListService
    ) -> ListReadDTO:
        """Endpoint for creating a new todo list."""
        return await list_service.create(title=data.title)

    @delete("/{list_id:uuid}")
    async def delete_list(self, list_id: UUID, list_service: ListService) -> None:
        """Endpoint for deleting a todo list."""
        await list_service.delete(list_id=list_id)


class NoteController(Controller):
    """Controller for managing todo notes."""

    path: ClassVar[str] = "/note"
    dependencies: ClassVar[dict[str, Provide]] = {
        "note_service": Provide(provide_note_service)
    }

    @get()
    async def get_note(
        self, note_id: UUID, note_service: NoteService
    ) -> list[NoteReadDTO]:
        """Endpoint for retrieving a single todo note."""
        return await note_service.get_by_id(note_id=note_id)

    @get("/all")
    async def get_all(self, note_service: NoteService) -> list[NoteReadDTO]:
        """Endpoint for retrieving all todo notes."""
        return await note_service.get_all()

    @post()
    async def create_note(
        self, data: NoteCreateScheme, note_service: NoteService
    ) -> NoteReadDTO:
        """Endpoint for creating a new todo note."""
        result = await note_service.create(text=data.text, list_id=data.list_id)
        if result is None:
            return Response(
                content={"message": "Invalid input"}, status_code=HTTP_400_BAD_REQUEST
            )
        return result

    @delete("/{note_id:uuid}")
    async def delete_note(self, note_id: UUID, note_service: NoteService) -> None:
        """Endpoint for deleting a todo note."""
        await note_service.delete(note_id=note_id)
