# Validação Formal em OWL DL: Controle de Autoridade e Homonímia (BRAJIS)

Este repositório contém os artefatos suplementares (ontologias em Turtle e RDF/XML, scripts de verificação, justificativas formais e logs de execução) referentes à verificação formal com raciocinador (*reasoner*) **HermiT** dos dois cenários de controle de autoridade discutidos no artigo submetido à **BRAJIS (*Brazilian Journal of Information Science: Research Trends*)**.

---

## 1. Descrição dos Cenários Avaliados

O estudo analisa formalmente em OWL 2 DL o problema de controle de autoridade envolvendo nomes homônimos/variantes (`leaoXIV` e `robertWPrevost`) diante da obra de autoria única `probabilityTheisticExplanation` (`LivroDeAutoriaUnica ⊑ ≤1 temAutor.⊤`, sendo `temAutor ≡ autorDe⁻`):

- **Cenário A (`cenario_A_com_distincao.ttl` / `.owl`) — Com distinção explícita (`owl:differentFrom`)**:
  Inclui os axiomas (1) a (4), a asserção equivocada `:leaoXIV :autorDe :probabilityTheisticExplanation` e o **Axioma (5)**: `:leaoXIV owl:differentFrom :robertWPrevost`.
  - **Resultado**: **Ontologia Inconsistente** (`owl:Thing ⊑ owl:Nothing`), detectando formalmente a contradição entre a restrição de autoria única (`≤ 1 temAutor.⊤`) e a existência de dois autores declarados como indivíduos distintos.

- **Cenário B (`cenario_B_sem_distincao.ttl` / `.owl`) — Sem distinção explícita**:
  Inclui os axiomas (1) a (4) e a asserção `:leaoXIV :autorDe :probabilityTheisticExplanation`, **omitindo** o Axioma (5) (`owl:differentFrom`).
  - **Resultado**: **Ontologia Consistente**. Como a linguagem OWL adota a *Open World Assumption* (OWA) e **não** adota a *Unique Name Assumption* (UNA), o raciocinador resolve a restrição de cardinalidade máxima (`≤ 1 temAutor.⊤`) inferindo que ambos os identificadores denotam o mesmo indivíduo (`leaoXIV = robertWPrevost`, i.e., `owl:sameAs`).

---

## 2. Estrutura de Arquivos do Repositório

| Arquivo | Descrição |
| :--- | :--- |
| [`cenario_A_com_distincao.ttl`](./cenario_A_com_distincao.ttl) | Ontologia original em formato Turtle do **Cenário A** (com `owl:differentFrom`). |
| [`cenario_B_sem_distincao.ttl`](./cenario_B_sem_distincao.ttl) | Ontologia original em formato Turtle do **Cenário B** (sem `owl:differentFrom`). |
| [`cenario_A_com_distincao.owl`](./cenario_A_com_distincao.owl) | Ontologia do Cenário A convertida para RDF/XML via ROBOT (`robot convert`). |
| [`cenario_B_sem_distincao.owl`](./cenario_B_sem_distincao.owl) | Ontologia do Cenário B convertida para RDF/XML via ROBOT (`robot convert`). |
| [`explicacao_cenario_A.md`](./explicacao_cenario_A.md) | Justificativa formal mínima (*laconic explanation*) da inconsistência do Cenário A gerada pelo HermiT via ROBOT (`robot explain`). |
| [`cenario_B_inferido.owl`](./cenario_B_inferido.owl) | Ontologia resultante da execução do raciocinador HermiT sobre o Cenário B via ROBOT (`robot reason`). |
| [`teste_homonimo.py`](./teste_homonimo.py) | Script Python utilizando `owlready2` e HermiT para verificar ambos os cenários e consultar a identidade inferida via classe nominal enumerada `OneOf([rob])` (`{robertWPrevost}`). |
| [`resultados.txt`](./resultados.txt) | Saída bruta completa da execução do script `teste_homonimo.py`. |
| [`requirements.txt`](./requirements.txt) | Dependências Python para reprodução exata (`owlready2==0.51`). |

---

## 3. Ambiente de Execução Registrado

- **Java**: `openjdk version "25.0.5" 2026-10-20 LTS` (Eclipse Temurin 25.0.5+8 64-Bit Server VM)
- **ROBOT**: `ROBOT version 1.9.11` (OWL API 4.5.29 / Reasoner HermiT)
- **Python**: `3.13.17`
- **Owlready2**: `0.51`

---

## 4. Instruções para Reprodução pelos Revisores

### Pré-requisitos
- Java 11+ instalado (`java -version`)
- Python 3.9+ instalado (`python --version`)

