# Rocket-League-Dashboard

[Link to live dashboard](https://app.powerbi.com/view?r=eyJrIjoiNTc2M2UyZDQtODAxYS00MDJkLTgzODEtODc4MTRhMzUxNTJmIiwidCI6IjM1ZWE1YjZhLWVjNjEtNGJhYy05N2I3LWE4NGVhYTc2NWZiMyIsImMiOjF9)
## Background
The purpose of this project is to enhance my ETL skills by building a fully automated data pipeline. 
Taking raw game stats entered via Google Sheets and transforming them into a live Power BI dashboard so I can have 
realtime data-driven insights about my performance in-game.

Rocket League is my favorite video game. It is essentially playing soccer with cars that can fly. Like soccer, the purpose 
of the game is to shoot shots at your opponents net, assist your teammates with passes, save opponent shots from scoring, 
and of course scoring goals. I wanted to compare my performance to my teammates and opponents and see if I can determine 
anything that will give me a better chance to win each match.


![Rocket League Gif](https://i.makeagif.com/media/9-13-2023/NyA8lk.gif)

## Project Workflow
![Workflow diagram](images\Workflow%20Diagram.png)

The project workflow is as follows:
1. After each match, I enter for each player, the score, goals, assists, shots, saves, and overtime length (if applicable) 
into my Google Sheet.
2. My python script `pipeline.py` is executed on a linux VM hosted on a Google Cloud Compute Engine instance via a cron job, 
and extracts the data from my Google Sheet using the pygsheets library.
3. `pipeline.py` then inserts the new game data into a Postgres database also hosted on my Compute Engine VM.
4. Power BI connects to my Postgres database, running sql queries to extract the data and transform into a clean data model 
for analysis via power query.
5. Power BI dashboard is ready for use.

## Setting up VM on Google Cloud
Installing updates, python libraries, and docker.
```
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lab-release
sudo apt install pip
sudo apt install libpq-dev python3-dev
pip install pygsheets \ pandas \ psycopg2
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arcj=$ (dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
curl -o pipeline.py https://raw.githubusercontent.com/Nick-Corona/Rocket-League-Dashboard/main/pipeline.py
```
Then I set my database host and password as environment variables in the system profile.

`sudo nano /etc/profile`

`export db_password=<password>`

`export db_host=<host ip>`

Then I setup my cron jobs and environment variables via `crontab -e`

`30 17 * * TUE,FRI python3 /home/nickccorona/pipeline.py 1 2>&1 >> solo_cronrun.log`

`30 17 * * MON,THU,SAT python3 /home/nickccorona/pipeline.py 2 2>&1 >> doubles_cronrun.log`

`30 17 * * WED python3 /home/nickccorona/pipeline.py 3 2>&1 >> trios_cronrun.log`

I set the cron jobs to run 2v2 most frequently since it's my most-played gamemode.

## Creating Postgres Database
Pulling the Postgres docker image and running the Postgres database.

```
sudo docker pull postgres
sudo docker run --name some-postgres -e POSTGRES_PASSWORD=<password> -v postgres:/lib/postgresql/data -p 5432:5432 -d postgres
```

Then I connect to the database in pgAdmin and create the schemas for solo, doubles, and trios gamemodes and associated 
tables by running the below sql scripts.

`create schemas.sql`

`create tables.sql`

## Connecting Power BI
After creating data sources and connecting to my database I created the data model and wrote the DAX expressions needed for analysis.

![Data model](images\doubles data model.png)

Then the dashboard is ready for use.

https://app.powerbi.com/view?r=eyJrIjoiNTc2M2UyZDQtODAxYS00MDJkLTgzODEtODc4MTRhMzUxNTJmIiwidCI6IjM1ZWE1YjZhLWVjNjEtNGJhYy05N2I3LWE4NGVhYTc2NWZiMyIsImMiOjF9

![Dashboard](images\dashboard.png)
