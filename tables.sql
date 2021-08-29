CREATE TABLE rules(
	id_rules int(9) AUTO_INCREMENT,
	relation varchar(50) NOT NULL,
	action_rules varchar(50) NOT NULL,
	PRIMARY KEY (id_rules)
)

CREATE TABLE product(
	id_product int(9) AUTO_INCREMENT,
	product_name varchar(30) NOT NULL,
	id_rules int(9) NOT NULL,
	PRIMARY KEY (id_product)
)

ALTER TABLE reflex.product 
ADD CONSTRAINT id_rules_FK FOREIGN KEY (id_rules) 
REFERENCES reflex.rules(id_rules) 
ON DELETE CASCADE 
ON UPDATE CASCADE;
