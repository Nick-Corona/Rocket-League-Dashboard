-- create solo tables

create table if not exists solo.mystats (
	gameid		serial primary key,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null
);

create table if not exists solo.opponent1 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_opponent1_mystats
    foreign key (gameid) 
    references solo.mystats(gameid)
);

create table if not exists solo.gamedetails (
	gameid		serial,
	overtime	int null,
	comms		varchar null,
  	constraint fk_gamedetails_mystats
    foreign key (gameid) 
    references solo.mystats(gameid)
);

-- create doubles tables

create table if not exists doubles.mystats (
	gameid		serial primary key,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null
);

create table if not exists doubles.teammate1 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_teammate1_mystats
    foreign key (gameid) 
    references doubles.mystats(gameid)
);

create table if not exists doubles.opponent1 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_opponent1_mystats
    foreign key (gameid) 
    references doubles.mystats(gameid)
);

create table if not exists doubles.opponent2 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_opponent2_mystats
    foreign key (gameid) 
    references doubles.mystats(gameid)
);

create table if not exists doubles.gamedetails (
	gameid		serial,
	overtime	int null,
	comms		varchar null,
  	constraint fk_gamedetails_mystats
    foreign key (gameid) 
    references doubles.mystats(gameid)
);

-- create trios tables

create table if not exists trios.mystats (
	gameid		serial primary key,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null
);

create table if not exists trios.teammate1 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_teammate1_mystats
    foreign key (gameid) 
    references trios.mystats(gameid)
);

create table if not exists trios.teammate2 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_teammate2_mystats
    foreign key (gameid) 
    references trios.mystats(gameid)
);

create table if not exists trios.opponent1 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_opponent1_mystats
    foreign key (gameid) 
    references trios.mystats(gameid)
);

create table if not exists trios.opponent2 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_opponent2_mystats
    foreign key (gameid) 
    references trios.mystats(gameid)
);

create table if not exists trios.opponent3 (
	gameid		serial,
	score		int not null,
	goals		int not null,
	assists		int not null,
	saves		int not null,
	shots		int not null,
  	constraint fk_opponent3_mystats
    foreign key (gameid) 
    references trios.mystats(gameid)
);

create table if not exists trios.gamedetails (
	gameid		serial,
	overtime	int null,
	comms		varchar null,
  	constraint fk_gamedetails_mystats
    foreign key (gameid) 
     REFERENCES trios.mystats(gameid)
);