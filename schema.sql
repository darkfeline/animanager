CREATE TABLE "anime_statuses" (
	`status`	text,
	PRIMARY KEY(status)
);
CREATE TABLE "anime_types" (
	`type`	text,
	PRIMARY KEY(type)
);
CREATE TABLE "manga_statuses" (
	`status`	TEXT,
	PRIMARY KEY(status)
);
CREATE TABLE "manga_types" (
	`type`	TEXT,
	PRIMARY KEY(type)
);
CREATE TABLE "anime" (
	`id`	INTEGER,
	`name`	text NOT NULL,
	`type`	TEXT NOT NULL,
	`ep_watched`	integer NOT NULL DEFAULT 0,
	`ep_total`	integer,
	`status`	TEXT NOT NULL,
	`date_started`	text,
	`date_finished`	text,
	`animedb_id`	integer NOT NULL UNIQUE,
	PRIMARY KEY(id),
	FOREIGN KEY(`type`) REFERENCES anime_types ( type ) on delete restrict on update cascade,
	FOREIGN KEY(`status`) REFERENCES anime_statuses ( status ) on delete restrict on update cascade
);
CREATE TRIGGER fix_ep_counts
after update of ep_watched, ep_total on anime for each row
when new.ep_total != 0 and new.ep_watched > new.ep_total
begin
update anime set ep_watched=new.ep_total where id=new.id;
end;
CREATE TABLE "manga" (
	`id`	INTEGER,
	`name`	TEXT NOT NULL,
	`type`	TEXT NOT NULL,
	`ch_read`	INTEGER NOT NULL DEFAULT 0,
	`ch_total`	INTEGER,
	`vol_read`	INTEGER NOT NULL DEFAULT 0,
	`vol_total`	INTEGER,
	`status`	TEXT NOT NULL,
	`date_started`	TEXT,
	`date_finished`	TEXT,
	`mangadb_id`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(id),
	FOREIGN KEY(`type`) REFERENCES manga_types ( type ) on delete restrict on update cascade,
	FOREIGN KEY(`status`) REFERENCES manga_statuses ( status ) on delete restrict on update cascade
);
CREATE TRIGGER fix_vol_counts
after update of vol_read, vol_total on manga for each row
when new.vol_total != 0 and new.vol_read > new.vol_total
begin
update manga set vol_read=new.vol_total where id=new.id;
end;
CREATE TRIGGER fix_ch_counts
after update of ch_read, ch_total on manga for each row
when new.ch_total != 0 and new.ch_read > new.ch_total
begin
update manga set ch_read=new.ch_total where id=new.id;
end;
