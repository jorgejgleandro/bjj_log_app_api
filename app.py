from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Tecnica, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="BJJ Training Log API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tecnica_tag = Tag(name="Técnica", description="Adição, visualização e remoção de técnicas do banco de dados")
comentario_tag = Tag(name="Comentário", description="Adição de uma técnica cadastrada na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/tecnica', tags=[tecnica_tag],
          responses={"200": TecnicaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tecnica(form: TecnicaSchema):
    """Adiciona uma nova Técnica ao banco de dados

    Devolve uma representação das técnicas e respectivos comentários.
    """
    tecnica = Tecnica(
        nome=form.nome,
        descricao=form.descricao,
        nivel=form.nivel,
        video=form.video)
    logger.debug(f"Adicionando tecnica chamada: '{tecnica.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando tecnica
        session.add(tecnica)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado tecnica de nome: '{tecnica.nome}'")
        #return apresenta_tecnica(tecnica), 200
        return ""

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "tecnica de mesmo nome já salva na base :/"
        logger.warning(f"Erro ao adicionar tecnica '{tecnica.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar tecnica '{tecnica.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/tecnicas', tags=[tecnica_tag],
         responses={"200": ListagemTecnicasSchema, "404": ErrorSchema})
def get_tecnicas():
    """Faz a busca por todas as tecnicas cadastradas

    Devolve uma representação da listagem de tecnicas.
    """
    logger.debug(f"Coletando tecnicas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tecnicas = session.query(tecnica).all()

    if not tecnicas:
        # se não há tecnicas cadastradas
        return {"tecnicas": []}, 200
    else:
        logger.debug(f"%d tecnicas encontradas" % len(tecnicas))
        # Devolve a representação de tecnica
        print(tecnicas)
        return apresenta_tecnicas(tecnicas), 200


@app.get('/tecnica', tags=[tecnica_tag],
         responses={"200": TecnicaViewSchema, "404": ErrorSchema})
def get_tecnica(query: TecnicaBuscaSchema):
    """Faz a busca por um tecnica a partir do id da tecnica

    Devolve uma representação das tecnicas e respectivos comentários.
    """
    tecnica_id = query.id
    logger.debug(f"Coletando dados sobre tecnica #{tecnica_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    tecnica = session.query(tecnica).filter(tecnica.id == tecnica_id).first()

    if not tecnica:
        # se a tecnica não foi encontrada
        error_msg = "tecnica não encontrada no banco de dados :/"
        logger.warning(f"Erro ao buscar tecnica '{tecnica_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"tecnica econtrada: '{tecnica.nome}'")
        # Devolve a representação de tecnica
        return apresenta_tecnica(tecnica), 200


@app.delete('/tecnica', tags=[tecnica_tag],
            responses={"200": TecnicaDelSchema, "404": ErrorSchema})
def del_tecnica(query: TecnicaBuscaSchema):
    """Remove uma tecnica a partir do nome informado de tecnica

    Devolve uma mensagem de confirmação da remoção.
    """
    tecnica_nome = unquote(unquote(query.nome))
    print(tecnica_nome)
    logger.debug(f"Deletando dados sobre tecnica #{tecnica_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(tecnica).filter(tecnica.nome == tecnica_nome).delete()
    session.commit()

    if count:
        # Devolve a representação da mensagem de confirmação
        logger.debug(f"Removida tecnica #{tecnica_nome}")
        return {"mesage": "tecnica removido", "id": tecnica_nome}
    else:
        # se a tecnica não foi encontrada
        error_msg = "tecnica não encontrado no banco de dados :/"
        logger.warning(f"Erro ao remover tecnica #'{tecnica_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/comentario', tags=[comentario_tag],
          responses={"200": TecnicaViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona um novo comentário à tecnica cadastrada na base identificada pelo id

    Devolve uma representação das tecnicas e respectivos comentários.
    """
    tecnica_id  = form.tecnica_id
    logger.debug(f"Adicionando comentários à tecnica #{tecnica_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pela tecnica
    tecnica = session.query(tecnica).filter(tecnica.id == tecnica_id).first()

    if not tecnica:
        # se tecnica não encontrada
        error_msg = "tecnica não encontrada na base :/"
        logger.warning(f"Erro ao adicionar comentário à tecnica '{tecnica_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário à tecnica
    tecnica.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao tecnica #{tecnica_id}")

    # Devolve a representação de tecnica
    return apresenta_tecnica(tecnica), 200
