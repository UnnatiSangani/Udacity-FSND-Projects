Project-Logs-Analysis

Project logs analysis is a python application to generate reports based on information from database news.

Databse news is a PostgreSQL database for a fictional news website. Database news has three tables: articles, authors, and log.

1. Table articles contain information of newspaper articles like article author, title and so on.
2. Table authors has information related to news authors, such as author's name.
3. Table log has a database row for each time a reader loaded a web page.

When running the python application, following reports will be generated:

1. The top three most viewed articles
2. Authors and their articles' total views, author with most views first
3. Days where requests leading to errors more than 1%

Running Environment
Python: 3
PostgreSQL: 9.5.8
psycopg: psycopg2 2.7.
Vagrant: 2.3.5
Virtualbox: 6.0

How to Run?

1.Setup Project
1.1 Download and install the virtual box.
Download virtual box from following link:
  [Please, click here to download Virtual box.] (https://www.virtualbox.org/wiki/Downloads)
1.2 Download and install Vagrant VM from following link:
  [Please, click here to download Vagrant.] (https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)

2.Set up the VM
2.1 From your bash terminal, move to the same directory where this Vagrant file is located and run the following command to start VM:
  $ vagrant up
2.2 Then Log in to VM this using command:
  $ vagrant ssh
2.3 Now change directory to /vagrant and go to project folder.

3.Setting up the database and Creating Views:
3.1 Download  the database news from following link:
  [Please, click here to download news database!] (https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3.2 Load the data in local database using the command:
  psql -d news -f newsdata.sql

4.Create views using command:
  psql -d news -f create_view.sql

5.Run the application using command:
python newsdb.py

It will present the answers of the questions.

6.Report
When the application finishes running, three reports will be printed on the screen.
To find out what reports should look like, check 'log-report.txt' file.

License
The content of this repository is licensed under MIT License.