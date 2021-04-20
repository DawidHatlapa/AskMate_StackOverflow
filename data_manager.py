from typing import List, Dict

from psycopg2 import sql
from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
from settings import *

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import connection


@connection.connection_handler
def get_tags_names(cursor: RealDictCursor) -> list:
    query = """
            SELECT name
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_question_by_id(cursor: RealDictCursor, question_id: int) -> list:
    # query = f"""
    #         SELECT *
    #         FROM question
    #         WHERE id = %(question_id)s"""
    # param = {"question_id": f"{question_id}"}
    # cursor.execute(query, param)

    query = """
    WITH question_1 AS (
        SELECT uq.user_id, q. *
        FROM question q 
        LEFT JOIN user_question uq on q.id = uq.question_id
        WHERE q.id = %(question_id)s
    )
    SELECT u.username, u.email, *
    FROM question_1
    LEFT JOIN users u on u.user_id = question_1.user_id
    """

    cursor.execute(query, {'question_id': f"{question_id}"})
    return cursor.fetchall()

@connection.connection_handler
def get_nonquestion_by_question_id(cursor: RealDictCursor, question_id, table_name: str) -> list:
    if table_name == ANSWER_TABLE_NAME:
        # f"SELECT * \
        #                 FROM {table_name} \
        #                 WHERE question_id = {question_id} \""
        query = """
        WITH answer_1 AS (
            SELECT ua.user_id, a.*
            FROM answer a 
            LEFT JOIN user_answer ua on a.id = ua.answer_id
            WHERE a.question_id = %(question_id)s
        )
        SELECT u.username, u.email, a.*
        FROM answer_1 a
        LEFT JOIN users u on u.user_id = a.user_id
        ORDER BY a.vote_number DESC 
        """

        cursor.execute(query,{'question_id': f"{question_id}"})
        return cursor.fetchall()

    elif table_name == COMMENTS_TABLE_NAME:
        query = f"SELECT * \
                FROM {table_name}\
                WHERE question_id = {question_id} \
                ORDER BY submission_time DESC \
                "
        cursor.execute(query)
        return cursor.fetchall()

    else:
        query = f"SELECT * \
                FROM {table_name}\
                WHERE question_id = {question_id} \
                "
        cursor.execute(query)
        return cursor.fetchall()



    # f"SELECT * \
    #                 FROM {table_name} \
    #                 WHERE question_id = {question_id} \""
    query = """
    WITH question_1 AS (
        SELECT uq.user_id, q. *
        FROM question q 
        LEFT JOIN user_question uq on q.id = uq.question_id
        WHERE q.id = %(question_id)s
    )
    SELECT u.username, u.email, *
    FROM question_1
    LEFT JOIN users u on u.user_id = question_1.user_id
    """

    cursor.execute(query, {'question_id': f"{question_id}"})
    return cursor.fetchall()


@connection.connection_handler
def get_tag_by_id(cursor: RealDictCursor, tag_id: int) -> list:
    query = """
            SELECT name
            FROM tag
            WHERE id = %(tag_id)s"""
    param = {"tag_id": tag_id}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor: RealDictCursor, question):
    command = """
            INSERT INTO question(submission_time, view_number, vote_number, title, message, image, status, answers_number) 
            VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s, %(status)s, %(answers_number)s)
            RETURNING id
            """

    param = {"submission_time": question.get("submission_time"),
             "view_number": question.get("view_number"),
             "vote_number": question.get("vote_number"),
             "title": question.get("title"),
             "message": question.get("message"),
             "image": question.get("image"),
             "status": question.get("status"),
             "answers_number": question.get("answers_number")}
    cursor.execute(command, param)
    return cursor.fetchone()


@connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int):
    command = """
            DELETE
            FROM question
            WHERE id = %(question_id)s
    """

    param = {"question_id": question_id}
    cursor.execute(command, param)


@connection.connection_handler
def delete_answers_by_question_id(cursor: RealDictCursor, question_id: int):
    command = """
            DELETE
            FROM answer
            WHERE question_id = %(question_id)s
    """
    param = {"question_id": question_id}

    cursor.execute(command, param)

