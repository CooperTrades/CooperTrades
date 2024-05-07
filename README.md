# CooperTrades
To run this code, you will first need to install this chrome extension: https://chromewebstore.google.com/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf

Then, to you need to start a Postgres docker container on port `5435` with username `postgres` and password `dbpassword`.

Then, inside the `db` directory, run `python3 init_db.py` to initialize the schema and insert some dummy data into the database.

Then, in the home directory, run `python3 app.py` to start the server. 

Finally, move into the `coopertrades-app` directory and run `npm start`. Once that is up, the entire website is ready.