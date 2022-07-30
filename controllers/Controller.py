from models.Database import User, News, UserSchema, NewsSchema, db

class Logon(object):
    def __init__(self):
        '''Global Var in Here'''

    def get(self, uname, password):
        obj = User.get_or_404_via_username(uname)
        verify = obj.verify_password(password)
        if not obj:
            return 'Login Gagal, Cek Username Anda',404
        elif not verify:
            return 'Login gagal, Cek Password Anda',404
        else:
            one = User.query.filter_by(uname=uname).first()
            schema = UserSchema()
            data = schema.dump(one)
            return data

    def create(self, name, uname, password):
        obj = User.get_or_404_via_username(uname)
        if not obj:
            obj = User(name=name, uname=uname)
            obj.hash_password(password)
            obj.save()
            return {
                        
                    'message': 'Success!'
                        
                }
        else:
            return {
                
                'message': "Username is Taken"
            
            }

class Nows(object):
    def __init__(self):
        '''Global Var in Here'''

    def all(self, token):
        if User.getname_byreadkey(token) == True:
            all = News.query.all()
            schema = NewsSchema(many=True)
            data = schema.dump(all)
            # print(data)
            return data
        else:
            all = News.query.filter_by(flag=1).all()
            schema = NewsSchema(many=True)
            data = schema.dump(all)
            # print(data)
            return data

    def one(self, news_id, token):
        if User.getname_byreadkey(token) == True:
            one = News.query.filter_by(news_id=news_id).first()
            schema = NewsSchema()
            data = schema.dump(one)
            # print(data)
            return data
        else:
            one = News.query.filter_by(flag=1).first()
            schema = NewsSchema()
            data = schema.dump(one)
            # print(data)
            return data

    def create(self, title, content, flag, token):
        if User.getname_bywritekey(token) == True:
            obj = News(title=title, content=content, flag=flag, created_by=User.get_idwrite(token))
            obj.save()
            return {
                            
                        'message': 'Success!'
                            
                    }
        else:
            return {
                            
                        'message': 'Cannot Create Draft or Non Active Content by User!'
                            
                    }
    
    def update(self, news_id, title, content, flag, token):
        if User.getname_bywritekey(token) == True:
            datas = News.query.filter_by(news_id = news_id).first()
            datas.news_id = news_id
            datas.title = title
            datas.content = content
            datas.flag = flag
            datas.updated_by = User.get_idwrite(token)
            db.session.commit()
            return {
                                
                            'message': 'Update Success!'
                                
                        }
        else:
            return {
                            
                        'message': 'Cannot Create Draft or Non Active Content by User!'
                            
                    }


    def patch(self, news_id, flag, token):
        if User.getname_bywritekey(token) == True:
            datas = News.query.filter_by(news_id = news_id).first()
            datas.news_id = news_id
            datas.flag = flag
            db.session.commit()
            return {
                                
                            'message': 'Patch Success!'
                                
                        }
        else:
            return {
                            
                        'message': 'Cannot Create Draft or Non Active Content by User!'
                            
                    }

    def delete(self, news_id, token):
        if User.getname_bywritekey(token) == True:
            datas = News.query.filter_by(news_id = news_id).first()
            db.session.delete(datas)
            db.session.commit()
            return {
                                
                            'message': 'Delete Success!'
                                
                        }
        else:
            return {
                            
                        'message': 'Cannot Create Draft or Non Active Content by User!'
                            
                    }

LOG = Logon()
NEWS = Nows()