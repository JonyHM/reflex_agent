#############################################################

# CRIANDO E ACESSANDO O BANCO 
CREATE DATABASE IF NOT EXISTS reflex;

USE reflex;

#############################################################

# CRIANDO TABELA RULES
CREATE TABLE IF NOT EXISTS rules(
	id_rules int(9) AUTO_INCREMENT,
	relation varchar(50) NOT NULL,
	action_rules varchar(50) NOT NULL,
	PRIMARY KEY (id_rules)
);

#############################################################

# CRIANDO TABELA PRODUCT
CREATE table IF NOT EXISTS product(
	id_product int(9) AUTO_INCREMENT,
	product_name varchar(30) NOT NULL,
	id_rules int(9) NOT NULL,
	PRIMARY KEY (id_product)
);

#############################################################

# CRIANDO CHAVE EXTRANGEIRA 
ALTER TABLE reflex.product 
  ADD CONSTRAINT id_rules_FK FOREIGN KEY (id_rules) 
  REFERENCES reflex.rules(id_rules) 
  ON DELETE CASCADE 
  ON UPDATE CASCADE;

#############################################################

# CRIANDO FUNCAO PARA INSERIR RULE
DELIMITER //
CREATE OR REPLACE FUNCTION FNC_INSERT_RULE (fnc_relation varchar(50), fnc_action_rules varchar(50))
RETURNS int
LANGUAGE SQL
NOT DETERMINISTIC
BEGIN

  DECLARE next_id_rule int;
  SELECT `AUTO_INCREMENT` INTO next_id_rule
    FROM  INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'reflex'
    AND TABLE_NAME   = 'rules';
  insert into rules (relation, action_rules) values (fnc_relation, fnc_action_rules);
  RETURN next_id_rule;

END; //

DELIMITER ;

#############################################################

# CHAMADA DA FUNCAO
select FNC_INSERT_RULE('==', 'leite');

#############################################################

# CRIANDO FUNCAO PARA INSERIR product
DELIMITER //
CREATE OR REPLACE FUNCTION FNC_INSERT_PRODUCT (fnc_product_name varchar(30), fnc_id_rules int(9))
RETURNS int
LANGUAGE SQL
NOT DETERMINISTIC
BEGIN

  DECLARE next_id_product int;
  SELECT max(id_product + 1) INTO next_id_product FROM product;
  insert into product (product_name, id_rules) values (fnc_product_name, fnc_id_rules);
  RETURN next_id_product;

END; //

DELIMITER ;

#############################################################

# CHAMADA DA FUNCAO

select FNC_INSERT_PRODUCT('pão', 1);

#############################################################

create or replace view all_percepts as
select p.id_rules,
	   p.product_name "percept",
	   r.relation "relation",
	   r.action_rules "action"
	   from product p
inner join rules r on p.id_rules = r.id_rules;

#############################################################

# CRIANDO TABELA BASKET
CREATE table IF NOT EXISTS basket(
	bsk_id int(9) AUTO_INCREMENT,
  bsk_transaction_id int(9) NOT NULL,
	bsk_item_name varchar(100) NOT NULL,
	PRIMARY KEY (bsk_id)
);

# CRIANDO SEQUENCE PARA CONTROLE DO ID DE TRANSAÇÃO
CREATE SEQUENCE id_transaction START WITH 1 INCREMENT BY 1;
