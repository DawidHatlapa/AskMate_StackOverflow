from flask import Flask, render_template, url_for, redirect, request, session
import data_manager, util, connection, os
from settings import *
from flask_paginate import Pagination, get_page_args
from os import urandom
import bcrypt


app = Flask(__name__)
app.secret_key = urandom(16)

class server_state:

    #SORTING
    actual_sort_column = question.submission_time
    actual_sort_direction = sort.descending

    def toogle_sort_direction():
        if server_state.actual_sort_direction == sort.ascending:
            server_state.actual_sort_direction = sort.descending
        else:
            server_state.actual_sort_direction = sort.ascending

    #FILTERING
    default_filter_by_date = filter.date_all_time
    default_filter_by_status = filter.status_all
    default_filter_by_search = filter.search_empty

    actual_advanced_filter_on_date = state.off
    actual_advanced_filter_on_status = state.off
    actual_filter_reset_button_active = state.off
    filter_reset_active = state.off

    #default values for starting page
    actual_filter_by_date_mode = default_filter_by_date
    actual_filter_by_status_mode = default_filter_by_status
    actual_filter_by_search_mode = default_filter_by_search

    #TAGS (filtering)
    actual_tag = tag.all_tags


    def toogle_advanced_filter_date():
        if server_state.actual_advanced_filter_on_date == state.off:
            server_state.actual_advanced_filter_on_date = state.on
        else:
            server_state.actual_advanced_filter_on_date = state.off

    def toogle_advanced_filter_status():
        if server_state.actual_advanced_filter_on_status == state.off:
            server_state.actual_advanced_filter_on_status = state.on
        else:
            server_state.actual_advanced_filter_on_status = state.off

    #FOR USER's PAGE
    is_enabled_user_activity_lists = user_page.is_enabled_user_activity_lists_default
    actual_user_activity_list = user_page.user_activity_list_default

    def toogle_user_activity_list():
        if server_state.is_enabled_user_activity_lists == state.off:
            server_state.is_enabled_user_activity_lists = state.on
        else:
            server_state.is_enabled_user_activity_lists = state.off

@app.route('/', methods=["GET"])
def index():
    headers = data_manager.get_headers_from_table_for_main_page()

    # FILTERS AND SORTING
    actual_filters=[server_state.actual_filter_by_date_mode, \
                    server_state.actual_filter_by_status_mode, \
                    server_state.actual_filter_by_search_mode]
    sorting_mode = [server_state.actual_sort_column, \
                    server_state.actual_sort_direction]

    # TAGS CLOUD
    tags_cloud = data_manager.list_tags_with_counts()

    #PAGINATION
    page, per_page, offset = get_page_args(page_parameter='page',\
                                           per_page_parameter='per_page')
    per_page=4
    offset = (page - 1) * per_page

    total_result_question = data_manager.get_list_questions(actual_filters, \
                                                sorting_mode, \
                                                server_state.actual_tag,\
                                                offset=0,\
                                                per_page=0,\
                                                just_count_result_number=True)

    count_number_index = 0
    total_result_question = total_result_question[count_number_index]['count']

    paginations_questions = data_manager.get_list_questions(actual_filters, \
                                                sorting_mode, \
                                                server_state.actual_tag,\
                                                offset=offset,\
                                                per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, \
                            total=total_result_question, \
                            css_framework='bootstrap4')

    return render_template("index.html", headers=headers, \
                           questions=paginations_questions, \
                           server_state=server_state, \
                           tags_cloud=tags_cloud,\
                           page=page,\
                           per_page=per_page,
                           pagination=pagination)

