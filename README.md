# Fetch Rewards #
## Data Engineering Take Home: ETL off a SQS Qeueue ##

You may use any programming language to complete this exercise. We strongly encourage you to write a README to explain how to run your application and summarize your thought process.

## What do I need to do?
This challenge will focus on your ability to write a small application that can read from an AWS SQS Qeueue, transform that data, then write to a Postgres database. This project includes steps for using docker to run all the components locally, **you do not need an AWS account to do this take home.**

Your objective is to read JSON data containing user login behavior from an AWS SQS Queue that is made available via [localstack](https://github.com/localstack/localstack). Fetch wants to hide personal identifiable information (PII). The fields `device_id` and `ip` should be masked, but in a way where it is easy for data analysts to identify duplicate values in those fields.

Once you have flattened the JSON data object and masked those two fields, write each record to a Postgres database that is made available via [Postgres's docker image](https://hub.docker.com/_/postgres). Note the target table's DDL is:

```sql
-- Creation of user_logins table

CREATE TABLE IF NOT EXISTS user_logins(
    user_id             varchar(128),
    device_type         varchar(32),
    masked_ip           varchar(256),
    masked_device_id    varchar(256),
    locale              varchar(32),
    app_version         integer,
    create_date         date
);
```

You will have to make a number of decisions as you develop this solution:

*    How will you read messages from the queue?
*    What type of data structures should be used?
*    How will you mask the PII data so that duplicate values can be identified?
*    What will be your strategy for connecting and writing to Postgres?
*    Where and how will your application run?

**The recommended time to spend on this take home is 2-3 hours.** Make use of code stubs, doc strings, and a next steps section in your README to elaborate on ways that you would continue fleshing out this project if you had the time. For this assignment an ounce of communication and organization is worth a pound of execution.

## Project Setup
1. Fork this repository to a personal Github, GitLab, Bitbucket, etc... account. We will not accept PRs to this project.
2. You will need the following installed on your local machine
    * make
        * Ubuntu -- `apt-get -y install make`
        * Windows -- `choco install make`
        * Mac -- `brew install make`
    * python3 -- [python install guide](https://www.python.org/downloads/)
    * pip3 -- `python -m ensurepip --upgrade` or run `make pip-install` in the project root
    * awslocal -- `pip install awscli-local`  or run `make pip install` in the project root
    * docker -- [docker install guide](https://docs.docker.com/get-docker/)
    * docker-compose -- [docker-compose install guide]()
3. Run `make start` to execute the docker-compose file in the the project (see scripts/ and data/ directories to see what's going on, if you're curious)
    * An AWS SQS Queue is created
    * A script is run to write 100 JSON records to the queue
    * A Postgres database will be stood up
    * A user_logins table will be created in the public schema
4. Test local access
    * Read a message from the queue using awslocal, `awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue`
    * Connect to the Postgres database, verify the table is created
    * username = `postgres`
    * database = `postgres`
    * password = `postgres`

```bash
# password: postgres

psql -d postgres -U postgres  -p 5432 -h localhost -W
Password: 

postgres=# select * from user_logins;
 user_id | device_type | hashed_ip | hashed_device_id | locale | app_version | create_date 
---------+-------------+-----------+------------------+--------+-------------+-------------
(0 rows)
```
5. Run `make stop` to terminate the docker containers and optionally run `make clean` to clean up docker resources.

## All done, now what?
Upload your codebase to a public Git repo (GitHub, Bitbucket, etc.) and email us the link.  Please double-check this is publicly accessible.

Please assume the evaluator does not have prior experience executing programs in your chosen language and needs documentation understand how to run your code
