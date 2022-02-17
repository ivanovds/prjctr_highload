# 20. Backups

## Assignment
1. Take/create the database from your pet project

2. Implement all kinds of repository models (Full, Incremental, Differential, Reverse Delta, CDP)
- Unstructured
- Full
- Incremental
- Differential
- Reverse Delta
- Continuous Data Protection

3. Compare their parameters:
- size
- ability to roll back at specific time point
- speed of roll back
- cost

## 1. Take/create the database from your pet project
We will populate a PostgreSQL database with a command
```bash
docker-compose up
```

When the `seed.rb` script completes, we can ckeck the data is populated:

```bash
docker-compose exec postgres psql -h localhost -d mydb -U app

select count(*) from books;
 1001000
```

## 2. Implement all kinds of repository models (Full, Incremental, Differential, Reverse Delta, CDP)

```sql
mydb=# SELECT pg_size_pretty( pg_database_size('mydb') );
 pg_size_pretty
----------------
 101 MB
(1 row)
```

The database size is 101 MB. The folder containing all DB data takes 384,4 MB on the disk.

Let's try various backup strategies

### Unstructured
We save the data on external drive.
```bash
mkdir -p ../data/backups
tar czf ../data/backups/20_backups__.tar.gz ../data/postgres/20_backups__

ls -lh ../data/backups
total 149504
-rw-r--r--  1 vb  staff    73M 13 Feb 08:39 20_backups__.tar.gz
```

As we can see, the archive size is 73M, which is 5.26 times smaller than the original folder.

To roll the database back, we just have to unpack the archive.

### Full
Even though we can play with [building an ISO image from Docker Container](https://iximiuz.com/en/posts/from-docker-container-to-bootable-linux-disk-image/), much convinient way to explore full backups is to make a regular database backup.

```bash
docker-compose exec postgres bash

time pg_dump -U app -F t --gzip mydb > /backups/full_pg_dump.tar
real    0m7.200s
user    0m0.276s
sys     0m0.479s

ls -lh /backups | grep full
-rw-r--r--    1 root     root       34.2M Feb 13 07:55 full_pg_dump.tar
```

The backup size is 34.2 MB and it took 7.2 seconds to back it up. Let's create `mydb_full` and measure how much time it needs to be created out from the backup

```bash
psql -U app -d mydb

CREATE DATABASE mydb_full;
\q

time pg_restore -c -U app -d mydb_full -v "/backups/full_pg_dump.tar"
real    0m45.305s
user    0m0.012s
sys     0m0.061s
```

It took 45 seconds.

### Incremental
PostgreSQL supports `Wal_Archiving`, we can use it to implement incremental backups.
`pg_basebackup` command dumps the system along with WAL filles. To recover from a backup, we restore the last good backup and replay the WALs from the point in time from the last backup.

Cons: backups are always taken of the entire database cluster. It is impossible to back up individual databases or database objects.

Back-up:

```bash
time pg_basebackup -U app -h localhost -z -P -X stream --format tar -D /backups/incremental/server
234041/234041 kB (100%), 1/1 tablespace

real    0m20.379s
user    0m8.564s
sys     0m1.025s

ls -lh /backups/incremental/server
total 35M
-rw-------    1 root     root      221.0K Feb 13 10:02 backup_manifest
-rw-------    1 root     root       35.0M Feb 13 10:02 base.tar.gz
-rw-------    1 root     root       16.7K Feb 13 10:02 pg_wal.tar.gz
```

`backup_label` file contains important data to perform point-in-time recovery:
```bash
cat /backups/incremental/unarchived/backup_label

START WAL LOCATION: 0/16000028 (file 000000010000000000000016)
CHECKPOINT LOCATION: 0/16000060
BACKUP METHOD: streamed
BACKUP FROM: primary
START TIME: 2022-02-13 10:02:25 UTC
LABEL: pg_basebackup base backup
START TIMELINE: 1
```
`cat /backups/incremental/unarchived/tablespace_map` returs empty result, therefore there are no tablespaces

Let's restore from the backup:

```bash
docker-compose down
docker-compose run --rm postgres bash
su - postgres
rm -rf /var/lib/postgresql/data/*

time tar xzf /backups/incremental/server/base.tar.gz -C /var/lib/postgresql/data/
real    0m 27.81s
user    0m 2.36s
sys     0m 1.96s

mkdir -p /backups/incremental/archived_wals/
time tar xzf /backups/incremental/server/pg_wal.tar.gz -C /backups/incremental/archived_wals/
real    0m 0.41s
user    0m 0.12s
sys     0m 0.06s

echo "restore_command = 'cp /backups/incremental/archived_wals/%f \"%p\" '" >> /var/lib/postgresql/data/postgresql.conf
touch /var/lib/postgresql/data/recovery.signal
```

Now start the `postgresql`
```bash
docker-compose up
```

As we observe, the DB is up and running. WAL files were restored:
```bash
postgres_1  | 2022-02-13 15:54:28.379 UTC [25] LOG:  restored log file "000000010000000000000016" from archive
```

The whole process took about 50 seconds, but it is much more complex than a full backup.

### Differencial

### Reverse Delta
### Continuous Data Protection

## 3. Compare their parameters:
- size
- ability to roll back at specific time point
- speed of roll back
- cost

|  | Size (MB)  | point-in-time recovery | roll-back speed | Cost |
| :-----: | :-: | :-: | :-: | :-: |
| Unstructured | 73 | Limited to the time the back-up was made | 20s | Low |
| Full | 34.2 | Limited to the time the back-up was made | 45.3s | Low |
| Incremental | 25 | Full support | 50s | Low, but more complex |
| Differencial | MB |  |  |  |
| Reverse Delta | MB |  |  |  |
| Continuous Data Protection | MB |  |  |  |

## References
- [Continuous Data Protection (CDP)](https://www.baculasystems.com/continuous-data-protection-solutions/)
- [PostgreSQL Backup](https://www.postgresqltutorial.com/postgresql-backup-database/)
- [pg_basebackup](https://www.postgresql.org/docs/current/app-pgbasebackup.html )
- [Backup and Restore a PostgreSQL Cluster With Multiple Tablespaces Using pg_basebackup](https://www.percona.com/blog/2018/12/21/backup-restore-postgresql-cluster-multiple-tablespaces-using-pg_basebackup/#:~:text=Backup%20and%20Restore%20a%20PostgreSQL%20Cluster%20With%20Multiple%20Tablespaces%20Using%20pg_basebackup,-Back%20to%20the&text=pg_basebackup%20is%20a%20widely%20used,set%20up%20a%20slave%2Fstandby.)
- [pg_basebackup / pg-barman – restore tar backup](http://postgresql.freeideas.cz/pg_basebackup-pgbarman-restore-tar-backup/)
- [26.3. Continuous Archiving and Point-in-Time Recovery (PITR)](https://www.postgresql.org/docs/14/continuous-archiving.html)
- [Backup rotation scheme](https://en.wikipedia.org/wiki/Backup_rotation_scheme)
- [Backup PostgreSQL databases with Barman](https://www.scaleway.com/en/docs/tutorials/back-up-postgresql-barman/)
## Questions