@app.route('/', methods=["POST"])
def index_post():

    # FILTERING FEATURE
    if request.form.get("actual_advanced_filter_date_clicked") == "clicked":
        server_state.toogle_advanced_filter_date()
        if server_state.actual_advanced_filter_on_status == state.on:
            server_state.toogle_advanced_filter_status()

    if request.form.get("actual_advanced_filter_status_clicked") == "clicked":
        server_state.toogle_advanced_filter_status()
        if server_state.actual_advanced_filter_on_date == state.on:
            server_state.toogle_advanced_filter_date()

    if request.form.get("date_filter_changed") == "true":
        server_state.actual_filter_by_date_mode = request.form.get("date_filter")
        server_state.toogle_advanced_filter_date()

    if request.form.get("status_filter_changed") == "true":
        server_state.actual_filter_by_status_mode = request.form.get("status_filter")
        server_state.toogle_advanced_filter_status()

    if request.form.get("filter_reset_button_clicked") == "clicked":
            server_state.actual_filter_by_date_mode = server_state.default_filter_by_date
            server_state.actual_filter_by_status_mode = server_state.default_filter_by_status
            server_state.actual_filter_by_search_mode = server_state.default_filter_by_search
            server_state.filter_reset_active = state.off

    if not (server_state.actual_filter_by_date_mode == server_state.default_filter_by_date and \
        server_state.actual_filter_by_status_mode == server_state.default_filter_by_status and \
        server_state.actual_filter_by_search_mode == server_state.default_filter_by_search):
            server_state.filter_reset_active = state.on

    if request.form.get("filter_search_clicked") == "yes":
        server_state.actual_filter_by_search_mode = request.form.get("searched_text")
        server_state.filter_reset_active = state.on

    return redirect(url_for("index"))

@app.route("/select_tag")
def select_tag():
    selected_tag = request.args.get('selected_tag')
    server_state.actual_tag = selected_tag
    return redirect(url_for("index"))

@app.route("/sort")
def sort_questions():
    ## SORTING FEATURE

    sort_question_column = request.args.get('sort_question_column')
    if sort_question_column:
        server_state.actual_sort_column = sort_question_column

    if sort_question_column  == server_state.actual_sort_column:
        server_state.toogle_sort_direction()
    else:
        server_state.actual_sort_direction = sort.ascending

    return redirect(url_for("index"))


@app.route("/vote", methods=["POST"])
def vote():
    question_id = request.form.get("question_id")
    vote_type = request.form.get("vote") # vote_up or vote_down
    vote_for_answer_or_question = request.form.get("vote_for_answer_or_question") # vote_for_answer or vote_for_question

    if vote_for_answer_or_question == "vote_for_question":
        if vote_type == "up_vote":
            data_manager.vote_for_question(question_id=question_id, vote_up_or_down="up")
            data_manager.update_reputation("question", "user_question", "question_id", question_id, 5, "+")
        else:
            data_manager.vote_for_question(question_id=question_id, vote_up_or_down="down")
            data_manager.update_reputation("question", "user_question", "question_id", question_id, 2, "-")
        return redirect(url_for("display_a_question", question_id = question_id))

    else: # vote_for_answer
        answer_id = request.form.get("answer_id")
        if vote_type == "up_vote":
            data_manager.vote_for_answer(answer_id=answer_id, vote_up_or_down="up")
            data_manager.update_reputation("answer", "user_answer", "answer_id", answer_id, 10, "+")
        else:
            data_manager.vote_for_answer(answer_id=answer_id, vote_up_or_down="down")
            data_manager.update_reputation("answer", "user_answer", "answer_id", answer_id, 2, "-")
        return redirect(url_for("display_a_question", question_id = question_id))



@app.route("/question/<question_id>")
def display_a_question(question_id):
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    answers = data_manager.get_nonquestion_by_question_id(question_id, ANSWER_TABLE_NAME)
    comments = data_manager.get_all_comments()
    question["view_number"] += 1
    data_manager.update_question(question, question_id)
    tags = data_manager.get_nonquestion_by_question_id(question_id, QUESTION_TAG_TABLE_NAME)
    user_id = util.users_id(session)
    username = util.take_out_of_the_list(data_manager.get_username_by_id(user_id))["username"] if user_id else False

    question_tags = [util.take_out_of_the_list(data_manager.get_tag_by_id(tag["tag_id"]))
                     for tag in tags]

    return render_template("display_question.html", question=question, answers=answers, comments=comments,
                           question_tags=question_tags, img_path=util.IMAGE_PATH, user_id=user_id, username=username) #img_path=connection.IMAGE_PATH)