@connection.connection_handler
def get_headers_from_table_for_main_page(cursor: RealDictCursor) -> list:
    query = f"\
            SELECT column_name \
            FROM information_schema.columns \
            WHERE table_name = '{QUESTION_TABLE_NAME}' or table_name = '{QUESTION_TAG_TABLE_NAME}'  \
            AND column_name IN ('{question.vote_number}',\
                                '{question.view_number}',\
                                '{question.answers_number}',\
                                '{question.title}',\
                                '{question.status}',\
                                '{question.submission_time}',\
                                '{question.id}',\
                                '{question.message}',\
                                '{question.image}',\
                                'tag_id')\
            "

    cursor.execute(query)
    headers = cursor.fetchall()

    # set proper columns order for listing questions on index.html page
    column = {question.vote_number:3, question.view_number:2, question.answers_number:8, question.title:4, question.status:7, question.submission_time:1, question.id:0, question.message:5, question.image:6, 'tag_id':9}
    new_headers = [\
            headers[column[question.vote_number]],\
                      headers[column[question.view_number]],\
                      headers[column[question.answers_number]],\
                      headers[column[question.title]],\
                      headers[column[question.status]],\
                      headers[column[question.submission_time]],\
                      headers[column['tag_id']],\
                      headers[column[question.id]],\
                      headers[column[question.message]],\
                      headers[column[question.image]]\
                      ]
    return new_headers

