CREATE table IF NOT EXISTS basket(
	bsk_id int(9) AUTO_INCREMENT,
	bsk_transaction int(9) NOT NULL,
	bsk_item varchar(100) NOT NULL,
  bsk_date_time DATETIME(6) NOT NULL,
  bsk_period_day varchar(15) NOT NULL,
  bsk_weekday_weekend varchar(10) NOT NULL,
	PRIMARY KEY (bsk_id)
);

CREATE table IF NOT EXISTS product_base(
	pb_id int(9) AUTO_INCREMENT,
	pb_name varchar(100) NOT NULL,
	PRIMARY KEY (pb_id)
);

CREATE SEQUENCE id_transaction START WITH 1 INCREMENT BY 1;