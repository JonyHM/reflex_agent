CREATE table IF NOT EXISTS basket(
	bsk_id int(9) AUTO_INCREMENT,
	bsk_transaction int(9) NOT NULL,
	bsk_item varchar(100) NOT NULL,
  bsk_date_time DATETIME(6) NOT NULL,
  bsk_period_day varchar(15) NOT NULL,
  bsk_weekday_weekend varchar(10) NOT NULL,
	PRIMARY KEY (bsk_id)
);