@connection.connection_handler
def get_list_questions(cursor: RealDictCursor, actual_filters:list, sorting_mode:list, selected_tag: str,\
                       offset :int = 0, per_page : int = 10, just_count_result_number : bool = False) -> list:

    #FILTERING
    actual_filter_by_date_mode = actual_filters[0]
    actual_filter_by_status_mode = actual_filters[1]
    actual_filter_by_search_mode = actual_filters[2]

    query_part_by_date = ""
    if actual_filter_by_date_mode == filter.date_last_month:
        query_part_by_date = (datetime.now() + relativedelta(months=-1)).strftime("%Y-%m-%d")
    elif actual_filter_by_date_mode == filter.date_3_last_months:
        query_part_by_date = (datetime.now() + relativedelta(months=-3)).strftime("%Y-%m-%d")
    elif actual_filter_by_date_mode == filter.date_all_time:
        query_part_by_date = filter.date_starting_point_for_all_time_question

    query_part_by_status = ""
    if actual_filter_by_status_mode == filter.status_new:
        query_part_by_status = "status = 'new'"
    elif actual_filter_by_status_mode == filter.status_discussed:
        query_part_by_status = "status = 'discussed'"
    elif actual_filter_by_status_mode == filter.status_active:
        query_part_by_status = "status IN ('new', 'discussed')"
    elif actual_filter_by_status_mode == filter.status_closed:
        query_part_by_status = "status = 'closed'"
    elif actual_filter_by_status_mode == filter.status_all:
        query_part_by_status = "status IN ('new', 'discussed', 'closed')"

    # FILTERING BY TAGS
    query_part_by_tag = ""
    if selected_tag == tag.all_tags:
        query_part_by_tag


    #SORTING
    sorting_column = sorting_mode[0]
    sorting_direction = "DESC" if sorting_mode[1] == sort.descending else "ASC"

    #PAGINATION
    per_page = 'ALL' if per_page == 0 else per_page

    if selected_tag == tag.all_tags:
        if just_count_result_number == False:

            full_query = f" \
                        WITH listed_questions AS \
                        (\
                            SELECT q.vote_number, q.view_number, q.answers_number, q.title, q.status, \
                            q.submission_time,  tag.name,  q.id, q.message, q.image \
                            FROM question_tag \
                            RIGHT JOIN question q on q.id = question_tag.question_id \
                            LEFT JOIN tag on question_tag.tag_id = tag.id \
                            WHERE  submission_time >= '{query_part_by_date}' \
                            AND {query_part_by_status} \
                            AND (title LIKE '%%{actual_filter_by_search_mode}%%'\
                                OR message LIKE '%%{actual_filter_by_search_mode}%%') \
                            \
                        )\
                        SELECT l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                        l.submission_time, string_agg(l.name, ', ') as tags_names, l.id, l.message, l.image\
                        FROM listed_questions l \
                        GROUP BY l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                        l.submission_time, l.id, l.message, l.image\
                        ORDER BY l.{sorting_column} {sorting_direction}\
                        LIMIT {per_page} OFFSET {offset} \
                "
        else: #just count results number (without tags)

            full_query = f" \
                        WITH listed_questions AS \
                        (\
                            SELECT q.vote_number, q.view_number, q.answers_number, q.title, q.status, \
                            q.submission_time,  tag.name,  q.id, q.message, q.image \
                            FROM question_tag \
                            RIGHT JOIN question q on q.id = question_tag.question_id \
                            LEFT JOIN tag on question_tag.tag_id = tag.id \
                            WHERE  submission_time >= '{query_part_by_date}' \
                            AND {query_part_by_status} \
                            AND (title LIKE '%%{actual_filter_by_search_mode}%%'\
                                OR message LIKE '%%{actual_filter_by_search_mode}%%') \
                            \
                        ),\
                        results_questions_without_tags AS \
                        (\
                            SELECT l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                            l.submission_time, string_agg(l.name, ', ') as tags_names, l.id, l.message, l.image\
                            FROM listed_questions l \
                            GROUP BY l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                            l.submission_time, l.id, l.message, l.image\
                            ORDER BY l.{sorting_column} {sorting_direction}\
                        )\
                        SELECT COUNT(*) AS count FROM results_questions_without_tags\
                "


    else: # for query with tags

        if just_count_result_number == False:
            full_query = f" \
                        WITH listed_questions AS \
                        (\
                            SELECT q.vote_number, q.view_number, q.answers_number, q.title, q.status, \
                            q.submission_time,  tag.name,  q.id, q.message, q.image \
                            FROM question_tag \
                            RIGHT JOIN question q on q.id = question_tag.question_id \
                            LEFT JOIN tag on question_tag.tag_id = tag.id \
                            WHERE  submission_time >= '{query_part_by_date}' \
                            AND {query_part_by_status} \
                            AND (title LIKE '%%{actual_filter_by_search_mode}%%'\
                                OR message LIKE '%%{actual_filter_by_search_mode}%%') \
                        ),\
                        questions_before_tag_filtering AS \
                        (\
                            SELECT l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                            l.submission_time,  string_agg(l.name, ', ') as tags_names , l.id, l.message, l.image\
                            FROM listed_questions l \
                            GROUP BY l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                            l.submission_time, l.id, l.message, l.image\
                        )\
                        SELECT qq.* FROM questions_before_tag_filtering qq WHERE  qq.tags_names LIKE '%%{selected_tag}%%' \
                        ORDER BY qq.{sorting_column} {sorting_direction}\
                        LIMIT {per_page} OFFSET {offset} \
                "
        else: #just count results number
            full_query = f" \
                        WITH listed_questions AS \
                        (\
                            SELECT q.vote_number, q.view_number, q.answers_number, q.title, q.status, \
                            q.submission_time,  tag.name,  q.id, q.message, q.image \
                            FROM question_tag \
                            RIGHT JOIN question q on q.id = question_tag.question_id \
                            LEFT JOIN tag on question_tag.tag_id = tag.id \
                            WHERE  submission_time >= '{query_part_by_date}' \
                            AND {query_part_by_status} \
                            AND (title LIKE '%%{actual_filter_by_search_mode}%%'\
                                OR message LIKE '%%{actual_filter_by_search_mode}%%') \
                        ),\
                        questions_before_tag_filtering AS \
                        (\
                            SELECT l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                            l.submission_time,  string_agg(l.name, ', ') as tags_names , l.id, l.message, l.image\
                            FROM listed_questions l \
                            GROUP BY l.vote_number, l.view_number, l.answers_number, l.title, l.status, \
                            l.submission_time, l.id, l.message, l.image\
                        ),\
                        results_questions_with_tags AS \
                        (\
                            SELECT qq.* FROM questions_before_tag_filtering qq WHERE  qq.tags_names LIKE '%%{selected_tag}%%' \
                            ORDER BY qq.{sorting_column} {sorting_direction}\
                        )\
                        SELECT count(*) AS count FROM results_questions_with_tags \
                "



    param = {\
        "sorting_column" : sorting_column,\
        "sorting_direction" : f"{sorting_direction}"\
    }
    cursor.execute(full_query, param)
    questions = cursor.fetchall()
    return questions


