import os
import collections
import random
import flask

ENCODING = "utf-8"
INDEX_PAGE = "index.html"
TOPIC_PAGE = "topic.html"
QUIZ_PAGE = "quiz.html"
BASE = "data"
TOPIC_LEVELS = (
    "Language",
    "Theme",
    "Topic"
)
SEPARATOR = '/'
PATH_START = len(BASE) + 1
TOPIC_SUFFIX = ".txt"
TOPIC_END = -len(TOPIC_SUFFIX)
TO_ENGLISH = "to"
FROM_ENGLISH = "from"

app = flask.Flask(__name__)

def make_dict(path):
    with open(path, encoding = ENCODING) as file:
        dictionary = collections.deque()
        
        while True:
            foreign = file.readline()[:-1]
            english = file.readline()[:-1]
            
            if foreign and english:
                dictionary.append([foreign, english])
            
            else:
                break
    
    return dictionary

@app.route("/")
@app.route("/<language>")
@app.route("/<language>/<theme>")
def route(language = "", theme = ""):
    path = BASE + SEPARATOR
    level = 0
    back = None
    
    if language:
        back = SEPARATOR
        path += language + SEPARATOR
        level += 1
    
    if theme:
        back += language
        path += theme + SEPARATOR
        level += 1
        topics = [f[:TOPIC_END] for f in os.listdir(path)]
        
    else:
        topics = os.listdir(path)
    
    topic_name = TOPIC_LEVELS[level]
    
    return flask.render_template(
        INDEX_PAGE,
        back = back,
        path = path[PATH_START:],
        topic_name = topic_name,
        topics = topics
    )

@app.route("/<language>/<theme>/<topic>")
def view_topic(language, theme, topic):
    back = SEPARATOR + language + SEPARATOR + theme
    page = back + SEPARATOR + topic
    path = BASE + page + TOPIC_SUFFIX
    dictionary = make_dict(path)
    
    return flask.render_template(
        TOPIC_PAGE,
        back = back,
        page = page,
        language = language,
        topic = topic,
        dictionary = dictionary
    )

@app.route("/<language>/<theme>/<topic>/<mode>")
def quiz(language, theme, topic, mode):
    back = SEPARATOR + language + SEPARATOR + theme + SEPARATOR + topic
    path = BASE + back + TOPIC_SUFFIX
    dictionary = make_dict(path)
    random.shuffle(dictionary)
    questions = [entry[0 if mode == TO_ENGLISH else 1] for entry in dictionary]
    answers = [entry[1 if mode == TO_ENGLISH else 0] for entry in dictionary]
    
    return flask.render_template(
        QUIZ_PAGE,
        back = back,
        language = language,
        topic = topic,
        dictionary = dictionary,
        questions = questions,
        answers = answers,
        mode = mode
    )