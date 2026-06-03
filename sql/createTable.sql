CREATE TABLE public.sales_shops (
	num_shop int4 NOT NULL,
	num_cash_desk int4 NOT NULL,
	dt date NOT NULL,
	doc_id varchar NOT NULL,
	item varchar NOT NULL,
	category varchar NOT NULL,
	amount int4 NOT NULL,
	price numeric NOT NULL,
	discount int4 NOT NULL,
	CONSTRAINT sales_shops_pk PRIMARY KEY (num_shop, num_cash_desk, dt, doc_id, item, category, amount, price, discount)
);