# @connection.connection_handler
# def get_id(cursor: RealDictCursor, name_table):
#     query = """
#         SELECT CURRVAL(pg_get_serial_sequence('sheet_tbl','sheet_id'))";
#     """

@connection.connection_handler
def get_answer_by_answer_id(cursor: RealDictCursor, answer_id: int) -> dict:
    query = """
            SELECT *
            FROM answer
            WHERE id = %(answer_id)s"""
    param = {"answer_id": f"{answer_id}"}
    cursor.execute(query, param)
    result = cursor.fetchall()
    return result

@connection.connection_handler
def vote_for_question(cursor: RealDictCursor, question_id: int, vote_up_or_down="up") -> None:
    operant = '+' if vote_up_or_down == "up" else '-'
    query = f"UPDATE question \
    SET vote_number = vote_number {operant} 1 \
    WHERE id = {question_id}"
    cursor.execute(query)


@connection.connection_handler
def change_question_status(cursor: RealDictCursor, question_id: int, open_or_close="open") -> None:
    query_for_number_of_answers = f"SELECT answers_number FROM question WHERE id = '{question_id}'"
    cursor.execute(query_for_number_of_answers)
    answers_number = cursor.fetchall()
    answers_number = answers_number[0]['answers_number']
    new_status = "new" if answers_number == 0 else "discussed"

    if open_or_close == "open":
        query = f"UPDATE question \
        SET status = '{new_status}' \
                WHERE id = {question_id}"
        cursor.execute(query)
    else:
        query = f"UPDATE question \
        SET status = 'closed'\
                WHERE id = {question_id}"
        cursor.execute(query)


@connection.connection_handler
def vote_for_answer(cursor: RealDictCursor, answer_id: int, vote_up_or_down="up") -> None:
    operant = '+' if vote_up_or_down == "up" else '-'
    query = f"UPDATE answer \
    SET vote_number = vote_number {operant} 1 \
    WHERE id = {answer_id}"
    cursor.execute(query)

@connection.connection_handler
def add_answer(cursor: RealDictCursor, answer: dict):
    command = """
            INSERT INTO answer(submission_time, vote_number, question_id, message, image)
            VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)
            RETURNING id
            """

    param = {
            "submission_time": answer["submission_time"],
            "vote_number": answer["vote_number"],
            "question_id": answer["question_id"],
            "message": answer["message"],
            "image": answer["image"]
            }
    cursor.execute(command, param)
    return cursor.fetchone()


@connection.connection_handler
def get_answer_image(cursor: RealDictCursor, answer_id) -> list:
    query = """
            SELECT image
            FROM answer
            WHERE id = %(answer_id)s"""
    param = {"answer_id": f"{answer_id}"}
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def update_answer(cursor: RealDictCursor, answer_id, new_message: str, new_image: str):
    command = """
            UPDATE answer
            SET message = %(new_message)s,
                image = %(new_image)s
            WHERE id = %(answer_id)s"""
    param = {
        "new_message": f"{new_message}",
        "new_image": f"{new_image}",
        "answer_id": f"{answer_id}"
    }
    cursor.execute(command, param)


@connection.connection_handler
def del_answer_img_from_db(cursor: RealDictCursor, answer_id):
    command = """
            UPDATE answer 
            SET image = %(image)s
            WHERE id = %(answer_id)s"""
    param = {"image": "",
             "answer_id": f"{answer_id}"}
    cursor.execute(command, param)


@connection.connection_handler
def delete_answer(cursor: RealDictCursor, answer_id):
    command = """
            DELETE FROM answer
            WHERE id = %(answer_id)s"""
    param = {"answer_id": f"{answer_id}"}
    cursor.execute(command, param)

