create database if not exists bank;
use bank;
create table users(
Account_no bigint primary key,
Account_Holder varchar (25),
Account_Type enum('SAVINGS','CURRENT','CREDIT'),
Account_Balance decimal(10,2) default 00.00,
Phone_Number bigint unique,
Email_ID varchar(30),
UserPin int
);



select * from users;


create table Transactions(
 Transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
    Account_No BIGINT,
    Transaction_Type VARCHAR(20),
    Amount DOUBLE,
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Account_No) REFERENCES users(Account_No)
);
select * from Transactions;





-- alter table Transactions add constraint FK_Transactions foreign key(Account_No) references users(Account_no);

