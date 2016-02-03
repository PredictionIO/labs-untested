# database/
The PostgreSQL database schema and a bunch of queries and functions used for the features extraction.

* _setup.sh_
  * - **description:** script for setting up the database
  * - **usage:** ./setup.sh [database name] [username]
  * - **note:** You have to put all files into /tmp directory first. The setup may take some time.

* _dump.sh_
  * **description:** script for dumping the features into .csv file
  * **usage:** ./dump.sh [database name] [username]
  * **note:** The file containing the extracted features will be created in the /tmp directory (data.csv).

# scripts/
A few R scripts used for testing and evaluating different regression and classification models.

* summary.md - a brief summary of the different classification and regression models

# plots/
Some plots for the fitted models.