@connection.connection_handler
def update_question(cursor: RealDictCursor, question, question_id):
    command = """
           UPDATE question
           SET title = %(title)s,
               message = %(message)s,
               image = %(image)s, 
               view_number = %(view_number)s,
               status = %(status)s,
               answers_number = %(answers_number)s
           WHERE id = %(question_id)s       
    """
    param = {"title": question["title"],
             "message": question["message"],
             "image": question["image"],
             "view_number": question["view_number"],
             "status": question["status"],
             "answers_number": question["answers_number"],
             "question_id": question_id
             }
    cursor.execute(command, param)


@connection.connection_handler
def add_comment_to_question(cursor: RealDictCursor, comment):
    command = """
            INSERT INTO comment(question_id, message, submission_time)
            VALUES (%(question_id)s, %(message)s, %(submission_time)s);
            SELECT id
            FROM comment
            WHERE submission_time = %(submission_time)s
            """

    param = {
        "question_id": comment["question_id"],
        "message": comment["message"],
        "submission_time": comment["submission_time"],

            }
    cursor.execute(command, param)
    return cursor.fetchall()


@connection.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, comment: dict):
    query = """
            INSERT INTO comment(answer_id, message, submission_time, edited_count)
            VALUES (%(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s);
            SELECT id
            FROM comment
            WHERE submission_time = %(submission_time)s
            """
    param = {
        "answer_id": f"{comment['answer_id']}",
        "message": f"{comment['message']}",
        "submission_time": f"{comment['submission_time']}",
        "edited_count": f"{comment['edited_count']}"
    }
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def get_all_comments(cursor: RealDictCursor) -> RealDictCursor:
    query = """
            SELECT c.id AS comment_id, c.question_id, c.answer_id, c.message, c.submission_time, c.edited_count, usrs.username
            FROM comment c
            LEFT JOIN user_comment uc
            ON c.id = uc.comment_id
            LEFT JOIN users usrs
            ON uc.user_id = usrs.user_id;
            """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_comment_by_comment_id(cursor: RealDictCursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id = %(comment_id)s
    """
    param = {
        "comment_id": comment_id
    }

    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def update_comment(cursor: RealDictCursor, comment):
    command = """
               UPDATE comment
               SET message = %(message)s,
                   submission_time = %(submission_time)s,
                   edited_count = %(edited_count)s 
               WHERE id = %(comment_id)s       
        """
    param = {"message": comment["message"],
             "submission_time": comment["submission_time"],
             "edited_count": comment["edited_count"],
             "comment_id": comment["id"]
             }
    cursor.execute(command, param)


@connection.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id):
    command = """
                DELETE FROM user_comment
                WHERE comment_id = %(comment_id)s;
                DELETE FROM comment
                WHERE id = %(comment_id)s;"""
    param = {"comment_id": f"{comment_id}"}
    cursor.execute(command, param)



@connection.connection_handler
def get_tags_with_ids(cursor: RealDictCursor) -> list:
    query = """
            SELECT *
            FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_tag(cursor: RealDictCursor, tag_name: str):
    command = """
            INSERT INTO tag("name")
            VALUES (%(tag_name)s)"""
    param = {"tag_name": f"{tag_name}"}
    cursor.execute(command, param)

@connection.connection_handler
def add_question_tag(cursor: RealDictCursor, question_id, tag_id):
    command = """
                INSERT INTO question_tag(question_id, tag_id)
                VALUES (%(question_id)s, %(tag_id)s)"""
    param = {
            "question_id": f"{question_id}",
            "tag_id": f"{tag_id}"
    }
    cursor.execute(command, param)


@connection.connection_handler
def del_question_tag(cursor: RealDictCursor, question_id):
    command = f"""
            DELETE
            FROM question_tag
            WHERE question_id = %(question_id)s"""
    param = {"question_id": f"{question_id}"}
    cursor.execute(command, param)


@connection.connection_handler
def get_user_profil_info(cursor: RealDictCursor, user_id):
    command = f"""
        SELECT u.username, u.email, u.reputation,
        u.count_questions, u.count_answers, u.count_comments
        FROM users u
        WHERE u.user_id = %(user_id)s
    """
    param = {"user_id":f"{user_id}"}
    cursor.execute(command, param)
    return cursor.fetchall()


@connection.connection_handler
def list_tags_with_counts(cursor: RealDictCursor) -> list:
    query = """SELECT  tag.name, count(*)
            FROM question_tag
            INNER JOIN tag on question_tag.tag_id = tag.id
            GROUP BY tag.name"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_id_login_password(cursor: RealDictCursor, email: str) -> list:
    cursor.execute("""
            SELECT user_id, email, password
            FROM users
            WHERE email = %(email)s;
            """,
            {"email": email})
    return cursor.fetchall()


@connection.connection_handler
def get_id_username_login_password(cursor: RealDictCursor, email: str, user_name: str) -> list:
    cursor.execute("""
            SELECT user_id, username, email, password
            FROM users
            WHERE email = %(email)s OR username = %(user_name)s;
            """,
            {"email": email, "user_name": user_name})
    return cursor.fetchall()


@connection.connection_handler
def add_to_table(cursor: RealDictCursor, user_name, email, password, date, reputation, count_questions, count_answers, count_comments):
    cursor.execute("""
        INSERT INTO users(username, password, email, join_date, reputation, count_questions, count_answers, count_comments)
        VALUES (%(user_name)s, %(password)s, %(email)s, %(date)s, %(reputation)s, %(count_questions)s, %(count_answers)s, %(count_comments)s)
        """,
        {
            "user_name": user_name,
            "email": email,
            "password": password,
            "date": date,
            "reputation": reputation,
            "count_questions": count_questions,
            "count_answers": count_answers,
            "count_comments": count_comments
            })


@connection.connection_handler
def get_users(cursor:RealDictCursor) -> list:
    query = """ SELECT username, reputation, count_questions, count_answers, count_comments, join_date
                FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_headers_to_users_list(cursor: RealDictCursor) -> list:
    query = """ SELECT column_name 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = 'users';
    """
    cursor.execute(query)
    return cursor.fetchall()

@connection.connection_handler
def bind_user_with_comment(cursor: RealDictCursor, user_id, comment_id):
    cursor.execute("""
        INSERT INTO user_comment(user_id, comment_id)
        VALUES(%(user_id)s, %(comment_id)s)
        """,
        {
            "user_id": user_id,
            "comment_id": comment_id
        })


@connection.connection_handler
def bind_user_with_question(cursor: RealDictCursor, user_id, question_id):
    cursor.execute("""
        INSERT INTO user_question(user_id, question_id)
        VALUES(%(user_id)s, %(question_id)s)
        """,
        {
            "user_id": user_id,
            "question_id": question_id
        })


@connection.connection_handler
def bind_user_with_answer(cursor: RealDictCursor, user_id, answer_id):
    cursor.execute("""
        INSERT INTO user_answer(user_id, answer_id)
        VALUES(%(user_id)s, %(answer_id)s)
        """,
        {
            "user_id": user_id,
            "answer_id": answer_id
        })


@connection.connection_handler
def get_username_by_id(cursor: RealDictCursor, user_id) -> list:
    cursor.execute("""
        SELECT username
        FROM users
        WHERE user_id = %(user_id)s;
        """,
        {"user_id": user_id})
    return cursor.fetchall()


@connection.connection_handler
def update_reputation(cursor: RealDictCursor, table_1, table_2, col_name, relevant_id, amount, operant):
    cursor.execute(f"""
        UPDATE users
        SET reputation = reputation {operant} %(amount)s
        FROM (SELECT users.username
            FROM {table_1} tab_1
            LEFT JOIN {table_2} tab_2
            ON tab_1.id = tab_2.{col_name}
            LEFT JOIN users
            ON tab_2.user_id = users.user_id
            WHERE tab_1.id = %(relevant_id)s) AS usrs
        WHERE users.username = usrs.username;""",
    {
        "relevant_id": relevant_id,
        "amount": amount
    })


@connection.connection_handler
def change_count_comment(cursor: RealDictCursor, user_id, operant):
    command = f""" UPDATE users
                  SET count_comments = count_comments {operant} 1  
                  WHERE user_id = %(user_id)s
    """
    param = {
                "user_id": user_id,
    }

    cursor.execute(command, param)


@connection.connection_handler
def change_count_question(cursor: RealDictCursor, user_id, operant):
    command = f""" UPDATE users
                  SET count_questions = count_questions {operant} 1  
                  WHERE user_id = %(user_id)s
    """
    param = {
                "user_id": user_id,
    }

    cursor.execute(command, param)


@connection.connection_handler
def change_count_answer(cursor: RealDictCursor, user_id, operant):
    command = f""" UPDATE users
                  SET count_answers = count_answers {operant} 1  
                  WHERE user_id = %(user_id)s
    """
    param = {
                "user_id": user_id,
    }

    cursor.execute(command, param)

@connection.connection_handler
def get_user_questions(cursor: RealDictCursor, user_id):
    query = f"""
        SELECT * 
        FROM user_question ua
        INNER JOIN question on ua.question_id = question.id
        WHERE ua.user_id = {user_id}
        ORDER BY question.submission_time
    """
    cursor.execute(query,{'user_id': f'{user_id}'})
    return cursor.fetchall()

@connection.connection_handler
def get_user_answers(cursor: RealDictCursor, user_id):
    query = f"""
        SELECT * 
        FROM user_answer ua
        INNER JOIN answer on ua.answer_id = answer.id
        WHERE ua.user_id = {user_id}
        ORDER BY answer.submission_time
    """
    cursor.execute(query,{'user_id': f'{user_id}'})
    return cursor.fetchall()


@connection.connection_handler
def get_user_comments(cursor: RealDictCursor, user_id):
    query = f"""
        SELECT * 
        FROM user_comment ua
        INNER JOIN comment on ua.comment_id = comment.id
        WHERE ua.user_id = {user_id}
        ORDER BY comment.submission_time
    """
    cursor.execute(query,{'user_id': f'{user_id}'})
    return cursor.fetchall()

@connection.connection_handler
def delete_comments_by_question_id(cursor: RealDictCursor, question_id):
    command = """DELETE 
                 FROM comment
                 WHERE question_id = %(question_id)s  """

    param = {"question_id": question_id}

    cursor.execute(command, param)


@connection.connection_handler
def delete_comments_by_answer_id(cursor: RealDictCursor, answer_id):
    command = """DELETE 
                 FROM comment
                 WHERE answer_id = %(answer_id)s  """

    param = {"answer_id": answer_id}


    cursor.execute(command, param)


@connection.connection_handler
def delete_binding_to_user(cursor: RealDictCursor, id, table_name, component_name):
    command = f"""DELETE
                  FROM {table_name}
                  WHERE {component_name} = {id} """
    cursor.execute(command)

@connection.connection_handler
def get_comment_by_answer_id(cursor: RealDictCursor, answer_id):
    query = """SELECT *
               FROM comment
               WHERE answer_id = %(answer_id)s"""

    param = {
        "answer_id": answer_id
    }
    cursor.execute(query, param)
    return cursor.fetchall()


@connection.connection_handler
def get_user_id_by_answer_id(cursor: RealDictCursor, answer_id):
    query = """SELECT user_id
               FROM user_answer
               WHERE answer_id = %(answer_id)s"""

    param = {
        "answer_id": answer_id
    }
    cursor.execute(query, param)
    return cursor.fetchall()

@connection.connection_handler
def update_accepted_status(cursor: RealDictCursor, accepted, answer_id):
    command = """UPDATE answer
                 SET accepted = %(accepted)s
                 WHERE id = %(answer_id)s
    """
    param = {
        "accepted": accepted,
        "answer_id": answer_id
    }
    cursor.execute(command, param)


# @connection.connection_handler
# def update_reputation(cursor: RealDictCursor, table_1, table_2, col_name, relevant_id, amount, operant):
#     cursor.execute(f"""
#         SELECT users.username
#         FROM {table_1} tab_1
#         LEFT JOIN {table_2} tab_2
#         ON tab_1.id = tab_2.{col_name}
#         LEFT JOIN users
#         ON tab_2.user_id = users.user_id
#         WHERE tab_1.id = %(relevant_id)s;""",
#     {
#         "relevant_id": relevant_id,
#         "amount": amount
#     })
#     return cursor.fetchall()