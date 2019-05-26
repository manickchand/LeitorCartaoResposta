from flask import Flask, request
from flask_restful import Resource, Api
import ProcessaGabarito as pg

app = Flask(__name__)
api = Api(app)

#class Gabarito(Resource):
@app.route('/gabarito', methods=['GET','POST'])
def get():
    v = request.args.get('id')

    x = pg.init(v)

    return "ola cara %s" % x

#api.add_resource(Gabarito, '/gabarito')
# if __name__ == 'main':
#     app.run(port='5002')