@app.route("/change-question-status", methods=["POST"])
def change_question_status():
    new_question_status = request.form.get("new_question_status")
    question_id = request.form.get("question_id")

    if new_question_status == "close":
        data_manager.change_question_status(question_id,"close")
    elif new_question_status == "open":
        data_manager.change_question_status(question_id,"open")
    return redirect(url_for("index"))


@app.route("/add-question", methods=["GET"])
def add_question_get():
    if SESSION_KEY not in session:
        message = "PLease, log in to ask a question."
        return render_template("login_register.html", login_or_register="login", message=message, email=FORM_EMAIL,
                               pswrd=FORM_PASSWORD)
    else:
        list_of_tags = data_manager.get_tags_names()
        return render_template("add-question.html", tags_list=list_of_tags)


@app.route("/add-question", methods=["POST"])
def add_question_post():
    question = dict(request.form)
    question["submission_time"] = util.current_datetime()
    file_name = request.files["image"].filename
    if file_name != "":
        image_file = request.files["image"]
        util.add_image(image_file)
        question["image"] = image_file.filename
    return_value = data_manager.add_question(question)
    util.add_question_tag_to_db(return_value["id"], question)
    user_id = session[SESSION_KEY]
    data_manager.bind_user_with_question(user_id, question_id=return_value["id"])

    user_id = session[SESSION_KEY]
    data_manager.change_count_question(user_id, "+")

    return redirect(url_for("display_a_question", question_id=return_value["id"]))


