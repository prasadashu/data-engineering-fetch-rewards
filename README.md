# Fetch Rewards #
## Data Engineering Take Home: ETL off a SQS Qeueue ##

## To run the code
1. Clone this repo
```bash
git clone https://github.com/prasadashu/data-engineering-fetch-rewards.git
``

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