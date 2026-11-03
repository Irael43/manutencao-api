# Manutenção Preditiva API

API REST que disponibiliza um modelo de Machine Learning para prever falhas em equipamentos industriais. O projeto foi desenvolvido como parte do curso de Desenvolvedor em IA para Análise Preditiva.

## Sobre o projeto

A ideia surgiu de um problema comum na indústria: máquinas quebram sem aviso e param a linha de produção. Com sensores monitorando temperatura, rotação, torque e desgaste, dá para prever falhas antes que aconteçam.

Neste projeto, peguei o modelo que já tinha treinado na etapa anterior do curso (uma Árvore de Decisão com 94,15% de acurácia) e o transformei em uma API REST usando FastAPI. Assim, qualquer sistema da empresa pode consultar o modelo via HTTP, sem precisar rodar Python ou carregar o modelo localmente.

## O que o sistema faz

- **GET /health** — Verifica se a API está no ar e se o modelo está carregado na memória.
- **POST /predict** — Recebe os dados dos sensores e devolve se há risco de falha (0 ou 1) e a probabilidade.

## Tecnologias que usei

| Ferramenta | Para quê |
|------------|----------|
| Python 3.13 | Linguagem base |
| FastAPI | Framework da API |
| Uvicorn | Servidor para rodar a API |
| Pydantic | Validação dos dados de entrada e saída |
| Scikit-learn | Modelo de Machine Learning |
| Joblib | Salvar e carregar o modelo treinado |
| NumPy | Manipulação dos arrays de features |

## Estrutura de pastas
manutencao-api/
│
├── app/
│ ├── init.py
│ ├── main.py # Onde a API é criada e o modelo é carregado
│ ├── schemas.py # Contratos de entrada e saída (Pydantic)
│ ├── services.py # Lógica de inferência (carrega modelo, faz predição)
│ └── routers.py # Definição dos endpoints
│
├── models/
│ └── modelo_manutencao.joblib # Modelo treinado serializado
│
├── requirements.txt
└── README.md

A separação em camadas foi uma escolha para deixar o código organizado. O `services.py` não sabe nada sobre HTTP, e o `routers.py` não sabe como o modelo funciona. Isso facilita manutenção e testes.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Irael43/manutencao-api.git
cd manutencao-api

2. Criar ambiente virtual e ativar
bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
3. Instalar dependências
bash
pip install -r requirements.txt
4. Rodar a API
bash
uvicorn app.main:app --reload
5. Abrir a documentação
No navegador:

text
http://127.0.0.1:8000/docs
Exemplos de uso
Health check
bash
curl http://127.0.0.1:8000/health
Resposta:

json
{
  "status": "ok",
  "model_loaded": true
}
Predição
bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperatura_ar_k": 300.0,
    "temperatura_processo_k": 310.0,
    "velocidade_rotacao_rpm": 1500,
    "torque_nm": 40,
    "desgaste_ferramenta_min": 100
  }'
Resposta:

json
{
  "falha_prevista": 0,
  "probabilidade": 0.9653
}
O campo falha_prevista retorna 0 para normal e 1 para falha. A probabilidade indica a confiança do modelo naquela predição.

Sobre o modelo
O modelo usado foi uma Árvore de Decisão com max_depth=10, treinada com 5 features dos sensores. Antes de treinar, os dados passaram por limpeza (nulos tratados com mediana) e balanceamento com SMOTE apenas no conjunto de treino, para evitar vazamento de dados.

Métrica	Valor
Algoritmo	DecisionTreeClassifier
Acurácia no teste	94,15%
Profundidade máxima	10
Features de entrada	5
Decisões técnicas que tomei
Carregar o modelo uma única vez: usei o lifespan do FastAPI para carregar o .joblib na inicialização. Ler o arquivo a cada requisição seria lento e desnecessário.

Pydantic com Field: coloquei restrições de faixa (ge, le) para que dados inválidos retornem erro 422 automaticamente, antes de chegar no modelo.

Separar services de routers: a lógica de inferência ficou isolada da camada HTTP. Se amanhã eu trocar o modelo ou o framework, o services.py continua igual.

Retreinar com 5 features: o modelo original usava 12 features, mas a API só recebe 5. Retreinei com apenas as features que o endpoint expõe, para manter consistência entre treino e produção.

O que poderia melhorar
Adicionar autenticação na API (hoje qualquer um com acesso à rede pode chamar).

Criar testes automatizados com pytest para os endpoints.

Usar Docker para facilitar o deploy.

Monitorar as predições em produção para detectar drift nos dados.

Colocar um versionamento na rota (/v1/predict) para facilitar futuras mudanças.

Vídeo de demonstração
[Link do vídeo no Google Drive]

Autor
Israel — Curso de Desenvolvedor(a) em IA para Análise Preditiva

Novembro/2026