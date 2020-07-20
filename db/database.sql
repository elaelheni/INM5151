create table profiles (
  id integer primary key,
  fname varchar(40),
  lname varchar(40),
  pic_id varchar(32)
);

create table article (
  id integer primary key,
  titre varchar(100),
  identifiant varchar(50),
  description varchar(500),
  pic_id varchar(32)
);

create table pictures (
  id varchar(32) primary key,
  data blob
);

