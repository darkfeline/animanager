CREATE TABLE new (
  `id`	INTEGER,
  `name`	text NOT NULL,
  `type`	TEXT NOT NULL,
  `ep_watched`	integer NOT NULL DEFAULT 0 CHECK(ep_total IS NULL OR ep_watched <= ep_total),
  `ep_total`	integer DEFAULT NULL,
  `status`	TEXT NOT NULL,
  `date_started`	text DEFAULT NULL,
  `date_finished`	text DEFAULT NULL,
  `animedb_id`	integer NOT NULL UNIQUE,
  `anidb_id`	INTEGER DEFAULT 0,
  PRIMARY KEY(id),
  FOREIGN KEY(`type`) REFERENCES `anime_types`(`type`) on delete restrict on update cascade,
  FOREIGN KEY(`status`) REFERENCES `anime_statuses`(`status`) on delete restrict on update cascade
);
INSERT INTO new SELECT id, name, type, ep_watched, ep_total, status, date_started, date_finished, animedb_id, 0 FROM anime;
DROP TABLE anime;
ALTER TABLE new RENAME TO new;
