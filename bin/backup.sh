#!/bin/bash
mysqldump -u root -p --all-databases | gzip > mysql_backup.gz
