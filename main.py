from flask import Flask, jsonify
from flask_restx import Resource, Api
from customer_orders import orders
from season_orders import seasonOrders
from weather import weather

app = Flask(__name__)
api = Api(app, version='1.0', title='3 pruebas de python', description='API Documentation')
ns = api.namespace('', description='Customer orders, Seasons and Weather')

@ns.route('/orders')
class Orders(Resource):
    def get(self):
        return jsonify(orders)

@ns.route('/seasons')
class Seasons(Resource):
    def get(self):
        return jsonify(seasonOrders)

@ns.route('/weather')
class Weathers(Resource):
    def get(self):
        return jsonify(weather)

@ns.route('/orders/<string:name>')
@ns.doc(params={'name': 'The customer order'})
class Order(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'ORDER NOT FOUND')
    def get(self, name):
        result = "SHIPPED"
        canceledCounter = 0
        try:
            for record in orders[name]:
                if record['status'] == "PENDING":
                    result = "PENDING"
                elif record['status'] == "CANCELLED":
                    canceledCounter += 1
            if canceledCounter == len(orders[name]):
                result = "CANCELLED"
        except KeyError:
            return "ORDER NOT FOUND", 400
        return jsonify({ "order_number":name, "status":result })

@ns.route('/seasons/<string:order>')
@ns.doc(params={'order': 'The order'})
class Season(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'ORDER NOT FOUND')
    def get(self, order):
        try:
            date = seasonOrders[order]
            month, day, year = [int(x) for x in date.split("/")]
            result = ''
            if month == 1 or month == 2:
                result = 'Winter'
            elif month == 4 or month == 5:
                result = 'Spring'
            elif month == 7 or month == 8:
                result = 'Summer'
            elif month == 10 or month == 11:
                result = 'Fall'
            elif month == 3:
                result = 'Winter' if 1 <= day <= 20 else 'Spring'
            elif month == 6:
                result = 'Spring' if 1 <= day <= 21 else 'Summer'
            elif month == 9:
                result = 'Summer' if 1 <= day <= 22 else 'Fall'
            elif month == 12:
                result = 'Fall' if 1 <= day <= 21 else 'Winter'
        except KeyError:
            return "ORDER NOT FOUND", 400
        return jsonify({ "order_id":order, "season":result })

@ns.route('/weather/<string:date>')
@ns.doc(params={'date': 'The date'})
class Weather(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'DATE NOT FOUND')
    def get(self, date):
        try:
            todayWasRainy = weather[date]
            month, day, year = [int(x) for x in date.split("-")]
            yesterdayWasRainy = weather["%d-%d-%d" % (month, day-1, year)]
            result = todayWasRainy and yesterdayWasRainy == False
        except KeyError:
            return "DATE NOT FOUND", 400
        return jsonify({ "date":date, "was_rainy":result })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)