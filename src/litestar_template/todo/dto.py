from uuid import UUID

import msgspec
from litestar.dto import DTOConfig, MsgspecDTO


class ListScheme(msgspec.Struct):
    """ListScheme class.

    Attributes:
        id (UUID): The ID of the list.
        title (str): The title of the list.

    """

    id: UUID
    title: str


class ListCreateScheme(msgspec.Struct):
    """ListCreateScheme class.

    Attributes:
        title (str): The title of the list.

    """

    title: str


class Note(msgspec.Struct):
    """Note class.

    Attributes:
        id (UUID): The ID of the note.
        text (str): The text of the note.
        list_id (UUID): The ID of the list to which the note belongs.

    """

    id: UUID
    text: str
    list_id: UUID


class ListReadDTO(MsgspecDTO[ListScheme]):
    """ListReadDTO class.

    Attributes:
        id (UUID): The ID of the list.
        title (str): The title of the list.

    """

    config = DTOConfig()
