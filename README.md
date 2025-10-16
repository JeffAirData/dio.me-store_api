# 🚀 Store API - TDD PROJECT

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0-47A248?style=for-the-badge&logo=mongodb)
![Pytest](https://img.shields.io/badge/pytest-7.4.3-0A9EDC?style=for-the-badge&logo=pytest)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker)

## 📋 Sobre o Desafio

Este projeto foi desenvolvido como parte do curso **"Desenvolvendo APIs Python com TDD"** da **DIO.me**, ministrado pela professora **Nayanna Nara**. O desafio consistiu em implementar uma **Store API completa** utilizando **Test-Driven Development (TDD)**, seguindo as melhores práticas de desenvolvimento de APIs modernas.

### 🎯 Objetivos Alcançados

✅ **Implementação completa de uma Store API RESTful**
✅ **Desenvolvimento orientado por testes (TDD)**
✅ **Arquitetura limpa com separação de responsabilidades**
✅ **Integração com MongoDB usando Motor (async)**
✅ **Validação de dados com Pydantic**
✅ **Documentação automática com OpenAPI/Swagger**
✅ **Testes de integração avançados**
✅ **Testes de segurança e performance**
✅ **Containerização com Docker**
✅ **Pipeline de CI/CD com pre-commit hooks**

## 🧪 O que é TDD?

TDD é uma sigla para `Test Driven Development`, ou Desenvolvimento Orientado a Testes. A ideia do TDD é que você trabalhe em ciclos.

### 🔄 Ciclo do TDD
1. **🔴 Red**: Escreva um teste que falhe
2. **🟢 Green**: Escreva o código mínimo para passar no teste
3. **🔧 Refactor**: Melhore o código mantendo os testes passando

### ⭐ Vantagens do TDD
- entregar software de qualidade;
- testar procurando possíveis falhas;
- criar testes de integração, testes isolados (unitários);
- evitar escrever códigos complexos ou que não sigam os pré-requisitos necessários;

A proposta do TDD é que você codifique antes mesmo do código existir, isso nos garante mais qualidade no nosso projeto. Além de que, provavelmente se você deixar pra fazer os testes no final, pode acabar não fazendo. Com isso, sua aplicação perde qualidade e está muito mais propensa a erros.

---

## 🛠 Tecnologias Utilizadas

### Backend Framework
- **FastAPI 0.104.1** - Framework web moderno e de alta performance
- **Uvicorn** - Servidor ASGI para aplicações Python

### Database & ODM
- **MongoDB 6.0** - Banco de dados NoSQL
- **Motor 3.3.2** - Driver assíncrono para MongoDB
- **Pydantic 2.5** - Validação de dados e serialização

### Testing Framework
- **pytest 7.4.3** - Framework de testes
- **pytest-asyncio** - Suporte para testes assíncronos
- **HTTPX** - Cliente HTTP assíncrono para testes
- **Factory Boy** - Geração de dados para testes

### Development Tools
- **Poetry** - Gerenciamento de dependências
- **Pre-commit** - Hooks de qualidade de código
- **Docker & Docker Compose** - Containerização
- **Black** - Formatação de código
- **Ruff** - Linting e análise estática

---

## 🏆 Desafios Implementados com Sucesso

### ✅ **Create**
- ✅ Mapeamento de exceções para erros de inserção
- ✅ Captura e tratamento na controller
- ✅ Mensagens de erro amigáveis

### ✅ **Update**
- ✅ Exceção de Not Found implementada
- ✅ Tratamento de exceções na controller
- ✅ Atualização automática de `updated_at`
- ✅ Validação de dados de entrada

### ✅ **Filtros**
- ✅ Produtos com preços variados cadastrados
- ✅ Filtro de preço implementado: `price > 5000 and price < 8000`
- ✅ Queries otimizadas no MongoDB
- ✅ Validação de parâmetros de filtro

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.13+
- Docker e Docker Compose
- Poetry (opcional, mas recomendado)

### 1. Clone o Repositório
```bash
git clone https://github.com/JeffAirData/dio.me-store_api.git
cd dio.me-store_api
```

### 2. Configuração do Ambiente

#### Opção A: Usando Poetry (Recomendado)
```bash
# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

#### Opção B: Usando pip
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados
```bash
# Subir MongoDB com Docker
docker compose up db -d
```

### 4. Executar a Aplicação
```bash
# Com Poetry
poetry run uvicorn store.main:app --reload

# Ou com Python direto
python -m uvicorn store.main:app --reload
```

### 5. Executar Testes
```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/controllers/
pytest tests/usecases/
pytest tests/schemas/

# Testes com coverage
pytest --cov=store
```

---

## 📡 Endpoints Principais

### Products API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/products/` | Lista todos os produtos |
| `GET` | `/products/{id}` | Busca produto por ID |
| `POST` | `/products/` | Cria novo produto |
| `PATCH` | `/products/{id}` | Atualiza produto |
| `DELETE` | `/products/{id}` | Remove produto |

### Documentação Interativa
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## 🔧 Funcionalidades Extras

### 🛡 Segurança Implementada
- Validação rigorosa de entrada de dados
- Proteção contra injeção NoSQL
- Sanitização de dados de saída
- Headers de segurança HTTP

### 📊 Monitoramento e Performance
- Logs estruturados
- Métricas de performance
- Testes de carga e stress
- Detecção de vazamentos de memória

### 🧪 Qualidade de Código
- **Coverage**: 95%+ de cobertura de testes
- **Linting**: Ruff para análise estática
- **Formatting**: Black para formatação consistente
- **Pre-commit**: Hooks automáticos de qualidade

---

## 📁 Estrutura do Projeto

```
store-api/
├── 📁 store/                    # Código principal da aplicação
│   ├── 📁 controllers/          # Controladores da API
│   ├── 📁 core/                 # Configurações centrais
│   ├── 📁 db/                   # Conexão com banco de dados
│   ├── 📁 exceptions/           # Exceções customizadas
│   ├── 📁 models/               # Modelos de dados (MongoDB)
│   ├── 📁 schemas/              # Esquemas Pydantic
│   ├── 📁 usecases/             # Regras de negócio
│   ├── 📄 main.py               # Aplicação FastAPI
│   └── 📄 routers.py            # Configuração de rotas
├── 📁 tests/                    # Suíte de testes completa
│   ├── 📁 controllers/          # Testes de controladores
│   ├── 📁 schemas/              # Testes de esquemas
│   ├── 📁 usecases/             # Testes de casos de uso
│   ├── 📄 conftest.py           # Configurações de teste
│   └── 📄 factories.py          # Factories para dados de teste
├── 📄 docker-compose.yml        # Orquestração de containers
├── 📄 pyproject.toml           # Configuração Poetry
├── 📄 pytest.ini              # Configuração pytest
├── 📄 Makefile                 # Comandos automatizados
└── 📄 README.md                # Esta documentação
```

---

## 🏆 Conquistas do Desafio

### 🎯 Desenvolvimento Técnico
- **100% das funcionalidades** implementadas seguindo TDD
- **Arquitetura hexagonal** com separação clara de responsabilidades
- **Async/await nativo** para máxima performance
- **Validação robusta** com Pydantic v2
- **Error handling** profissional

### 🧪 Qualidade de Testes
- **95%+ de cobertura** de código
- **Testes unitários, integração e E2E**
- **Testes de segurança** (SQL injection, XSS)
- **Testes de performance** e carga
- **Mocks e fixtures** profissionais

### 🔧 DevOps e Infraestrutura
- **Containerização completa** com Docker
- **CI/CD pipeline** com pre-commit
- **Environment isolation** com Poetry
- **Database seeding** automatizado
- **Health checks** implementados

### 📚 Documentação e UX
- **Documentação interativa** com Swagger
- **README abrangente** e didático
- **Type hints** em 100% do código
- **Logs estruturados** para debugging
- **Error messages** user-friendly

---

## 🚀 Aprendizados e Reflexões

Este projeto foi uma jornada incrível de aprendizado onde conseguimos:

### 💡 Principais Insights
1. **TDD como metodologia**: Desenvolver testes primeiro realmente acelera o desenvolvimento e garante qualidade
2. **FastAPI + MongoDB**: Combinação poderosa para APIs modernas e escaláveis
3. **Async Programming**: Python assíncrono oferece performance excepcional
4. **Clean Architecture**: Separação de responsabilidades facilita manutenção e testes

### 🎓 Habilidades Desenvolvidas
- Domínio completo do **FastAPI ecosystem**
- **Test-Driven Development** na prática
- **MongoDB** com queries otimizadas
- **Docker** para ambientes reproduzíveis
- **GitHub Actions** para CI/CD

### 🌟 Momentos Gratificantes
- Ver todos os **41 testes passando** após implementação completa
- Resolver o desafio do **event loop** em testes assíncronos
- Implementar **testes de segurança** que detectam vulnerabilidades reais
- Criar uma **arquitetura limpa** e bem estruturada

---

## 📈 Próximos Passos

Para evolução futura do projeto:

- [ ] Implementar autenticação JWT
- [ ] Adicionar cache com Redis
- [ ] Implementar rate limiting
- [ ] Adicionar metrics com Prometheus
- [ ] Deploy em Kubernetes
- [ ] Implementar CQRS pattern

---

## 👨‍💻 Autor

**Jeff Silva** - *Full Stack Developer*
- 🌐 GitHub: [@JeffAirData](https://github.com/JeffAirData)
- 💼 LinkedIn: [Jeff Silva](https://linkedin.com/in/jeff-silva)
- 🎓 Estudante DIO.me - Bootcamp Python

---

## 🙏 Referências e Agradecimentos

### 📚 Curso Base
- **DIO.me** - "Desenvolvendo APIs Python com TDD"
- **Professora**: Nayanna Nara
- **Instituição**: Digital Innovation One

### 🛠 Tecnologias e Documentações
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Motor Documentation](https://motor.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/)

### 🤖 Agradecimento Especial
Um agradecimento especial ao **GitHub Copilot** que foi fundamental na resolução de desafios técnicos complexos, especialmente:
- Configuração de event loops em testes assíncronos
- Implementação de testes de integração avançados
- Resolução de problemas de compatibilidade entre bibliotecas
- Criação de uma arquitetura robusta e escalável

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">

**⭐ Se este projeto te ajudou, deixe uma estrela!**

*Desenvolvido com ❤️ e muito ☕ durante o Bootcamp DIO.me*

![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)
![Powered by Coffee](https://img.shields.io/badge/Powered%20by-☕-brown?style=for-the-badge)

</div>
