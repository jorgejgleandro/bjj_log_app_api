from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    tecnica_id: int = 1
    texto: str = "Cuidado! Risco de lesão no cotovelo!"
