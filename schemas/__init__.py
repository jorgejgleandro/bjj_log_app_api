from schemas.comentario import ComentarioSchema

from schemas.tecnica import TecnicaSchema, TecnicaBuscaSchemaPorID, TecnicaBuscaSchemaPorNome, TecnicaBuscaSchemaPorTermo, TecnicaViewSchema, \
                            ListagemTecnicasSchema, TecnicaDelSchema, \
                            apresenta_tecnica, apresenta_tecnicas
                            
from schemas.aluno import   AlunoSchema, AlunoBuscaSchemaPorID, AlunoBuscaSchemaPorNome, AlunoBuscaSchemaPorTermo, AlunoViewSchema, \
                            ListagemAlunosSchema, AlunoDelSchema, \
                            apresenta_aluno, apresenta_alunos

from schemas.error import ErrorSchema
