from datetime import datetime
from flask import Flask, session, abort, redirect, request, render_template, jsonify, make_response
from flask_cors import CORS
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2 import id_token
import os
import pathlib
from pip._vendor import cachecontrol
import requests
import sys
import json
from urllib.parse import urlparse

# login
from login_model.login_model import LoginDB
from login_model.connection import connect

# settings
from settings.settings import URLDuration
from settings.settings import ResetResults

# PP 0
from pp_0.pp0 import DeleteURLPP0
from pp_0.pp0 import InterpretationExamineePP0
from pp_0.pp0 import InterperationModalPP0
from pp_0.pp0 import ModelPP0
from pp_0.pp0 import question_answer
from pp_0.pp0 import RandomURLPP0
from pp_0.pp0 import ResultsPP0

# PP 1
from pp_1.pp1 import DeleteURLPP1
from pp_1.pp1 import RandomURLPP1
from pp_1.pp1 import ResultsPP1
from pp_1.pp1 import UpdateDBModelPP1

# PP 2
from pp_2.pp_2 import ResultsPP2
from pp_2.pp_2 import InstrumentPP2


sys.stdout.reconfigure(encoding='utf-8')


app = Flask(__name__, template_folder="templates")
#app.config['MIME_TYPES'] = {'js': 'application/javascript'}  # ovo proveriti
app.config['MIME_TYPES'] = {'js': 'text/javascript'}  # ovo proveriti
app.secret_key = "H8H*H88h8*h"

app.config['SESSION_COOKIE_SECURE'] = True #fixes SameSite cookie error
app.config['SESSION_COOKIE_SAMESITE'] = 'None'

