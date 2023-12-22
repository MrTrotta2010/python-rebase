# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

Este formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2023-12-21

### Corrigido
- Validação do objeto `app` para os Movimentos. Agora, ao criar um Movimento, são aceitos tanto os atributos separados `appCode` e `appData` quanto o objeto `'app': { 'code': str, 'data': any }`.

## [0.2.1] - 2023-12-18

### Corrigido
- Link do changelog na página do pacote no PyPi.

## [0.2.0] - 2023-12-18

### Adicionado
- Atributo `movement_ids` em `session`, contendo os IDs dos seus Movimentos. Esse campo é retornado nas requisições `fetch_sessions` e `find_session` quando o parâmetro `deep` está ausente ou tem o valor `False`.
- Indicador da versão atual no topo do arquivo `README.md`

## [0.1.3] - 2023-12-01

### Adicionado
- Arquivo de changelog;
- Link para o changelog na página do PyPi.

## [0.1.2] - 2023-12-01

### Alterado
- Renomeia o servidor de ReBase REST Server, ou RRS, para apenas **ReBaseRS**.
