# AskMate (Sprint 3)

## Story

Last week you made a very good progress to improve your web application.
We need some more features to make it more usable and more appealing to users.

Users requested new features like ability to register and login.
There are a few other feature requests which you can find in the user stories.

The management would like you to separate the already working features from
the upcoming ones so your development team need to **start use branching
workflow and open new branches for the features you start in this sprint**.
As last week the ownership is in your hand so there is no compulsory stories
but of course the best case according to them if all of the stories are implemented.
So first, choose the stories and after that ask a mentor to validate it.

As last week you have a **prioritized list** of new user stories that you should
add to the unfinished stories from last weeks on your product backlog. Try to
estimate these new stories as well and based on the estimations decide how many
your team can finish until the demo. As the order is important, you should choose
from the beginning of the list as much as you can.

## What are you going to learn?

- Web routing and redirects,
- Gitflow workflow
- Advanced SQL commands (`JOIN`, `GROUP BY`, and aggregate functions)
- User authentication with sessions
- Hashed passwords
- HTML and the Jinja2 templating engine

## Tasks

1. As you will work in a new repository but you need the code from the previous sprint, add the `ask-mate-3` repository as a new remote to the previous sprint's repository, then pull (merge) and push your changes into it.
    - There is a merge commit in the project's repository that contains code from the previous sprint

2. As a user I would like to have the possibility to register a new account into the system.
    - There is a `/registration` page
    - The page is linked from the front page
    - Theres is a form on the `/registration` page when a request is issued with `GET` method
    - The form ask for username (email address), password and issues a `POST` request to `/registration` on submit
    - After submitting you are redirected back to the main page and the new user account is saved in the database
    - For a user account we store the email as username a password hash and the date of the registration

3. As a registered user, I'd like to be able to login to the system with my previously saved username and password.
    - There is a `/login` page
    - The page is linked from the front page
    - Theres is a form on the `/login` page when a request is issued with `GET` method
    - The form ask for username (email address), password and issues a `POST` request to `/login` on submit
    - After submitting you are redirected back to the main page and the given user is logged in
    - It is only possible to ask or answer a question if the user is logged in

4. There should be a page where I can list all the registered users with all their attributes.
    - There is a `/users` page
    - The page is linked from the front page when I'm logged in
    - The page is not accessible when I'm not logged in
    - Theres is a `<table>` with user data in it. The table should have these details of a user:
  - User name (link to user page if implemented)
  - Registration date
  - Count of asked questions (if binding implemented)
  - Count of answers (if binding implemented)
  - Count of comments (if binding implemented)
  - Reputation (if implemented)

5. As a user when I add a new question I would like to be saved as the user who creates the new question.
    - The user id of the currently logged in user is saved when a new question is saved

6. As a user when I add a new answer I would like to be saved as the user who creates the new answer.
    - The user id of the currently logged in user is saved when a new answer is saved

7. As a user when I add a new comment I would like to be saved as the user who creates the new comment.
    - The user id of the currently logged in user is saved when a new comment is saved

8. There should be a page where we can see all details and activities of a user.
    - There is a `/user/<user_id>` page
    - The user page of a logged in user is linked from the front page
    - The page of every user is linked from the users list page
    - Theres is a list with these deatils about the user:
  - User id
  - User name (link to user page if implemented)
  - Registration date
  - Count of asked questions (if binding implemented)
  - Count of answers (if binding implemented)
  - Count of comments (if binding implemented)
  - Reputation (if implemented)
    - There is a separate table where every **question** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **answer** is listed that the user created. The related question is linked in every line.
    - There is a separate table where every **comment** is listed that the user created. The related question is linked in every line.

9. As a user I would like to have the possibility to mark an answer as accepted.
    - On a question's page for every answer there is a clickable element that can be used to mark an answer as accepted
    - When there is an accepted answer there is an option to remove the accepted state
    - Only the user who asked the question can change the accepted state of answers
    - An accpted answer has a visual distinction from other answers

10. As a user I would like to see a reputation system to strengthen the community. Reputation is a rough measurement
 of how much the community trusts a user.
    - **A user gains reputation when:**
- her/his question is voted up: +5
- her/his answer is voted up: +10
- her/his answer is marked "accepted": +15

11. As a user I would like to see a small drop in reputation when a user's question or answer is voted down.
    - **A user loses reputation when:**
