# TDD Project

## O que é TDD?
TDD é uma sigla para `Test Driven Development`, ou Desenvolvimento Orientado a Testes. A ideia do TDD é que você trabalhe em ciclos.

### Ciclo do TDD
1. **Red**: Escreva um teste que falhe
2. **Green**: Escreva o código mínimo para passar no teste  
3. **Refactor**: Melhore o código mantendo os testes passando

### Vantagens do TDD
- entregar software de qualidade;
- testar procurando possíveis falhas;
- criar testes de integração, testes isolados (unitários);
- evitar escrever códigos complexos ou que não sigam os pré-requisitos necessários;

A proposta do TDD é que você codifique antes mesmo do código existir, isso nos garante mais qualidade no nosso projeto. Além de que, provavelmente se você deixar pra fazer os testes no final, pode acabar não fazendo. Com isso, sua aplicação perde qualidade e está muito mais propensa a erros.

# Store API

## Resumo do projeto
Este documento traz informações do desenvolvimento de uma API em FastAPI a partir do TDD.

## Objetivo
Essa aplicação tem como objetivo principal trazer conhecimentos sobre o TDD, na prática, desenvolvendo uma API com o Framework Python, FastAPI. Utilizando o banco de dados MongoDB, para validações o Pydantic, para os testes Pytest e entre outras bibliotecas.

## O que é?
Uma aplicação que:
- tem fins educativos;
- permite o aprendizado prático sobre TDD com FastAPI + Pytest;

## O que não é?
Uma aplicação que:
- se comunica com apps externas;

## Solução Proposta
Desenvolvimento de uma aplicação simples a partir do TDD, que permite entender como criar tests com o `pytest`. Construindo testes de Schemas, Usecases e Controllers (teste de integração).

## Desafio Final
- **Create**
  - Mapear uma exceção, caso dê algum erro de inserção e capturar na controller
- **Update**
  - Modifique o método de patch para retornar uma exceção de Not Found, quando o dado não for encontrado
  - a exceção deve ser tratada na controller, pra ser retornada uma mensagem amigável pro usuário
  - ao alterar um dado, a data de updated_at deve corresponder ao time atual, permitir modificar updated_at também
- **Filtros**
  - cadastre produtos com preços diferentes
  - aplique um filtro de preço, assim: (price > 5000 and price < 8000)

## Preparar ambiente

Vamos utilizar Pyenv + Poetry:

1. Instale o Poetry se ainda não tiver
2. Execute `poetry install` para instalar as dependências
3. Configure as variáveis de ambiente no arquivo `.env`
4. Execute `poetry run uvicorn store.main:app --reload` para rodar a aplicação

## Como executar
```bash
# Instalar dependências
poetry install

# Executar testes
poetry run pytest

# Executar aplicação
poetry run uvicorn store.main:app --reload
```

## Links úteis de documentação
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/dev/)
- [Motor (MongoDB)](https://motor.readthedocs.io/en/stable/)
- [Pytest](https://docs.pytest.org/en/7.4.x/)