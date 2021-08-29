#############################################################

# CRIANDO TABELA RULES
CREATE TABLE rules(
	id_rules int(9) AUTO_INCREMENT,
	relation varchar(50) NOT NULL,
	action_rules varchar(50) NOT NULL,
	PRIMARY KEY (id_rules)
)

#############################################################

# CRIANDO TABELA PRODUCT
CREATE TABLE product(
	id_product int(9) AUTO_INCREMENT,
	product_name varchar(30) NOT NULL,
	id_rules int(9) NOT NULL,
	PRIMARY KEY (id_product)
)

#############################################################

# CRIANDO CHAVE EXTRANGEIRA 
ALTER TABLE reflex.product 
ADD CONSTRAINT id_rules_FK FOREIGN KEY (id_rules) 
REFERENCES reflex.rules(id_rules) 
ON DELETE CASCADE 
ON UPDATE CASCADE;

#############################################################

# CRIANDO FUN플O PARA INSERIR RULE
CREATE OR REPLACE FUNCTION FNC_INSERT_RULE (fnc_relation varchar(50), fnc_action_rules varchar(50))
RETURNS int
LANGUAGE SQL
NOT DETERMINISTIC
BEGIN

  DECLARE next_id_rule int;
  SELECT max(id_rules + 1) INTO next_id_rule FROM rules;
  insert into rules (relation, action_rules) values (fnc_relation, fnc_action_rules);
  RETURN next_id_rule;

END

#############################################################

# CHAMADA DA FUN플O
select FNC_INSERT_RULE('<=', 'teste');

#############################################################

# CRIANDO FUN플O PARA INSERIR product
CREATE OR REPLACE FUNCTION FNC_INSERT_PRODUCT (fnc_product_name varchar(30), fnc_id_rules int(9))
RETURNS int
LANGUAGE SQL
NOT DETERMINISTIC
BEGIN

  DECLARE next_id_product int;
  SELECT max(id_product + 1) INTO next_id_product FROM product;
  insert into product (product_name, id_rules) values (fnc_product_name, fnc_id_rules);
  RETURN next_id_product;

END

#############################################################

# CHAMADA DA FUN플O

select FNC_INSERT_PRODUCT('batata', 1);

#############################################################



