@app.route("/question/<question_id>/new_answer", methods=["GET"])
def post_an_answer_get(question_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
        return render_template("add-question.html", question_id=question_id, question=question)


@app.route("/question/<question_id>/new_answer", methods=["POST"])
def post_an_answer_post(question_id):
    new_answer = dict(request.form)
    new_answer["submission_time"] = util.current_datetime()
    new_answer["image"] = request.files["image"].filename

    if "image" in request.files and request.files["image"].filename != '':
        image_file = request.files["image"]
        util.add_image(image_file)

    return_value = data_manager.add_answer(new_answer)
    if return_value != None:
        question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
        question["answers_number"] = int(question["answers_number"]) + 1

    if question["status"] != "discussed":
        question["status"] = "discussed"
    data_manager.update_question(question, question_id)

    user_id = session[SESSION_KEY]
    data_manager.change_count_answer(user_id, "+")
    data_manager.bind_user_with_answer(user_id=user_id, answer_id=return_value["id"])

    return redirect(url_for("display_a_question", question_id=question_id))


@app.route("/answer/<answer_id>/delete endpoint")
def delete_answer(answer_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
        question_id = answer["question_id"]
        # delete image from answer
        util.delete_image(answer["image"])

        # get comments by answer_id and delete binding comments with user
        comments = data_manager.get_comment_by_answer_id(answer_id)
        for comment in comments:
            data_manager.delete_binding_to_user(comment["id"], "user_comment", "comment_id")
        # delete comments to answer  and binding answer with user
        data_manager.delete_comments_by_answer_id(answer_id)
        data_manager.delete_binding_to_user(answer_id, "user_answer", "answer_id")
        # delete answer
        data_manager.delete_answer(answer_id)

        # change answers number and status question
        question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
        question["answers_number"] -= 1
        if question["answers_number"] == 0:
            question["status"] = "new"
        data_manager.update_question(question, question_id)

        # change count answer bind to user
        user_id = session[SESSION_KEY]
        data_manager.change_count_answer(user_id, "-")

        return redirect(url_for("display_a_question", question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        # delete bind tag with question id
        data_manager.del_question_tag(question_id)

        # delete answer, comments to answer and bind answer to user and bind comment-answer to user
        answers = data_manager.get_nonquestion_by_question_id(question_id, "answer")
        for answer in answers:
            comments = data_manager.get_comment_by_answer_id(answer["id"])
            for comment in comments:
                data_manager.delete_binding_to_user(comment["id"], "user_comment", "comment_id")
            data_manager.delete_comments_by_answer_id(answer["id"])
            data_manager.delete_binding_to_user(answer["id"], "user_answer", "answer_id")
        data_manager.delete_answers_by_question_id(question_id)

        # delete comments to question and bind comment-question to user
        comments_to_question = data_manager.get_nonquestion_by_question_id(question_id, "comment")
        for comment_question in comments_to_question:
            data_manager.delete_binding_to_user(comment_question["id"], "user_comment", "comment_id")
        data_manager.delete_comments_by_question_id(question_id)

        # delete bind question to user and delete question
        data_manager.delete_binding_to_user(question_id, "user_question", "question_id")
        data_manager.delete_question(question_id)

        user_id = session[SESSION_KEY]
        data_manager.change_count_question(user_id, "-")

        return redirect(url_for("index"))


@app.route("/question/<question_id>/edit", methods=["GET"])
def edit_question_get(question_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
        question_tags = util.question_tags_names(question_id)
        all_tags = data_manager.get_tags_names()
        return render_template("edit.html", question_id=question_id, question=question, tags_list=all_tags,
                           tags_selected=question_tags)

@app.route("/question/<question_id>/edit", methods=["POST"])
def edit_question_post(question_id):
    data_from_form = dict(request.form)
    question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
    if "image" in request.files and request.files["image"].filename != '':
        if question["image"] == "":
            image_file = request.files["image"]
            util.add_image(image_file)
            question["image"] = image_file.filename
        elif request.files["image"].filename != question["image"]:
            image_file = request.files["image"]
            util.add_image(image_file)
            util.delete_image(question["image"])
            question["image"] = image_file.filename

    question["title"] = data_from_form["title"]
    question["message"] = data_from_form["message"]
    data_manager.update_question(question, question["id"])
    util.update_question_tags(question_id, data_from_form)
    return redirect(url_for("display_a_question", question_id=question["id"]))


@app.route("/question/<question_id>/remove_image")
def delete_image_from_question(question_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
        util.delete_image(question["image"])
        question["image"] = ""
        data_manager.update_question(question, question_id)
        return redirect(url_for("display_a_question", question_id=question_id))

@app.route("/<answer_id>/delete-img")
def delete_answer_img(answer_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
        util.delete_image(answer["image"])
        data_manager.del_answer_img_from_db(answer["id"])
        return redirect(url_for('display_a_question', question_id=answer['question_id']))

@app.route("/edit/<answer_id>")
def edit_answer_get(answer_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
        img_path = os.path.join(util.IMAGE_PATH, answer["image"])
        return render_template('edit.html', answer_id=answer_id, answer=answer, img_path=img_path)

@app.route("/edit/<answer_id>", methods=["POST"])
def edit_answer_post(answer_id):
    data_from_form = dict(request.form)
    current_answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    current_answer["message"] = data_from_form["message"]

    if "image" in request.files and request.files["image"].filename != '':
        util.delete_image(current_answer["image"])
        current_answer["image"] = request.files["image"].filename
        util.add_image(request.files["image"])

    data_manager.update_answer(answer_id, current_answer["message"], current_answer["image"])
    return redirect(url_for('display_a_question', question_id=current_answer['question_id']))

@app.route("/question/<question_id>/new-comment", methods=["GET"])
def add_comment_to_question_get(question_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        question = util.take_out_of_the_list(data_manager.get_question_by_id(question_id))
        return render_template("add-comment.html", question=question, mode="question")


@app.route("/question/<question_id>/new-comment", methods=["POST"])
def add_comment_to_question_post(question_id):
        comment = dict(request.form)
        comment["submission_time"] = util.current_datetime()
        comment_id = util.take_out_of_the_list(data_manager.add_comment_to_question(comment))["id"]
        user_id = session[SESSION_KEY]
        data_manager.bind_user_with_comment(user_id, comment_id)

        data_manager.change_count_comment(user_id, "+")

        return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/answer/<answer_id>/new-comment')
def add_comment_to_answer_get(answer_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
        question = util.take_out_of_the_list(data_manager.get_question_by_id(answer["question_id"]))
        return render_template("add-comment.html", answer=answer, question=question, mode="answer")


@app.route('/answer/<answer_id>/new-comment', methods=["POST"])
def add_comment_to_answer_post(answer_id):
    comment = dict(request.form)
    comment["submission_time"] = util.current_datetime()
    # data_manager.add_comment_to_answer(comment)
    # answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    # return redirect(url_for("display_a_question", question_id=answer["question_id"]))

    comment_id = util.take_out_of_the_list(data_manager.add_comment_to_answer(comment))["id"]
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    user_id = session[SESSION_KEY]
    data_manager.bind_user_with_comment(user_id, comment_id)
    data_manager.change_count_comment(user_id, "+")
    return redirect(url_for("display_a_question", question_id=answer["question_id"]))


@app.route('/comment/<comment_id>/edit', methods=["GET"])
def edit_comment_get(comment_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        comment = util.take_out_of_the_list(data_manager.get_comment_by_comment_id(comment_id))
        answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(comment["answer_id"])) if comment["question_id"] is None else None
        return render_template("edit_comment.html", comment=comment, answer=answer)


@app.route('/comment/<comment_id>/edit', methods=["POST"])
def edit_comment_post(comment_id):
    data_from_form = dict(request.form)
    current_comment = util.take_out_of_the_list(data_manager.get_comment_by_comment_id(comment_id))
    current_comment["message"] = data_from_form["message"]
    current_comment["submission_time"] = util.current_datetime()
    if current_comment["edited_count"] is not None:
        current_comment["edited_count"] = current_comment["edited_count"] + 1
    else:
        current_comment["edited_count"] = 1
    data_manager.update_comment(current_comment)
    if current_comment["question_id"] is not None:
        question_id = current_comment["question_id"]
    else:
        answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(current_comment["answer_id"]))
        question_id = answer["question_id"]
    return redirect(url_for("display_a_question", question_id=question_id))


@app.route('/comments/<comment_id>/delete')
def delete_comment(comment_id):
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        comment = util.take_out_of_the_list(data_manager.get_comment_by_comment_id(comment_id))
        if comment["question_id"] is not None:
            question_id = comment["question_id"]
        else:
            answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(comment["answer_id"]))
            question_id = answer["question_id"]


    data_manager.delete_comment(comment_id)
    user_id = session[SESSION_KEY]
    data_manager.change_count_comment(user_id, "-")
    return redirect(url_for("display_a_question", question_id=question_id))




@app.route("/login")
def login_get():
    return render_template("login_register.html", login_or_register="login", email=FORM_EMAIL, pswrd=FORM_PASSWORD)


@app.route("/login", methods=["POST"])
def login_post():
    login = request.form.get(FORM_EMAIL)
    password = request.form.get(FORM_PASSWORD).encode("utf-8")
    data_from_db = data_manager.get_id_login_password(login)

    if data_from_db != [] and bcrypt.checkpw(password, data_from_db[0].get(FORM_PASSWORD).encode('utf-8')):
        session[SESSION_KEY] = data_from_db[0][DB_USER_ID]
        return redirect(url_for("index"))
    else:
        message = "Incorrect login or password"
        return render_template("login_register.html", login_or_register="login", message=message, email=FORM_EMAIL,
                               pswrd=FORM_PASSWORD)

@app.route("/register")
def register_get():
    return render_template("login_register.html", login_or_register="register", username=FORM_USERNAME, email=FORM_EMAIL,
                           pswrd=FORM_PASSWORD, confirm_pswrd=FORM_CONFIRM_PSWRD)

@app.route("/register", methods=["POST"])
def register_post():
    login = request.form.get(FORM_EMAIL)
    password = request.form.get(FORM_PASSWORD)
    confirm_pswrd = request.form.get(FORM_CONFIRM_PSWRD)
    user_name = request.form.get(FORM_USERNAME)
    user_db_data = data_manager.get_id_username_login_password(login, user_name)

    if password != confirm_pswrd:
        message = "Passwords provided do not match. Try again."
    elif user_db_data != []:
        message = "Username or email already occupied"
    else:
        current_date = util.current_datetime()
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(16))
        reputation = 0
        count_questions = 0
        count_answers = 0
        count_comments = 0
        data_manager.add_to_table(user_name, login, password.decode('utf-8'), current_date, reputation, count_questions, count_answers, count_comments)
        message = "Account created successfully"

    return render_template("login_register.html", login_or_register="register", username=FORM_USERNAME, email=FORM_EMAIL,
                           pswrd=FORM_PASSWORD, confirm_pswrd=FORM_CONFIRM_PSWRD, message=message)


@app.route('/logout')
def logout():
    try:
        session.pop(SESSION_KEY)
        message = "You've been logged out successfully."
    except:
        message = "You are not logged in"

    return render_template("login_register.html", login_or_register="register", username=FORM_USERNAME, email=FORM_EMAIL,
                    pswrd=FORM_PASSWORD, confirm_pswrd=FORM_CONFIRM_PSWRD, message=message)

@app.route("/login-google", methods=["GET"])
def login_google():
    pass

@app.route("/login-google", methods=["POST"])
def login_google_post():
    return ("<h1>google login</h1>")


@app.route("/users-page")
def list_users():
    if SESSION_KEY not in session:
        return redirect(url_for("login_get"))
    else:
        headers = ["username", "join_date", "count_questions", "count_answers", "count_comments", "reputation"]
        users = data_manager.get_users()

        return render_template("users-page.html", headers=headers, users=users)


@app.route("/user_page", methods=["GET"])
def user_page():
   # if SESSION_KEY in session:
    user_id = session[SESSION_KEY]
    query_result_0 = 0
    user_info = data_manager.get_user_profil_info(user_id)[query_result_0]

    list_of_user_activity = []
    if server_state.actual_user_activity_list == "answer" \
        and server_state.is_enabled_user_activity_lists == "yes":
        list_of_user_activity = data_manager.get_user_answers(user_id)
    elif server_state.actual_user_activity_list == "question" \
        and server_state.is_enabled_user_activity_lists == "yes":
        list_of_user_activity = data_manager.get_user_questions(user_id)
    elif server_state.actual_user_activity_list == "comment" \
        and server_state.is_enabled_user_activity_lists == "yes":
        list_of_user_activity = data_manager.get_user_comments(user_id)

    return render_template("user_page.html",user_info=user_info, \
                           server_state=server_state,\
                           list_of_user_activity=list_of_user_activity)

@app.route("/user_page", methods=["POST"])
def user_page_post():
    chosen_user_activity_list = request.form.get("chosen_user_activity_list")
    toogle_user_activity_list = request.form.get("toogle_user_activity_list")
    if toogle_user_activity_list == "yes":
        server_state.toogle_user_activity_list()

    if chosen_user_activity_list in ["comment", "answer", "question"]:
        server_state.actual_user_activity_list = chosen_user_activity_list

    return redirect(url_for("user_page"))

@app.route("/answer/<answer_id>/accepted")
def accepted_answer(answer_id):
    answer = util.take_out_of_the_list(data_manager.get_answer_by_answer_id(answer_id))
    accepted = "TRUE"
    data_manager.update_accepted_status(accepted, answer_id)
    data_manager.update_reputation("answer", "user_answer", "answer_id", answer_id, 15, "+")
    return redirect(url_for("display_a_question", question_id=answer["question_id"]))



if __name__ == "__main__":
    app.run()

