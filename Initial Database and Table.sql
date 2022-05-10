CREATE DATABASE INVOICES;
USE INVOICES;
CREATE TABLE invoices_list(
  INVOICE_NO int(11),
  CUSTOMER_NAME varchar(24),
  ADDRESS varchar(24),
  DATE date,
  INVOICE_TOTAL float
  ); 