CORS(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# izmena #client_secret.json izmena
GOOGLE_CLIENT_ID = "877356822205-og43795nm67cu6odsvvqku7b7t3a878s.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"  # IZMENA
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function(*args, **kwargs)

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state

    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    mail = id_info.get("email")
    LoginDB(mail).login_count()

    return redirect("/main_page")


# Google logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# renders index page
@app.route("/")
def index():
    return render_template("index.html")


# renders main page
@app.route("/main_page")
@login_is_required
def protected_area():
    return render_template("main.html")


# redirects to main page
@app.route("/main_page_redirect")
def main_page_redirect():
    email = session.get("email")
    return render_template("main.html")


# renders settings template and returns duration settings to be displayed in label
@app.route("/settings")
def settings():
    email = session.get("email")
    duration = str(URLDuration(email).read_duration())
    duration_label = "Trajanje generisanog linka podešeno je na : " + duration
    session["URL_duration"] = duration
    return render_template("settings.html", duration_label=duration_label)


# snimanje unetog trajanja upitnika i ubacivanje u session
@app.route("/settings_set")
def settings_set():
    email = session.get("email")
    input_value = request.args.get("input")
    duration = int(input_value)
    URLDuration(email).set_duration(duration)
    return jsonify({"status": "OK"})


# returns URL duration for the session
@app.route('/session-data')
def session_data():
    email = session.get('email')
    duration = URLDuration(email).read_duration_int()
    session["URL_duration"] = duration
    return jsonify({'URL_duration': duration})


# reset results
@app.route("/settings_reset")
def settings_reset():
    email = session.get('email')
    data = request.args.get('data')
    ResetResults(email, data).reset_results()
    return ""


# Uslovi korišćenja
@app.route("/info")
def info():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("info.html")


# INSTRUMENTI
# PP0
# renders PP0 menu page
@app.route("/pp_0")
def pp_0():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP0/PP_0-info.html")


# renders PP0 generator page
@app.route("/pp_0_gen")
def pp_0_gen():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP0/PP_0-generator.html")


# PP 0 - generates random pp_0 URL
@app.route("/pp_0_gen_but")
def pp_0_gen_but():
    mail = session.get("email")
    url = RandomURLPP0(mail).save_url()
    return url


# renders PP0 results page
@app.route("/pp_0_rez")
def pp_0_rez():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP0/PP_0-rezultati.html")


# returns PP0 results in results table
@app.route("/pp_0_results")
def pp_0_results():
    mail = session.get("email")
    data = ResultsPP0(mail).result_page_data()
    return data


# modal pp_0 interpretation
@app.route("/pp_0_type_indicator", methods=['POST'])
def pp_0_type_indicator():
    input_data = request.get_json()
    result = InterperationModalPP0((input_data)).interpretation_modal()
    return jsonify(result)


# renders PP0 instrument start page
@app.route("/pp_0_inst_name")
def pp_0_inst_name():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP0/PP_0-instrument_name.html")


# renders PP0 instrument page
@app.route("/pp_0_inst", methods=["GET", "POST"])
def pp_0_inst():
    email = session.get('email')
    if email is None:
        return render_template("error.html")
    else:
        if request.method == "POST":
            # IME ISPITANIKA
            pp0_instrument_username = request.form.get(
                'pp0_instrument_username')
            if pp0_instrument_username:
                session['pp0_username'] = pp0_instrument_username
                return render_template("PP0/PP_0-instrument.html")
            else:
                return render_template("PP0/PP_0-instrument_name.html")
        else:
            return render_template("PP0/PP_0-instrument_name.html")


# POSTS question index number and returns dict Q and A
@app.route('/pp0_QA', methods=['POST'])
def receive_QA():
    index_value = int(request.form['integer_value'])
    q_a_return = question_answer(index_value)
    # print(session.get('pp0_username')) ovo dodajem u resulkt varijablu kada saljem rezultate
    return q_a_return

# personality assesment finished, displays results


@app.route("/pp_0_zavrseno", methods=['POST', 'GET'])
def pp_0_zavrseno():
    email = session.get('email')
    user = session.get('pp0_username')

    raw_data = request.form.get('results')
    save_data = (email, 'pp_0', user, raw_data)
    user_id = ModelPP0().save_results(save_data)

    user_mbti_data = InterpretationExamineePP0(user_id).examinee_interpretation()
    session['user_mbti_data'] = user_mbti_data  # save user_mbti_data to session

    delete_url = session.get("delete_URL")
    DeleteURLPP0(str(delete_url)).delete_link()

    
    return jsonify(user_mbti_data)


@app.route("/pp_0_zavrseno_render_page", methods=['POST', 'GET'])
def pp_0_zavrseno_render_page():
    print(session.get('user_mbti_data_local'))
    return render_template("PP0/PP_0-zavrsetak.html")


# MBTI interpretation for generated URL
@app.route('/get_user_mbti_data')
def get_user_mbti_data():
    user_mbti_data = session.get('user_mbti_data_local')
    if user_mbti_data:
        return jsonify(user_mbti_data)
    else:
       return jsonify({'error': 'User MBTI data not found in session'})


# renders PP1 menu page
@app.route("/pp_1")
def pp_1():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP1/PP_1-info.html")


# renders PP1 generator page
@app.route("/pp_1_gen")
def pp_1_gen():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP1/PP_1-generator.html")


# renders PP1 results page
@app.route("/pp_1_rez")
def pp_1_rez():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP1/PP_1-rezultati.html")


# renders PP1 results interpretation page
@app.route("/pp_1_int")
def pp_1_int():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP1/PP_1-interpretacija.html")


# renders PP1 instrument page
@app.route("/pp_1_inst")
def pp_1_inst():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP1/PP_1-instrument.html")


# PP 1-generator, returns random URL to frontend and saves random URL into database for client access *** FIX: need to read season/server duration settings and when saving random URL duration should be included
@app.route("/pp_1_gen_but")
def pp_1_gen_but():
    mail = session.get("email")
    url = RandomURLPP1(mail).save_url()
    return url

# PP 1-results, returns average results, suggestions


@app.route("/pp_1_results")
def pp_1_results():
    mail = session.get("email")
    data = ResultsPP1(mail).average_results()
    data_sug = ResultsPP1(mail).descriptive_results()
    result = {"data": data, "data_sug": data_sug}
    return result


# PP 1-interpretation, returns count, and factors with highest and lowest scores
@app.route("/pp_1_int_results")
def pp_1_int_results():
    mail = session.get("email")
    data = ResultsPP1(mail).get_interpretation()
    return data


# PP 1-upitnik, saves questionnaire data to database
@app.route("/pp_1_upitnik", methods=["POST"])
def cms_store_questionnaire_data():
    mail = session.get("email")
    input_data = request.get_json()
    result = {
        'user_email': mail,
        'raw_results': input_data[:-1],
        'suggestion': input_data[-1]
    }
    UpdateDBModelPP1(result).save_upitnik_data()

    delete_url = session.get("delete_URL")
    DeleteURLPP1(str(delete_url)).delete_upitnik_link()

    return "Update successful"


# PP1 - client questionnaire checks if date valid then if it is reders template
@app.route('/<string:link>')
def check_link(link):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM generated_url WHERE random_url=%s", (link,))
    row = c.fetchone()
    if row is None:
        return render_template('upitnik_error.html')

    session["delete_URL"] = row[1]
    test_code = row[4]
    if test_code == 'pp_1' and datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f') >= datetime.now():
        sender_username = row[3]
        return render_template('PP1/PP_1-instrument_template.html', sender_username=sender_username)
    elif test_code == 'pp_0' and datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f') >= datetime.now():
        sender_username = row[3]
        return render_template('PP0/PP_0-instrument_name_template.html', sender_username=sender_username)
    else:
        return render_template('upitnik_error.html')


# PP2
# renders PP2 info page
@app.route("/pp_2")
def pp_2():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP2/PP_2-info.html")
    

# renders PP2 rezultati
@app.route("/pp_2_rezultati")
def pp_2_rezultati():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP2/PP_2-rezultati.html")


# renders PP2 instrument
@app.route("/pp_2_instrument")
def pp_2_instrument():
    email = session.get('email')
    if email == None:
        return render_template("error.html")
    else:
        return render_template("PP2/PP_2-instrument.html")


# UNIVERSAL: renders finished page
@app.route("/pp_1_zavrseno")
def pp_1_zavrseno():
    return render_template("zavrsetak.html")

# PP2

#upitnik
# PP 1-upitnik, saves questionnaire data to database
@app.route("/pp_2_upitnik", methods=["POST"])
def PCLRSaveData():
    mail = session.get("email")
    input_data = request.get_json()
    
    result = {
        'email': mail,
        'name': input_data['name'],
        'results': input_data['results']
    }
    InstrumentPP2(result).save_results()

    return "Update successful"



@app.route("/pp_2_results")
def pp_2_results():
    mail = session.get("email")
    data = ResultsPP2(mail).display_results()
    return data


if __name__ == "__main__":
    app.run(debug=True)
