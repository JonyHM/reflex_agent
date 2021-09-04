# AGENTE REFLEXIVO
## _Banco de Dados - Fatec SJC_
## _Laboratório de Desenvolvimento em Banco de Dados V_

PROF. FABRÍCIO GALENDE M. DE CARVALHO
ALUNOS. GUILHERME ANDERSON E JONATHAS HENRIQUE
TRABALHO PRÁTICO I:   AGENTES RACIONAIS REFLEXIVOS / REFLEXIVOS BASEADOS EM MODELO.

## I. Técnologias Utilizadas
- Python
- Maria DB

## II.  DESCRIÇÃO  DO  PROBLEMA:

- Desenvolver  um  sistema  de  recomendação  simples, utilizando a abordagem de agentes racionais reflexivos / reflexivos baseados em modelos. Esse sistema deve atender aos seguintes requisitos e restrições: 

## III. REQUISITOS:
-  Quando um consumidor indicar a intenção de comprar um produto A, frequentemente comprado com um produto B, o sistema de recomendação sugerirá ao cliente a compra do produto B; 
-  Quando  um  consumidor  indicar  a  intenção  de  compra  dos  produtos  A  e  B, frequentemente comprados  com  o  produto  C, o  sistema de recomendação  sugerirá  ao cliente a compra do produto C;
-   O sistema deve permitir o cadastro, a exclusão e a visualização das regras armazenadas em um banco de dados relacional;
-   A interface poderá ser totalmente textual, via prompt de comando.

## IV. RESTRIÇÕES:
- Ser desenvolvido em linguagem de programação Python 3+;
- Utilizar uma base de regras que seja armazenada em banco de dados relacional (utilizar o MariaDB);
-  Disponibilizar todo o código via repositório do GitHub (não esquecer de gerar o arquivo requirements.txt com as dependências de projeto) .


## Primeiros Passos


#### 1.  Criação do ambiente virutal.

1.1.    Instalar a virtualenv
```sh
pip install virtualenv
```

1.2.    Criar virtualenv
```sh
virtualenv nome_da_virtualenv
```

1.3.    Ativar a virtual env
```sh
cd nome_da_venv/Scripts
Activate
```

#### 2.  Instalar dependência do projeto
2.1.    Retorne até a raiz do projeto
```sh
cd ../..
```

2.2.    Instalar todas as dependências do projeto
```sh
pip install -r requirements.txt
```
#### 3. Criação do Banco de dados

##### 3.1. CRIANDO E ACESSANDO O BANCO :

```sh
CREATE DATABASE IF NOT EXISTS reflex;
```

##### 3.2. Selecionar banco que deseja utilizar:
```sh
USE reflex;
```

##### 3.3. CRIANDO TABELA RULES:
```sh
CREATE TABLE IF NOT EXISTS rules(
	id_rules int(9) AUTO_INCREMENT,
	relation varchar(50) NOT NULL,
	action_rules varchar(50) NOT NULL,
	PRIMARY KEY (id_rules)
)
```

##### 3.4. CRIANDO TABELA PRODUCT:
```sh
CREATE table IF NOT EXISTS product(
	id_product int(9) AUTO_INCREMENT,
	product_name varchar(30) NOT NULL,
	id_rules int(9) NOT NULL,
	PRIMARY KEY (id_product)
)
```

##### 3.5. CRIANDO CHAVE EXTRANGEIRA:
```sh
ALTER TABLE reflex.product 
ADD CONSTRAINT id_rules_FK FOREIGN KEY (id_rules) 
REFERENCES reflex.rules(id_rules) 
ON DELETE CASCADE 
ON UPDATE CASCADE
```

##### 3.6. CRIANDO FUNÇÃO PARA INSERIR RULE:
```sh
CREATE OR REPLACE FUNCTION FNC_INSERT_RULE (fnc_relation varchar(50), fnc_action_rules varchar(50))
RETURNS int
LANGUAGE SQL
NOT DETERMINISTIC
BEGIN
  DECLARE next_id_rule int;
  SELECT max(id_rules + 1) INTO next_id_rule FROM rules;
  insert into rules (relation, action_rules) values (fnc_relation, fnc_action_rules);
  RETURN next_id_rule;
end;
```

##### 3.7. CRIANDO FUNÇÃO PARA INSERIR product:
```sh
CREATE OR REPLACE FUNCTION FNC_INSERT_PRODUCT (fnc_product_name varchar(30), fnc_id_rules int(9))
RETURNS int
LANGUAGE SQL
NOT DETERMINISTIC
BEGIN
  DECLARE next_id_product int;
  SELECT max(id_product + 1) INTO next_id_product FROM product;
  insert into product (product_name, id_rules) values (fnc_product_name, fnc_id_rules);
  RETURN next_id_product;
end;
```

##### 3.8. CRIANDO VIEW COM TODAS AS RELAÇÕES:
```sh
create or replace view all_percepts as
select p.id_rules,
	   p.product_name "percept", 
	   r.relation "relation", 
	   r.action_rules "action" 
	   from product p 
inner join rules r on p.id_rules = r.id_rules 
```

#### 4. Executando a aplicação:

4.1. Antes de executar, é necessário revisar os dados no final do arquivo "reflex.py", alterando as informações de credenciais do banco, caso necessário. O padrão está conforme abaixo:
```
con = pymysql.connect(
        host='localhost',
        port=3306, ## porta padrão do mariaDB
        user='root',
        password='fatec',
        database='reflex',
        cursorclass=pymysql.cursors.DictCursor
    )
```

4.2. Estando na raiz do projeto, execute o comando abaixo e siga os menus interativos para cadastrar novas regras e testar as regras existentes:
```
python reflex.py
```
