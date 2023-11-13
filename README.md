# Python ReBase
Este projeto é uma API escrita em Python para comunicação com o ReBase, um banco de dados de sessões de reabilitação física.

## Índice
- [Python ReBase](#python-rebase)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
    - [Sobre o ReBase](#sobre-o-rebase)
  - [Instalação](#instalação)
  - [Requisitos](#requisitos)
  - [Quick Start](#quick-start)
    - [Criando um Movimento](#criando-um-movimento)
    - [Criando uma Sessão](#criando-uma-sessão)
    - [Buscando Movimentos e Sessões](#buscando-movimentos-e-sessões)
    - [Atualizando e deletando](#atualizando-e-deletando)
  - [Tópicos Avançados](#tópicos-avançados)
    - [Filtragem](#filtragem)
    - [Paginação](#paginação)
  - [Exemplos](#exemplos)
  - [Documentação Completa](#documentação-completa)
    - [Módulos](#módulos)
      - [rebase\_client](#rebase_client)
      - [util](#util)
    - [Modelos](#modelos)
      - [APIResponse](#apiresponse)
      - [Movement](#movement)
      - [Register](#register)
      - [Rotation](#rotation)
      - [Session](#session)
    - [Erros](#erros)

## Visão Geral
O pacote Python ReBase contém classes-modelo para Sessões e Movimentos. A classe `api_response` modela de forma generalizada as respostas enviadas pelo `ReBase REST Server (RRS)`. O módulo `rebase_client` é responsável pelo envio de requisições ao RRS. Estão inclusas também algumas exceções personalizadas e funções utilitárias. Todos os módulos se encontram na pasta `src/python_rebase`.

### Sobre o ReBase
O ReBase, do inglês *Rehabilitation Database*, é um baco de dados dedicado ao armazenamento de movimentos corporais, com foco em reabilitação neurofuncional e neuromotora. Apesar do enfoque, o ReBase é capaz de armazenar qualquer tipo de movimento corporal gravado por qualquer técnica de captura de movimentos, desde que siga o padrão definido. Para isto serve a API Python ReBase!

Os **Movimentos** do ReBase representam os movimentos corporais capturados e são compostos por metadados, uma lista de *Articulações* e uma lista de **Registros**, que representam as rotações em X, y e z da Articulação a cada instante do Movimento. Os Movimentos podem pertencer a **Sessões**. Cada Sessão também contem metadados e pode conter múltiplos movimentos.

## Instalação
O PyRebase pode ser instalado pelo terminal através do **PyPi** com os comandos:
```
pip3 install python-rebase
```
ou
```
python3 -m pip install python-rebase
```

## Requisitos
* Esta biblioteca depende da biblioteca `requests`, utilizada para enviar requisições HTTP;
* O Python ReBase está disponível apenas para Python 3.10 ou superior.

## Quick Start
Para utilizar a API, basta importar a biblioteca no começo do seu arquivo .py

### Criando um Movimento
```Python
from python_rebase.movement import Movement
from python_rebase import rebase_client

# Crie um objeto Movement
movement = Movement({
    'label': 'MyMovement',
    'fps': 30, # Varia conforme sua aplicação
    'professionalId': 'Prof',
    'articulations': ['1', '2']
})

# Adicione os Registros ao Movimento
# Cada registro representa um "frame" do movimento
# Os registros contêm as rotações de cada articulação em um dado momento 
# Apesar de o Python ReBase incluir classes-modelo para os Registros e para Rotações, os métodos também aceitam dicionários e listas como parâmetros
movement.add_register(Register(
    {
        '1': Rotation(1.0, 1.0, 1.0), # Rotações da articulação "1"
        '2': [2.0, 2.0, 2.0] # Rotações da articulação "2"
    }
))

# Utilize o módulo rebase_client para inserir o movimento
response = rebase_client.insert_movement(movement)
print(f'Inserted: {response}')
```

### Criando uma Sessão
```Python
from python_rebase.session import Session

# Crie um objeto Sessão.
# A Sessão pode ser criada vazia ou com Movimentos, sejam eles da classe Movement ou dicionários simples
session = Session({
    'title': 'Teste de Sessão',
    'professionalId': 'Prof',
    'patientId': 'Pat',
    'movements': [
        # Da mesma forma, os Movimentos podem ser criados já com Registros
        Movement({
            'label': 'MyMovement',
            'fps': 30,
            'articulations': ['1', '2'],
            'registers': [
                Register({
                    '1': Rotation(1.0, 1.0, 1.0),
                    '2': Rotation(2.0, 2.0, 2.0)
                })
            ]
        }),
        {
            'label': 'MyMovement',
            'fps': 30,
            'articulations': ['1', '2'],
            'registers': [
                {
                    '1': [1.0, 1.0, 1.0],
                    '2': [2.0, 2.0, 2.0]
                }
            ]
        }
    ]
})

response = rebase_client.insert_session(session)
```

### Buscando Movimentos e Sessões
```Python
# É possível encontrar um único Movimento ou listar vários
response = rebase_client.find_movement(id)
print(f'Movimento: {response.movement}')

# A listagem permite filtros e suporta paginação
# Os filtros possíveis são: professional_id (id do profissional de saúde), patient_id (id do paciente),
# movement_label (identificação do movimento), articulations (articulações incluídas no movimento)
response = rebase_client.fetch_movements(professional_id='professional', patient_id='patient', page=1, per=10)
print(f'Movimentos: {response.movements}')

# Da mesma forma, as Sessões podem ser buscadas individualmente ou listadas
response = rebase_client.find_session(id)
print(f'Sessão: {response.session}')

# Os filtros suportados pela listagem de Sessão são: professional_id e patient_id.
# Também são aceitos os filtros movement_label e articulations, mas estes filtram os movimentos das Sessões
response = rebase_client.fetch_sessions(professional_id='professional', patient_id='patient', page=1, per=10)
print(f'Sessões: {response.sessions}')
```

### Atualizando e deletando
```Python
# São disponibilizados métodos para deletar e excluir Movimentos e Sessões
response = rebase_client.update_movement(updatedMovement)
response = rebase_client.delete_movement(id)

response = rebase_client.update_session(updatedSession)
response = rebase_client.delete_session(id)
```

## Tópicos Avançados
A seguir, serão abordados dois assuntos relevantes para as requisições de listagem: **filtragem** e **paginação**.

### Filtragem
As requisições de listagem do ReBase, de Movimentos ou de Sessões, suportam alguns filtros, listados e explicados a seguir.

Listagem de Movimentos:
* **professional_id:** recebe uma `string` que representa o ID do profissional de saúde responsável pelo Movimento;
* **patient_id:** recebe uma `string` que representa o ID do paciente que executou o Movimento;
* **movement_label:** recebe uma `string` que representa a propriedade `label` do Movimento;
* **articulations:** recebe uma lista de `strings` que representam as articulações trabalhadas no Movimento.

Listagem de Sessões:
* **professional_id:** recebe uma `string` que representa o ID do profissional de saúde responsável pela Sessão;
* **patient_id:** recebe uma `string` que representa o ID do paciente que avaliado durante a Sessão.

A listagem de Sessões pode recebe ainda dois filtros adicionais. Estes, no entanto, não filtrarão a lista de Sessões em si, mas sim as listas de Movimentos das Sessões. São eles:
* **movement_label:** recebe uma `string` que representa a propriedade `label` do Movimento;
* **articulations:** recebe uma lista de `strings` que representam as articulações trabalhadas no Movimento.

Estes filtros podem ser úteis em alguns casos específicos. Um exemplo de uso: listar as Sessões de um paciente específico, mas incluir apenas os Movimentos que trabalharam um grupo específico de articulações.

Vale notar, por fim, que todos os filtros são **aditivos**, ou seja, ao utilizar `n` múltiplos filtros, serão retornados os documentos que satisfaçam **todos** os filtros, ou seja, os documentos que satisfaçam o filtro 1 **E** o filtro 2 **E** ... **E** o filtro n. 

### Paginação
As requisições de listagem, tanto de Movimentos quanto de Sessões, também suportam paginação. Utilizando paginação, elimina-se a necessidade de carregar todos os items de uma listagem de uma só vez, o que pode significar um ganho de velocidade e desempenho para uma aplicação. O RRS suporta dois tipos de paginação: baseada em **per e page** e baseada em **IDs**.

O primeiro tipo utiliza dois parâmetros: `per`, que representa a quantidade de itens presentes em cada página, e `page`, que representa qual página deve ser carregada. Desta forma, supondo que quiséssemos carregar 10 elementos por página, para carregar a primeira página usaríamos `{ per: 10, page: 1 }` e receberíamos os primeiros 10 itens da lista. Para carregar a segunda página usaríamos `{ per: 10, page: 2 }` e receberíamos os 10 itens seguintes e assim por diante. Este método é simples de se utilizar e de se entender e permite o carregamento de qualquer página, porém possui uma desvantagem: para recuperar uma página `n`, é necessário recuperar todas as páginas anteriores, o que faz com que as requisições fiquem mais lentas conforme o número `n` da página cresce. Para mitigar este problema, é possível utilizar a paginação baseada em IDs.

A paginação baseada em IDs também depende de dois parâmetros: `per`, a quantidade de itens por página, e `previous_id`, o ID do último item da página anterior. Pela forma como o banco de dados do ReBase é modelado, as listas de Movimentos e de Sessões são ordenadas pelos IDs dos documentos, que são sequenciais. Ou seja, se quisermos recuperar os 10 itens seguintes a um item `i`, basta recuperar os primeiros 10 itens cujo ID seja maior do que o ID de `i`. Explorando essa característica, é possível implementar um método de paginação que permite que todas as páginas sejam recuperadas em tempos equivalentes. Desta forma, para recuperar a primeira página usaríamos `{ per: 10, previous_id: null }`, já que não existe uma página anterior. Supondo que o ID do último item da primeira página seja "ABC", para recuperar a segunda página usaríamos `{ per: 10, previous_id: "ABC" }`. Apesar de tudo, este método de paginação também tem uma desvantagem: para recuperar uma página específica, é necessário ter recuperado todas as páginas anteriores a ela, já que é preciso saber os IDs dos documentos que estão contidos nelas.

Assim, cabe ao desenvolvedor analisar sua aplicação e decidir qual método de paginação deverá ser utilizado (ou se a paginação é mesmo necessária). Aplicações que devem permitir a qualquer momento o acesso a qualquer página, deverão usar a paginação baseada em per e page. Por outro lado, para uma aplicação que precisa exibir uma lista com scroll infinito, por exemplo, na qual os itens são carregados sequencialmente, se beneficiará mais do método baseado em IDs. Para mais informações, [este artigo](https://medium.com/swlh/mongodb-pagination-fast-consistent-ece2a97070f3) pode ser útil. 

## Exemplos
Esta biblioteca inclui a pasta `examples`, que inclui alguns códigos-exemplo básicos de utilização da API.

## Documentação Completa
A seguir, estão incluídas tabelas e descrições detalhando todas as classes e módulos da API Python ReBase.

### Módulos

#### rebase_client
Este módulo é responsável por toda a comunicação com o RRS. Seus métodos retornam objetos da classe [APIResponse](#apiresponse). Exemplos de uso podem ser encontrados na seção [Quick Start:](#quick-start). 

**Métodos:**
| Método              | Retorno                         | Parâmetros                           |
| :------------------ | :------------------------------ | -----------------------------------: |
| **fetch_movements** | **[APIResponse](#apiresponse)** |**professional_id: str = "", patient_id: str = "", movementLabel: str = "", articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = ""** |
| Recupera uma lista de Movimentos armazenados no RRS. Suporta diversos filtros e paginação    |
| **find_movement**   | **[APIResponse](#apiresponse)** | **id: str, legacy: bool = False**    |
| Recupera um Movimento específico a partir do ID. O parâmetro `legacy`, se `True`, retorna o Movimento no formato antigo do ReBase |
| **insert_movement**  | **[APIResponse](#apiresponse)** | **movement: [Movement](#movement)** |
| Insere um Movimento no ReBase                                                                |
| **update_movement**  | **[APIResponse](#apiresponse)** | **movement: [Movement](#movement)** |
| Atualiza um Movimento já existente no ReBase                                                 |
| **delete_movement** | **[APIResponse](#apiresponse)** | **id: str**                          |
| Exclui um Movimento do ReBase                                                                |
| **fetch_sessions**  | **[APIResponse](#apiresponse)** | **professional_id: str = "", patient_id: str = "", movement_label: str = "", articulations: list = None, legacy: bool = False, page: int = 0, per: int = 0, previous_id: str = ""** |
| Recupera uma lista de Sessões armazenadas no RRS. Suporta diversos filtros e paginação       |
| **find_session**    | **[APIResponse](#apiresponse)** | **id: str, legacy: bool = False**    |
| Recupera uma Sessão específica a partir do ID. O parâmetro `legacy`, se `True`, retorna a Sessão no formato antigo do ReBase |
| **insert_session**  | **[APIResponse](#apiresponse)** | **session: [Session](#session)**     |
| Insere uma Sessão no ReBase                                                                  |
| **update_session**  | **[APIResponse](#apiresponse)** | **session: [Session](#session)**     |
| Atualiza uma Sessão já existente no ReBase                                                   |
| **delete_session**  | **[APIResponse](#apiresponse)** | **id: str, deep: bool = False**      |
| Exclui uma Sessão do ReBase                                                                  |

#### util
O módulo `util` contém diversos métodos utilitários. 

**Métodos:**
| Método                      | Retorno  | Parâmetros                       |
| :-------------------------- | :------- | -------------------------------: |
| **is_valid_str**            | **bool** | **value: any**                   |
| Retorna `True` se `value` for uma string válida (uma instância da classe `str`). Caso contrário, retorna `False` |
| **is_valid_number**         | **bool** | **value: any**                   |
| Retorna `True` se `value` for um número válido (uma instância da classe `int` ou da classe `float`). Caso contrário, retorna `False` |
| **is_valid_id**             | **bool** | **value: any**                   |
| Retorna `True` se `value` for considerado um id válido para o ReBase (uma string válida não vazia ou um inteiro maior que 0). Caso contrário, retorna `False` |
| **is_valid_movement_field** | **bool** | **field: str, value: any**       |
| Retorna `True` se `field` for um campo válido para um Movimento do ReBase e se `value` for um valor válido para esse campo. Retorna `False` caso contrário |
| **is_valid_session_field**  | **bool** | **field: str, value: any**       |
| Retorna `True` se `field` for um campo válido para um Movimento do ReBase e se `value` for um valor válido para esse campo. Retorna `False` caso contrário |
| **exclude_keys_from_dict**  | **None** | **dictionary: dict, keys: list** |
| Remove uma dada lista de chaves de um dado dicionário                     |

### Modelos

#### APIResponse
A classe APIResponse modela uma resposta generalizada do servidor RRS.

**Atributos:**
| Atributo          | Tipo                   |
| :---------------- | ---------------------: |
| **response_type** | **ResponseType(Enum)** |
| Tipo da requisição enviada. Valores possíveis: { 0: FetchMovements, 1: FindMovement, 3: InsertMovement, 4: UpdateMovement, 5: DeleteMovement, 6: FetchSessions, 7: FindSession, 8: InsertSession, 9: UpdateSession, 10: DeleteSession, 11: APIError } |
| **status**        | **int**                |
| Status da resposta. 0 representa sucesso e qualquer outro valor representa um erro |
| **code**          | **int**                |
| Código HTTP da resposta (E.g. 200, 201, 404, etc. ) |
| **success**       | **bool**               |
| Diz se a requisição foi bem sucedida ou não. Em outras palavras, diz se status == 0 |

**Métodos:**
| Método            | Retorno  | Parâmetros   |
| :---------------- | :------- | ------------ |
| **has_data**      | **bool** | **key: str** |
| Retorna `True` se o atributo `key` estiver presente nos dados da resposta e `False` caso contrário |
| **get_data**      | **bool** | **key: str** |
| Retorna o valor do atributo `key` nos dados da resposta. Os possíveis atributos são: 'message', 'HTMLError', 'error', 'warning', 'movements', 'movement', 'sessions', 'session', 'deletedId', 'deletedCount' |
| **has_meta_data** | **bool** | **key: str** |
| Retorna `True` se o atributo `key` estiver presente nos metadados da resposta e `False` caso contrário |
| **get_meta_data** | **bool** | **key: str** |
| Retorna o valor do atributo `key` nos metadados da resposta. Os possíveis atributos são: 'current_page', 'next_page', 'total_count', 'total_page_count' |

#### Movement
Modela um Movimento do ReBase.

**Atributos:**
| Atributo                | Tipo                        |
| :---------------------- | --------------------------: |
| **id**                  | **str**                     |
| ID do Movimento                                       |
| **label**               | **str**                     |
| Label, ou etiqueta, de identificação do Movimento. Normalmente representa uma categoria ou grupo de Movimentos |
| **description**         | **str**                     |
| Descrição do Movimento                                |
| **device**              | **str**                     |
| Dispositivo responsável pela captura do Movimento (E.g. Kinect, MediaPipe, etc.) |
| **fps**                 | **float**                   |
| Quantidade de quadros por segundo do Movimento        |
| **duration**            | **float**                   |
| Duração do Movimento                                  |
| **number_of_registers** | **int**                     |
| Quantidade de Registros presentes no Movimento (os Registros serão descritos a seguir) |
| **articulations**       | **list**                    |
| Articulações utilizadas pelo Movimento. As Articulações são identificadas por strings arbitrárias definidas pelo usuário da API. Cabe a cada desenvolvedor definir e seguir seu padrão. Desta maneira, o ReBase pode armazenar movimentos com um conjunto variável de Articulações |
| **insertion_date**      | **str**                     |
| Data de inserção do Movimento                         |
| **update_date**         | **str**                     |
| Data da última atualização do Movimento               |
| **session_id**          | **str**                     |
| ID da Sessão à qual o Movimento pertence              |
| **professional_id**     | **str**                     |
| Identificação do profissional da saúde responsável pela captura do Movimento |
| **app_code**            | **str**                     |
| Código da aplicação que gerou o Movimento. Um código arbitrário definido pelos desenvolvedores da aplicação |
| **app_data**            | **str**                     |
| Dados arbitrários utilizados pela aplicação que gerou o Movimento. Pode ser utilizado pelos usuários da API para armazenar dados no formato que quiserem, como um json ou uma string |
| **patient_id**          | **str**                     |
| Identificação anônima do paciente que realizou o Movimento |
| **registers**           | **[[Register](#register)]** |
| Lista de Registros que representam o Movimento em si. Ao adicionar um registro a um Movimento, mesmo que ele seja um dicionário, será automaticamente convertido à classe [Register](#register) |

**Métodos:**
| Método                       | Retorno  | Parâmetros                          |
| :--------------------------- | :------- | ----------------------------------: |
| **add_register**             | **None** | **register: [Register](#register)** |
| Adiciona um novo Registro ao Movimento                                        |
| **to_dict**                  | **dict** | **exclude: list**                   |
| Converte o Movimento para um dicionário. Recebe uma lista de propriedades a serem ignoradas |
| **to_json**                  | **str**  | **update: bool = False**            |
| Converte o Movimento para json. O parâmetro update modifica o json gerado: para requisições de criação use update como `False` e para requisições de atualização use update como `True` |

#### Register
Modela um Registro do ReBase, essencialmente um quadro, ou um frame, de um Movimento. Um Registro contém as rotações nos eixos x, y e z de cada Articulação do Movimento em um determinado instante. A classe Register se comporta como um dicionário, ou seja, cada articulação deve ser acessada através do operador `[]` (ex: `register['articulation1'] = Rotation(1.0, 2.0, 3.0)`)

**Atributos:**
| Atributo               | Tipo              |
| :--------------------- | ----------------: |
| **articulation_count** | **int**           |
| A quantidade de Articulações presentes no Registro |
| **articulations**      | **readonly list** |
| A lista das Articulações presentes no Registro |
| **is_empty**           | **bool**          |
| Indica se o registro está vazio, ou seja, não contem nenhuma Articulação |

**Métodos:**
| Método              | Retorno  | Parâmetros |
| :------------------ | :------- | ---------- |
| **to_dict**         | **dict** |            |
| Converte o Registro em um dicionário        |

#### Rotation
Representa um conjunto de rotações de uma Articulação.

**Atributos:**
| Atributo | Tipo       |
| :------- | ---------: |
| **x**    | **number** |
| A rotação no eixo X   |
| **y**    | **number** |
| A rotação no eixo Y   |
| **z**    | **number** |
| A rotação no eixo Z   |

**Métodos:**
| Método        | Tipo     | Parâmetros |
| :------------ | :------- | ---------: |
| **to_list**   | **list** |            |
| Converte a Rotação para uma lista     |
| **to_tuple**  | **dict** |            |
| Converte a Rotação para uma tupla     |

#### Session
Modela uma Sessão do ReBase.

**Atributos:**
| Atributo                       | Tipo                       |
| :----------------------------- | -------------------------: |
| **id**                         | **str**                    |
| ID da Sessão                                                |
| **title**                      | **str**                    |
| Título da Sessão                                            |
| **description**                | **str**                    |
| Descrição da Sessão                                         |
| **professional_id**            | **str**                    |
| Identificação do profissional de saúde responsável pela captura da Sessão |
| **patient_session_number**     | **int**                     |
| Número da Sessão do paciente (Ex.: 1 para a primeira Sessão, 2 para a segunda, etc.) |
| **insertion_date**             | **str**                     |
| Data de criação da Sessão                                    |
| **update_date**                | **str**                     |
| Data de atualização da Sessão                                |
| **patient_id**                 | **str**                     |
| Identificação anônima do paciente que realizou a Sessão      |
| **patient_age**                | **int**                     |
| Idade do paciente                                            |
| **patient_height**             | **float**                   |
| Altura do paciente                                           |
| **patient_weight**             | **float**                   |
| Peso do paciente                                             |
| **main_complaint**             | **str**                     |
| Queixa principal do paciente                                 |
| **history_of_current_disease** | **str**                     |
| Histórico da condição atual do paciente                      |
| **history_of_past_disease**    | **str**                     |
| Histórico de condições anteriores do paciente                |
| **diagnosis**                  | **str**                     |
| Diagnóstico dado ao paciente pelo profissional de saúde      |
| **related_diseases**           | **str**                     |
| Condições relacionadas à do paciente                         |
| **medications**                | **str**                     |
| Medicações das quais o paciente faz uso                      |
| **physical_evaluation**        | **str**                     |
| Avaliação física do paciente realizada pelo profissional     |
| **number_of_movements**        | **int**                     |
| Número de Movimentos pertencentes à Sessão                   |
| **duration**                   | **float**                   |
| Duração total da Sessão. Equivale à soma das durações dos seus Movimentos |
| **movements**                  | **[[Movement](#movement)]** |
| Lista dos Movimentos pertencentes à Sessão                   |

**Métodos:**
| Método      | Tipo     | Parâmetros                                |
| :---------- | :------- | ----------------------------------------: |
| **to_dict** | **dict** | **exclude: list, movement_exclude: list** |
| Converte a Sessão para um dicionário. Recebe duas listas: uma lista de propriedades a serem ignoradas e uma outra lista de propriedades a serem ignoradas na conversão dos seus Movimentos |
| **to_json** | **str**  | **update: bool = False**                  |
| Converte a Sessão para json. O parâmetro update modifica o json gerado: para requisições de criação use update como `False` e para requisições de atualização use update como `True` |

### Erros
A biblioteca Python ReBase define alguns erros personalizados para os modelos de dados e casos de uso do ReBase. São eles:

1. **MismatchedArticulationsError:** disparado ao criar um Movimento com Registros que tenham articulações diferentes das definidas no Movimento ou ao adicionar a um Movimento um Registro que tenha articulações diferentes das do Movimento;
2. **MissingAttributeError:** disparado ao tentar enviar uma requisição ao RRS e algum parâmetro não tenha um atributo obrigatório;
3. **RepeatedArticulationError:** disparado ao criar um Movimento ou um Registro com uma lista de articulações que contenha articulações repetidas.
