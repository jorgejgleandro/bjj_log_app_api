from pydantic import BaseModel
from typing import Optional, List
from model.tecnica import Tecnica, NivelEnum
from flask import jsonify
import jsonpickle

from schemas import ComentarioSchema


class TecnicaSchema(BaseModel):
    """ Define como uma nova Tecnica a ser inserida deve ser representada
    """
    nome: str = "Chave reta"
    descricao: str = "Chave reta na montada"
    nivel: NivelEnum = "Iniciante"
    video: str = "https://youtu.be/TEV76y9ijHQ?si=rB_qrRT4KaI-lQP2"


class TecnicaBuscaSchemaPorNome(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Tecnica.
    """
    nome: str = "Chave reta"

class TecnicaBuscaSchemaPorID(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no ID da Tecnica.
    """
    id: int = 1

class ListagemTecnicasSchema(BaseModel):
    """ Define como uma listagem de tecnicas será devolvida.
    """
    tecnicas:List[TecnicaSchema]


def apresenta_tecnicas(tecnicas: List[Tecnica]):
    """ Devolve uma representação da tecnica seguindo o schema definido em
        TecnicaViewSchema.
    """
    result = []
    for tecnica in tecnicas:
        result.append({
            "nome": tecnica.nome,
            "descricao": tecnica.descricao,
            "nivel": jsonpickle.encode(tecnica.nivel),
            "video": tecnica.video,
        })

    return {"tecnicas": result}


class TecnicaViewSchema(BaseModel):
    """ Define como um tecnica será devolvida: tecnica + comentários.
    """
    id: int = 1
    nome: str = "Chave Reta"
    descricao: str = "Chave reta na montada"
    nivel: NivelEnum = "Iniciante"
    video: str = "https://youtu.be/TEV76y9ijHQ?si=rB_qrRT4KaI-lQP2"
    total_comentarios: int = 1
    comentarios:List[ComentarioSchema]


class TecnicaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_tecnica(tecnica: Tecnica):
    """ Devolve uma representação da tecnica seguindo o schema definido em
        TecnicaViewSchema.
    """
    return {
        "id": tecnica.id,
        "nome": tecnica.nome,
        "descricao": tecnica.descricao,
        "nivel": jsonpickle.encode(tecnica.nivel),
        "video": tecnica.video,
        "total_comentarios": len(tecnica.comentarios),
        "comentarios": [{"texto": c.texto} for c in tecnica.comentarios]
    }