- her/his question is voted down: −2
- her/his answer is voted down: −2

12. There should be a page where I can list all the existing tags and that how many questions are marked with the given tags
    - There is a `/tags` page
    - The page is linked from the front page and a question's page
    - The page is accessible when I'm not logged in

## General requirements

- Use gitflow workflow from now on in your team projects.

## Hints

- As you have became familiar with the `CREATE` statement the management
  hasn't prepared the data model. They trust in you and they are certain
  about you can design this small extension for the current database.
  To change the already existing tables you will need to use the
  `ALTER TABLE` statement. For this you can find some help
  [here](https://www.w3schools.com/sql/sql_alter.asp).
  (Do not forget to setup the foreign keys if those are necessary)
- It's important that if the database table has a timestamp column
  then you cannot insert a UNIX timestamp value directly into that
  table, you should use:
    - either strings in the following format `'1999-01-08 04:05:06'`,
    - or if you use `psycopg2` and the `datetime` module, you can pass
      a `datetime` object to the SQL query as a parameter (you'll find
      details about Date/Time handling in psycopg2 in the background materials).
- Pay attention on the order of inserting data into the tables, because you may
  violate foreign key constraints (that means e.g. if you insert data into the
  question_tag before you insert into the tag table the corresponding tag id
  you want to refer to then it won't exist yet)! Especially it is important
  after you change the database structure with new foreign keys. Maybe it's
  worth to modify the sample data based on your changes.
- Because you have learnt about how to write complex queries and join multiple
  tables in one select maybe you should spend some time to optimise your
  previously created queries where it's applicable.
- Pay attention that some user stories have prerequisites!

## Background materials

### Git

- <i class="far fa-exclamation"></i> [Working with the `git remote` command](https://git-scm.com/docs/git-remote)
- <i class="far fa-book-open"></i> [Merge vs rebase](project/curriculum/materials/pages/git/merge-vs-rebase.md)
- <i class="far fa-book-open"></i> [Mastering git](project/curriculum/materials/pages/git/mastering-git.md)

### SQL

- <i class="far fa-exclamation"></i> [Working with more complex data](project/curriculum/materials/pages/sql/sql-working-with-data.md)
- [SQL injection](project/curriculum/materials/pages/web-security/sql-injection.md)
- [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)
- [Database glossary](project/curriculum/materials/pages/sql/database-glossary.md)

### Workflow

- <i class="far fa-exclamation"></i> [Gitflow workflow](project/curriculum/materials/pages/git/git-branching.md)

### Web basics (Sessions/Flask)

- <i class="far fa-exclamation"></i> [Sessions](project/curriculum/materials/pages/web/authentication-sessions.md)
- <i class="far fa-exclamation"></i> [Salted password hashing](project/curriculum/materials/pages/web-security/salted-password-hashing.md)
- <i class="far fa-exclamation"></i> [Flask documentation](http://flask.palletsprojects.com/) (especially the quickstart#the-request-object and quickstart#sessions part)
- [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- <i class="far fa-book-open"></i> [HTTP is stateless](project/curriculum/materials/pages/web/authentication-http-stateless.md)
- <i class="far fa-book-open"></i> [Cookies](project/curriculum/materials/pages/web/authentication-cookies.md)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- <i class="far fa-book-open"></i> [Collection of web resources](project/curriculum/materials/pages/web/resources.md)






# AskMate (sprint 2)

## Story

Last week you created a pretty good site from scratch. It already has some features but it's a bit difficult to maintain due to the fact that we store data in csv files and we also need some more features to make it more usable and more appealing to users.

The management decided to move further as users requested new features like ability to comment on answers and tag questions (and here is the issue with csv files as well). There are several other feature requests which you can find in the user stories.

As last week the management is handing out a **prioritized list** of new user stories that you should add to the unfinished stories from last week on your product backlog. Try to estimate these new stories as well and based on the estimations decide how many your team can finish until the demo. As the order is important, you should choose from the beginning of the list as much as you can.

## What are you going to learn?

- how to use `psycopg2` to connect to a PostgreSQL database from Python,
- SQL basic commands (`SELECT`, `UPDATE`, `DELETE`, `INSERT`)
- CSS basics
- how to work according to the Scrum framework,
- how to create a _sprint plan_.

## Tasks

1. As you will work in a new repository but you need the code from the previous sprint, add the `ask-mate-2` repository as a new remote to the previous sprint's repository, then pull (merge) and push your changes into it.
    - There is a merge commit in the project's repository that contains code from the previous sprint

2. Make the application use a database instead of CSV files.
    - The application uses a PostgreSQL database instead of CSV files
    - The application respects the `PSQL_USER_NAME`, `PSQL_PASSWORD`, `PSQL_HOST` and `PSQL_DB_NAME` environment variables
    - The database structure (tables) is the same as in the provided SQL file (`sample_data/askmatepart2-sample-data.sql`)

3. Allow the user to add comments to a question.
    - There is a `/question/<question_id>/new-comment` page
    - The page is linked from the question's page
    - There is a form with `message` field, and issues `POST` requests
    - After submitting, you are redirected back to the question detail page, and the new comment appears together with submission time

4. Allow the user to add comments to an answer.
    - There is a `/answer/<answer_id>/new-comment` page
    - The page is linked from the question's page, next to or below the answer
    - There is a form with `message` field, and issues `POST` requests
    - After submitting, you are redirected back to the question detail page, and the new comment appears together with submission time

5. Implement searching in questions and answers. (Hint: [Passing data from browser](https://learn.code.cool/web-python/#/../pages/web/passing-data-from-browser))

    - There is a search box and "Search" button on the main page
    - When you write something and press the button, you see a results list of questions (same data as in the list page)
    - The results list contains questions for which the title or description contain the searched phrase
    - The results list also contains questions which have answers for which the message contains the searched phrase
    - The results list has the following URL: `/search?q=<search phrase>`

6. Allow the user to edit the posted answers.
    - There is a `/answer/<answer_id>/edit` page
    - The page is linked from the answer's page
    - There is a form with a `message` field, and issues a `POST` request
    - The field is pre-filled with existing answer's data
    - After submitting, you are redirected back to the question detail page, and the answer is updated

7. Allow the user to edit comments.
    - The page URL is `/comment/<comment_id>/edit`
    - There is a link to the edit page next to each comment
    - The page contains a `POST` form with a `message` field
    - The field pre-filled with current comment message
    - After submitting, you are redirected back to question detail page, and the new comment appears
    - The submission time is updated
    - There is a message that says "Edited `<number_of_editions>` times." next to or below the comment

8. Allow the user to delete comments.
    - There is a recycle bin icon next to the comment
    - Clicking the icon asks the user to confirm the deletion
    - The deletion itself is implemented by the `/comments/<comment_id>/delete` endpoint (which does not ask for confirmation anymore)
    - After deleting, you are redirected back to question detail page, and the comment is not showed anymore

9. Display latest 5 questions on the main page (`/`).
    - The main page (`/`) displays the latest 5 submitted questions
    - The main page contains a link to all of the questions (`/list`)

10. Implement sorting for the question list. [If you did this user story in the previous sprint, now you only have to rewrite it to use SQL]
    - The question list can be sorted by title, submission time, message, number of views, and number of votes
    - You can choose the direction: ascending or descending
    - The order is passed as query string parameters, for example `/list?order_by=title&order_direction=desc`

11. Add tags to questions.
    - The tags are displayed on the question detail page
    - There is an "add tag" link which leads to the page for adding a tag
    - The page for adding a tag has the URL `/question/<question_id>/new-tag`
    - The page allows to either choose from existing tags, or define a new one.

12. Highlight the search phrase in the search results.
    - On the search results page, the searched phrase should be highlighted
    - If the phrase is found in an answer, the answer is also displayed (slightly indented)
    - The search phrase is also highlighted in the answers

13. Allow the user to delete tags from questions
    - There is an X link next to each tag
    - Clicking that link deletes the tag and reloads the question page
    - The deletion is implemented as `/question/<question_id>/tag/<tag_id>/delete` endpoint

## General requirements

None

## Hints

- It's important that if the database table has a timestamp column then you cannot insert a UNIX timestamp value directly into that table, you should use:
    - either strings in the following format '1999-01-08 04&colon;05&colon;06',
    - or if you use psycopg2 and the datetime module, you can pass a datetime object to the SQL query as parameter (details in the background materials: [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation))
- Pay attention on the order of inserting data into the tables, because you may violate foreign key constraints (that means e.g. if you insert data into the question_tag before you insert into the tag table the corresponding tag id you want to refer to then it won't exist yet)!
- You can import the sample data file into `psql` with the `\i` command or run it via the Database tool in PyCharm.
- Some user stories may require to deal with CSS as well, but do not deal with CSS too much. It's more important that you write proper queries, have a working connection with psycopg2, have a clean Python code than create an amazingly beautiful web application (although if you have time, of course it's not forbidden to do so :smiley:).

### Data models

All data should be persisted in a PostgreSQL database in the following tables (you can ignore data in the not implemented fields):

![AskMate data model part 2](media/web-python/askmate-data-model-part-2.png)

**question table**<br>
*id:* A unique identifier for the question<br>
*submission_time:* The date and time when the question was posted<br>
*view_number:* How many times this question was displayed in the single question view<br>
*vote_number:* The sum of votes this question has received<br>
*title:* The title of the question<br>
*message:* The question text<br>
*image:* the path to the image for this question<br>

**answer table**<br>
*id:* A unique identifier for the answer<br>
*submission_time:* The date and time when the answer was posted<br>
*vote_number:* The sum of votes this answer has received<br>
*question_id:* The id of the question this answer belongs to<br>
*message:* The answer text<br>
*image:* The path to the image for this answer<br>

**tag table**<br>
*id:* A unique identifier for the tag<br>
*name:* The name of the tag<br>

**question_tag table**<br>
*question\_id:* The id of the question the tag belongs to<br>
*tag\_id:* The id of the tag belongs to the question<br>

**comment table**<br>
*id:* A unique identifier for the comment<br>
*question\_id:* The id of the question this comment belongs to (if the comment belongs to an answer, the value of this field should be NULL)<br>
*answer\_id:* The id of the answer this comment belongs to (if the comment belongs to a question, the value of this field should be NULL)<br>
*message:* The comment text<br>
*submission\_time:* The date and time the comment was posted or updated<br>
*edited\_number::* How many times this comment was edited<br>

### Database and sample data

To init the database use the `sample_data/askmatepart2-sample-data.sql` file in your repository.

## Background materials

### Git

- <i class="far fa-exclamation"></i> [Working with the `git remote` command](https://git-scm.com/docs/git-remote)
- <i class="far fa-book-open"></i> [Merge vs rebase](project/curriculum/materials/pages/git/merge-vs-rebase.md)
- <i class="far fa-book-open"></i> [Mastering git](project/curriculum/materials/pages/git/mastering-git.md)

### SQL

- <i class="far fa-exclamation"></i> [Installing and setting up PostgreSQL](project/curriculum/materials/pages/tools/installing-postgresql.md)
- <i class="far fa-exclamation"></i> [Installing psycopg2](project/curriculum/materials/pages/tools/installing-psycopg2.md)
- <i class="far fa-exclamation"></i> [Best practices for Python/Psycopg/Postgres](project/curriculum/materials/pages/python/tips-python-psycopg-postgres.md)
- [Setting up a database connection in PyCharm](project/curriculum/materials/pages/tools/pycharm-database.md)
- [Date/Time handling in psycopg2](https://www.psycopg.org/docs/usage.html?highlight=gunpoint#date-time-objects-adaptation)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page on Queries](https://www.postgresql.org/docs/current/queries.html)
- <i class="far fa-book-open"></i> [PostgreSQL documentation page Data Manipulation](https://www.postgresql.org/docs/current/dml.html)
- [Database glossary](project/curriculum/materials/pages/sql/database-glossary.md)

### Agile/SCRUM

- [Agile project management](project/curriculum/materials/pages/methodology/agile-project-management.md)
- <i class="far fa-book-open"></i> [Planning poker](https://en.wikipedia.org/wiki/Planning_poker)

### Web basics (Flask/Jinja/HTML/CSS)

- <i class="far fa-exclamation"></i> [Flask/Jinja Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- <i class="far fa-exclamation"></i> [Passing data from browser](project/curriculum/materials/pages/web/passing-data-from-browser.md)
- [Collection of web resources](project/curriculum/materials/pages/web/resources.md)
- <i class="far fa-book-open"></i> [Pip and VirtualEnv](project/curriculum/materials/pages/python/pip-and-virtualenv.md)
- <i class="far fa-book-open"></i> [A web-framework for Python: Flask](project/curriculum/materials/pages/python/python-flask.md)
- <i class="far fa-book-open"></i> [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)

# AskMate (sprint 1)

## Story

Its time to put your newly acquired Flask skills to use! Your next big task will be to implement a crowdsourced Q&A site, like Stack Overflow.

The initial version of the site should be able to handle questions and answers, there is no need for other functionality like user management or comments for questions/answers.

The management was very interested in the agile development methodologies that they just recently hear about, thus they are handing out a **prioritized list** of user stories called a product backlog. Try to estimate how many of these stories your team can finish until the demo. As the order is important, you should choose from the beginning of the list as much as you can, **the first four stories are the most important**.

## What are you going to learn?

- create a Flask project
- use routes with Flask
- use HTML and the Jinja templating engine
- CSV handling

## Tasks

1. Implement the `/list` page that displays all questions.
    - The page is available under `/list`
    - Load and display the data from `question.csv`
    - Sort the questions by the latest question on top

2. Create the `/question/<question_id>` page that displays a question and the answers for it.
    - The page is available under `/question/<question_id>`
    - There are links to the question pages from the list page
    - The page displays the question title and message
    - The page displays all the answers to a question

3. Implement a form that allows you to add a question.
    - There is an `/add-question` page with a form
    - The page is linked from the list page
    - There is a POST form with at least `title` and `message` fields
    - After submitting, you are redirected to "Display a question" page of this new question

4. Implement posting a new answer.
    - The page URL is `/question/<question_id>/new-answer`
    - The question detail page links to this page
    - The page has a POST form with a form field called `message`
    - Posting an answer redirects you back to the question detail page, and the new answer is there

5. Implement sorting for the question list.
    - The question list can be sorted by title, submission time, message, number of views, and number of votes
    - You can choose the direction: ascending or descending
    - The order is passed as query string parameters, for example `/list?order_by=title&order_direction=desc`

6. Implement deleting a question.
    - Deleting is implemented by the `/question/<question_id>/delete` endpoint
    - There should be a deletion link on the question page
    - Deleting redirects you back to the list of questions

7. Allow the user to upload an image for a question or answer.
    - The forms for adding question and answer contain an "image" file field
    - You can attach an image (.jpg, .png)
    - The image is saved on server and displayed next to question / answer
    - When you delete the question / answer, the file gets deleted as well

8. Implement editing an existing question.
    - There is a `/question/<question_id>/edit` page
    - The page is linked from the question's page
    - There is a POST form with at least `title` and `message` fields
    - The fields are pre-filled with existing question's data
    - After submitting, you are redirected back to "Display a question" page and you see the changed data

9. Implement deleting an answer.
    - Deleting is implemented by `/answer/<answer_id>/delete` endpoint
    - There should be a deletion link on the question page, next to an answer
    - Deleting redirects you back to the question detail page

10. Implement voting on questions.
    - Vote numbers are displayed next to questions on the question list page
    - There are "vote up/down" links next to questions on the question list page
    - Voting uses `/question/<question_id>/vote_up` and `/question/<question_id>/vote_down` endpoints
    - Voting up increases, voting down decreases the `vote_number` of the question by one
    - Voting redirects you back to the question list

11. Implement voting on answers.
    - Vote numbers are displayed next to answers on the question detail page
    - There are "vote up/down" links next to answers
    - Voting uses `/answer/<answer_id>/vote_up` and `/answer/<answer_id>/vote_down` endpoints
    - Voting up increases, voting down decreases the `vote_number` of the answer by one
    - Voting redirects you back to the question detail page

## General requirements

- All data should be persisted to `.csv` files. You will need a `questions.csv` for storing all questions and an `answers.csv` for storing all answers.

## Hints

### Project structure

We recommend that you split the code into modules according to clean code principles: Do not put more than 100-150 lines of code into a single file, files should contain logically the same things, etc.

For example, you could split it up to these 3+1 parts:

**Layer** | **Example filename** | **What should it do/contain?**
---|---|---
Routing layer | `server.py` | Flask stuff (server, routes, request handling, session, etc.)<br>This layer should consist of logic that is related to Flask. (with other words: this should be the only file importing from Flask)
Persistence layer | `data_manager.py` | Layer between the server and the data. Functions here should be called from the server.py and these should use generic functions from the connection.py
CSV _(later SQL)_ connection layer |  `connection.py | Common functions to read/write/append CSV files without feature specific knowledge.<br>The layer that have access to any kind of long term data storage. In this case, we use CSV files, but later on we'll change this to SQL database.
Utility "layer" | util.py | Helper functions which can be called from any other layer. (but mainly from the business logic layer)

This is just one way to structure your code, you don't have to follow it _strictly_.

### Data models

In the `sample_data` folder you'll see two sample files for questions and answers.

These look like the following (you can ignore data in the not implemented fields):

**question.csv**<br>
*id:* A unique identifier for the question<br>
*submission_time:* The UNIX timestamp when the question was posted<br>
*view_number:* How many times this question was displayed in the single question view<br>
*vote_number:* The sum of votes this question has received<br>
*title:* The title of the question<br>
*message:* The question text<br>
*image:* The path to the image for this question<br>

**answer.csv**<br>
*id:* A unique identifier for the answer<br>
*submission_time:* The UNIX timestamp when the answer was posted<br>
*vote_number:* The sum of votes this answer has received<br>
*question_id:* The id of the question this answer belongs to.<br>
*message:* The answer text<br>
*image:* the path to the image for this answer<br>

## Background materials

- <i class="far fa-exclamation"></i> [Understanding the web](project/curriculum/materials/pages/web/understanding-the-web.md)
- <i class="far fa-exclamation"></i> [Introduction to HTML](project/curriculum/materials/tutorials/introduction-to-html.md)
- <i class="far fa-exclamation"></i> [Pip and VirtualEnv](project/curriculum/materials/pages/python/pip-and-virtualenv.md)
- <i class="far fa-exclamation"></i> [A web-framework for Python: Flask](project/curriculum/materials/pages/python/python-flask.md)
- <i class="far fa-book-open"></i> [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- <i class="far fa-book-open"></i> [HTML tutorials and references on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- [About unique identifiers](project/curriculum/materials/pages/general/unique-id.md)

# AskMate (sprint 1)

## Story

Its time to put your newly acquired Flask skills to use! Your next big task will be to implement a crowdsourced Q&A site, like Stack Overflow.

The initial version of the site should be able to handle questions and answers, there is no need for other functionality like user management or comments for questions/answers.

The management was very interested in the agile development methodologies that they just recently hear about, thus they are handing out a **prioritized list** of user stories called a product backlog. Try to estimate how many of these stories your team can finish until the demo. As the order is important, you should choose from the beginning of the list as much as you can, **the first four stories are the most important**.

## What are you going to learn?

- create a Flask project
- use routes with Flask
- use HTML and the Jinja templating engine
- CSV handling

## Tasks

1. Implement the `/list` page that displays all questions.
    - The page is available under `/list`
    - Load and display the data from `question.csv`
    - Sort the questions by the latest question on top

2. Create the `/question/<question_id>` page that displays a question and the answers for it.
    - The page is available under `/question/<question_id>`
    - There are links to the question pages from the list page
    - The page displays the question title and message
    - The page displays all the answers to a question

3. Implement a form that allows you to add a question.
    - There is an `/add-question` page with a form
    - The page is linked from the list page
    - There is a POST form with at least `title` and `message` fields
    - After submitting, you are redirected to "Display a question" page of this new question

4. Implement posting a new answer.
    - The page URL is `/question/<question_id>/new-answer`
    - The question detail page links to this page
    - The page has a POST form with a form field called `message`
    - Posting an answer redirects you back to the question detail page, and the new answer is there

5. Implement sorting for the question list.
    - The question list can be sorted by title, submission time, message, number of views, and number of votes
    - You can choose the direction: ascending or descending
    - The order is passed as query string parameters, for example `/list?order_by=title&order_direction=desc`

6. Implement deleting a question.
    - Deleting is implemented by the `/question/<question_id>/delete` endpoint
    - There should be a deletion link on the question page
    - Deleting redirects you back to the list of questions

7. Allow the user to upload an image for a question or answer.
    - The forms for adding question and answer contain an "image" file field
    - You can attach an image (.jpg, .png)
    - The image is saved on server and displayed next to question / answer
    - When you delete the question / answer, the file gets deleted as well

8. Implement editing an existing question.
    - There is a `/question/<question_id>/edit` page
    - The page is linked from the question's page
    - There is a POST form with at least `title` and `message` fields
    - The fields are pre-filled with existing question's data
    - After submitting, you are redirected back to "Display a question" page and you see the changed data

9. Implement deleting an answer.
    - Deleting is implemented by `/answer/<answer_id>/delete` endpoint
    - There should be a deletion link on the question page, next to an answer
    - Deleting redirects you back to the question detail page

10. Implement voting on questions.
    - Vote numbers are displayed next to questions on the question list page
    - There are "vote up/down" links next to questions on the question list page
    - Voting uses `/question/<question_id>/vote_up` and `/question/<question_id>/vote_down` endpoints
    - Voting up increases, voting down decreases the `vote_number` of the question by one
    - Voting redirects you back to the question list

11. Implement voting on answers.
    - Vote numbers are displayed next to answers on the question detail page
    - There are "vote up/down" links next to answers
    - Voting uses `/answer/<answer_id>/vote_up` and `/answer/<answer_id>/vote_down` endpoints
    - Voting up increases, voting down decreases the `vote_number` of the answer by one
    - Voting redirects you back to the question detail page

## General requirements

- All data should be persisted to `.csv` files. You will need a `questions.csv` for storing all questions and an `answers.csv` for storing all answers.

## Hints

### Project structure

We recommend that you split the code into modules according to clean code principles: Do not put more than 100-150 lines of code into a single file, files should contain logically the same things, etc.

For example, you could split it up to these 3+1 parts:

**Layer** | **Example filename** | **What should it do/contain?**
---|---|---
Routing layer | `server.py` | Flask stuff (server, routes, request handling, session, etc.)<br>This layer should consist of logic that is related to Flask. (with other words: this should be the only file importing from Flask)
Persistence layer | `data_manager.py` | Layer between the server and the data. Functions here should be called from the server.py and these should use generic functions from the connection.py
CSV _(later SQL)_ connection layer |  `connection.py | Common functions to read/write/append CSV files without feature specific knowledge.<br>The layer that have access to any kind of long term data storage. In this case, we use CSV files, but later on we'll change this to SQL database.
Utility "layer" | util.py | Helper functions which can be called from any other layer. (but mainly from the business logic layer)

This is just one way to structure your code, you don't have to follow it _strictly_.

### Data models

In the `sample_data` folder you'll see two sample files for questions and answers.

These look like the following (you can ignore data in the not implemented fields):

**question.csv**<br>
*id:* A unique identifier for the question<br>
*submission_time:* The UNIX timestamp when the question was posted<br>
*view_number:* How many times this question was displayed in the single question view<br>
*vote_number:* The sum of votes this question has received<br>
*title:* The title of the question<br>
*message:* The question text<br>
*image:* The path to the image for this question<br>

**answer.csv**<br>
*id:* A unique identifier for the answer<br>
*submission_time:* The UNIX timestamp when the answer was posted<br>
*vote_number:* The sum of votes this answer has received<br>
*question_id:* The id of the question this answer belongs to.<br>
*message:* The answer text<br>
*image:* the path to the image for this answer<br>

## Background materials

- <i class="far fa-exclamation"></i> [Understanding the web](project/curriculum/materials/pages/web/understanding-the-web.md)
- <i class="far fa-exclamation"></i> [Introduction to HTML](project/curriculum/materials/tutorials/introduction-to-html.md)
- <i class="far fa-exclamation"></i> [Pip and VirtualEnv](project/curriculum/materials/pages/python/pip-and-virtualenv.md)
- <i class="far fa-exclamation"></i> [A web-framework for Python: Flask](project/curriculum/materials/pages/python/python-flask.md)
- <i class="far fa-book-open"></i> [Flask documentation](http://flask.palletsprojects.com/) (the Quickstart gives a good overview)
- <i class="far fa-book-open"></i> [Jinja2 documentation](https://jinja.palletsprojects.com/en/2.10.x/templates/)
- <i class="far fa-book-open"></i> [HTML tutorials and references on MDN](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [Tips & Tricks](project/curriculum/materials/pages/web/web-with-python-tips.md)
- [About unique identifiers](project/curriculum/materials/pages/general/unique-id.md)
