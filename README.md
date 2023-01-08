# Fetch Rewards #
## Data Engineering Take Home: ETL off a SQS Qeueue ##

This project is the solution for the Data Engineering assignment given in the below link:
https://bitbucket.org/fetchrewards/data-engineering-take-home/src/master/

## To run the code
1. Clone this repo
```bash
git clone https://github.com/prasadashu/data-engineering-fetch-rewards.git
```

2. Go into the cloned repo
```bash
cd data-engineering-fetch-rewards
```

3. Run `make` command to install dependencies
```bash
make pip-install
```

4. Run `make` command to configure aws shell
```bash
make aws-configure
```

5. Pull and start docker containers
```bash
make start
```

6. Run Python code to perform ETL process
```bash
make perform-etl
```

## Checking messages loaded in Postgres
- To validate the messages loaded in Postgres
```bash
psql -d postgres -U postgres  -p 5432 -h localhost -W
```
- Credentials and database information
-- **username**=`postgres`
-- **password**=`postgres`
-- **database**=`postgres`

- If `psql` binary is not installed on Ubuntu based distros, install it using the below command.
```bash
apt install postgresql-client
```