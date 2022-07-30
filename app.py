from flask import Flask, request
from flask_migrate import Migrate
from models.Database import db
from flask_restx import Resource, Api, fields
from models.Database import User, News
from controllers.Controller import LOG, NEWS
from flask_restx.reqparse import RequestParser
from faker import Faker

app = Flask(__name__)
app.config.from_object('config')
nFake = Faker()

db.init_app(app)
migrate = Migrate(app, db)

authorizations = {
    'api_key' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'x-access-token'
    }
}

apidoc = Api(app, doc='/', version='1.0', title='Docs Fake News API',
description = 'Docs Fake News API v 1.0', authorizations=authorizations)

doc = apidoc.namespace('user')
doc_news = apidoc.namespace('api/v2/news')

login_model = doc.model('Login', {
    'users_id': fields.Integer(required=True, description='id identifier'),
    'name': fields.String(required=True, description='name your-name'),
    'read_key': fields.String(required=True, description='read_key your-read_key'),
    'write_key': fields.String(required=True, description='write_key your-write_key')
})

news_model = doc.model('News', {
    'news_id': fields.Integer(required=True, description='id identifier'),
    'title': fields.String(required=True, description='title your-title'),
    'content': fields.String(required=True, description='content your-content'),
    'flag': fields.Integer(required=True, description='flag num-flag')
})

auth_reqparser = RequestParser(bundle_errors=True)
auth_reqparser.add_argument(
    name="username", type=str, location="form", required=True, nullable=False
)
auth_reqparser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)

reg_reqparser = RequestParser(bundle_errors=True)
reg_reqparser.add_argument(
    name="name", type=str, location="form", required=True, nullable=False
)
reg_reqparser.add_argument(
    name="username", type=str, location="form", required=True, nullable=False
)
reg_reqparser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)

news_reqparser = RequestParser(bundle_errors=True)
news_reqparser.add_argument(
    name="title", type=str, location="form", required=True, nullable=False
)
news_reqparser.add_argument(
    name="content", type=str, location="form", required=True, nullable=False
)
news_reqparser.add_argument(
    name="flag", type=int, location="form", required=True, nullable=False
)

patch_reqparser = RequestParser(bundle_errors=True)
patch_reqparser.add_argument(
    name="flag", type=int, location="form", required=True, nullable=False
)

@doc.route('/login')
class Login(Resource):
    @doc.doc('login')
    @doc.marshal_list_with(login_model)
    @doc.expect(auth_reqparser)
    def post(self):
        request_data = auth_reqparser.parse_args()
        uname= request_data.get("username")
        password = request_data.get("password")
        return LOG.get(uname, password)

@doc.route('/register')
class Login(Resource):
    @doc.doc('register')
    @doc.expect(reg_reqparser)
    def post(self):
        request_data = reg_reqparser.parse_args()
        name = request_data.get("name")
        uname= request_data.get("username")
        password = request_data.get("password")
        return LOG.create(name, uname, password)

@doc_news.route('')
class Beritaget(Resource):
    @doc_news.doc('News Get', security='api_key')
    @doc.marshal_list_with(news_model)
    def get(self):
        try:
            if User.verify_apiRead(request.headers['x-access-token']) == True:
                return NEWS.all(request.headers['x-access-token'])
        except:
            doc_news.abort(403, "Invalid APIKey")

    @doc.expect(news_reqparser)
    @doc_news.doc('News Post', security='api_key')
    def post(self):
        try:
            if User.verify_apiWrite(request.headers['x-access-token']) == True:
                request_data = news_reqparser.parse_args()
                title = request_data.get("title")
                content = request_data.get("content")
                flag = request_data.get("flag")
                return NEWS.create(title, content, flag, request.headers['x-access-token'])
        except:
            doc_news.abort(403, "Invalid APIKey")

@doc_news.route('/<int:news_id>')
class Beritanum(Resource):
    @doc_news.doc('News Get by ID', security='api_key')
    @doc_news.marshal_list_with(news_model)
    def get(self, news_id):
        try:
            if User.verify_apiRead(request.headers['x-access-token']) == True:
                return NEWS.one(news_id, request.headers['x-access-token'])
        except:
            doc_news.abort(403, "Invalid APIKey")
    
    @doc_news.doc('News Update', security='api_key')
    @doc.expect(news_reqparser)
    def put(self, news_id):
        try:
            if User.verify_apiWrite(request.headers['x-access-token']) == True:
                request_data = news_reqparser.parse_args()
                title = request_data.get("title")
                content = request_data.get("content")
                flag = request_data.get("flag")
                return NEWS.update(news_id, title, content, flag, request.headers['x-access-token'])
        except:
            doc_news.abort(403, "Invalid APIKey")
    
    @doc_news.doc('News Patch', security='api_key')
    @doc.expect(patch_reqparser)
    def patch(self, news_id):
        try:
            if User.verify_apiWrite(request.headers['x-access-token']) == True:
                request_data = patch_reqparser.parse_args()
                flag = request_data.get("flag")
                return NEWS.patch(news_id, flag, request.headers['x-access-token'])
        except:
            doc_news.abort(403, "Invalid APIKey")

    @doc_news.doc('Delete News', security='api_key')
    def delete(self, news_id):
        try:
            if User.verify_apiWrite(request.headers['x-access-token']) == True:
                return NEWS.delete(news_id, request.headers['x-access-token'])
        except:
            doc_news.abort(403, "Invalid APIKey")


if __name__ == '__main__':
    app.run(port=4000, debug=True)