### Passo 1: Download do ROBOT e execução via linha de comando

```bash
# 1. Baixar o ROBOT (v1.9.11+)
curl -L -o robot.jar https://github.com/ontodev/robot/releases/latest/download/robot.jar
java -jar robot.jar --version

# 2. Converter os arquivos .ttl para RDF/XML (.owl)
java -jar robot.jar convert --input cenario_A_com_distincao.ttl --output cenario_A_com_distincao.owl
java -jar robot.jar convert --input cenario_B_sem_distincao.ttl --output cenario_B_sem_distincao.owl

# 3. Cenário A: gerar a justificativa formal da inconsistência com HermiT
java -jar robot.jar explain --input cenario_A_com_distincao.owl --reasoner hermit -M inconsistency --explanation explicacao_cenario_A.md

# 4. Cenário B: verificar consistência e raciocinar com HermiT
java -jar robot.jar reason --input cenario_B_sem_distincao.owl --reasoner hermit --output cenario_B_inferido.owl
```

### Passo 2: Execução do script em Python (`owlready2` + HermiT)

```bash
# Criar e ativar ambiente virtual
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .\.venv\Scripts\Activate.ps1

# Instalar owlready2 e executar o teste
pip install -r requirements.txt
python teste_homonimo.py > resultados.txt 2>&1
```

---

## 5. Resultados Obtidos

### 5.1. Justificativa da Inconsistência do Cenário A (`explicacao_cenario_A.md`)

```markdown
## [Thing](http://www.w3.org/2002/07/owl#Thing) SubClassOf [Nothing](http://www.w3.org/2002/07/owl#Nothing) ##

  - [probabilityTheisticExplanation](http://example.org/homonimo#probabilityTheisticExplanation) Type [LivroDeAutoriaUnica](http://example.org/homonimo#LivroDeAutoriaUnica)
  - [leaoXIV](http://example.org/homonimo#leaoXIV) [autorDe](http://example.org/homonimo#autorDe) [probabilityTheisticExplanation](http://example.org/homonimo#probabilityTheisticExplanation)
  - [leaoXIV](http://example.org/homonimo#leaoXIV) DifferentFrom [robertWPrevost](http://example.org/homonimo#robertWPrevost)
  - [LivroDeAutoriaUnica](http://example.org/homonimo#LivroDeAutoriaUnica) SubClassOf [temAutor](http://example.org/homonimo#temAutor) max 1 [Thing](http://www.w3.org/2002/07/owl#Thing)
  - [autorDe](http://example.org/homonimo#autorDe) InverseOf [temAutor](http://example.org/homonimo#temAutor)
  - [robertWPrevost](http://example.org/homonimo#robertWPrevost) [autorDe](http://example.org/homonimo#autorDe) [probabilityTheisticExplanation](http://example.org/homonimo#probabilityTheisticExplanation)
```

### 5.2. Saída do Script Python (`resultados.txt`)

> **Nota técnica sobre a materialização de `owl:sameAs` no HermiT/Owlready2**: A interface CLI do HermiT invocada pelo `owlready2` (`org.semanticweb.HermiT.cli.CommandLine -c -O -D -I -Y`) materializa subsunções de classes e asserções de tipo (`ClassAssertion`), mas não exporta axiomas `SameIndividual` de volta para a lista `.equivalent_to` do Python. Para demonstrar diretamente a identidade inferida no Cenário B via `ClassAssertion`, o script define a classe nominal enumerada `MesmoQueRobert ≡ {robertWPrevost}` (`OneOf([rob])`), permitindo verificar que o HermiT classifica `leaoXIV` como instância de `{robertWPrevost}` (`True`).

```text
Python: 3.13.17 | owlready2: 0.51
openjdk version "25.0.5" 2026-10-20 LTS

=== CENÁRIO A (com axioma 5) ===
Resultado: INCONSISTENTE (esperado)

=== CENÁRIO B (sem axioma 5) ===
Resultado: CONSISTENTE
Indivíduos inferidos como idênticos a leaoXIV: []
leaoXIV sameAs robertWPrevost inferido? False

=== CENÁRIO B – consulta: quem é o mesmo indivíduo que robertWPrevost? ===
Instâncias inferidas de {robertWPrevost}: [D:\Mestrado\ECI\Mediação_da_Informação_Igreja\Testes_LD\cenario_B_sem_distincao.leaoXIV, D:\Mestrado\ECI\Mediação_da_Informação_Igreja\Testes_LD\cenario_B_sem_distincao.robertWPrevost]
leaoXIV inferido idêntico a robertWPrevost? True
```

