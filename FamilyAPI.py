import flask
from flask import Flask, jsonify,request,abort,make_response
from flask_httpauth import HTTPBasicAuth


auth = HTTPBasicAuth()
app = Flask(__name__)
app.config["DEBUG"] = True


# Create some family data in the form of a list of dictionaries.
family = [
    {'id': 0,
     'name': 'Gerardin Niveadhana',
     'age': 34,
     'DOB': '16-09-1986'},
    {'id': 1,
     'name': 'Loyola Stalin',
     'age': 40,
     'DOB': '03-09-1980'},
    {'id': 2,
     'name': 'Jerwin Joseph',
     'age': 6,
     'DOB': '03-03-2015'},
    {'id': 3,
     'name': 'Jeffrin Stalin',
     'age': 2,
     'DOB': '30-01-2019'}
]


# A method to check the password for secured authentication
@auth.get_password
def get_password(username):
    if username == 'gerardin':
        return 'jerwin16'
    return None


# A route to display Home page with all details
@app.route('/family/api/v1/details', methods=['GET'])
@auth.login_required
def homepage():
    return jsonify(family)


# A route to return a record based on the id given in the request
@app.route('/family/api/v1/details/<int:p_id>', methods=['GET'])
@auth.login_required
def get_person(p_id):
    person = [person for person in family if person['id'] == p_id]
    #  If no ID is provided, display an error in the browser.
    if len(person) == 0:
        abort(404)
    # If ID is provided,return the result.
    return jsonify(person[0])


# A route to create a new record
@app.route('/family/api/v1/details', methods=['POST'])
@auth.login_required
def create_record():
    if not request.json or not 'name' in request.json:
        abort(400)
    person = {
        'id': family[-1]['id'] + 1,
        'name': request.json['name'],
        'age': request.json['age'],
        'DOB': request.json.get('DOB', "")
    }
    family.append(person)
    return jsonify(person), 201

# A route to udpate a record based on the id given
@app.route('/family/api/v1/details/<int:p_id>', methods=['PUT'])
@auth.login_required
def update_record(p_id):
    person = [person for person in family if person['id'] == p_id]
    if len(person) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400)
    if 'age' in request.json and type(request.json['age']) is not int:
        abort(400)
    if 'DOB' in request.json and type(request.json['DOB']) is not str:
        abort(400)
    person[0]['name'] = request.json.get('name', person[0]['name'])
    person[0]['age'] = request.json.get('age', person[0]['age'])
    person[0]['DOB'] = request.json.get('DOB', person[0]['DOB'])
    return jsonify(person[0])


# A route to delete a record based on the id given
@app.route('/family/api/v1/details/<int:p_id>', methods=['DELETE'])
@auth.login_required
def delete_record(p_id):
    person = [person for person in family if person['id'] == p_id]
    if len(person) == 0:
        abort(404)
    family.remove(person[0])
    return jsonify({'result': 'Deleted'})


# A error handler to handle  when the id is not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# A error handler to handle for unauthorized access
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


# A error handler to handle when the data cannot be processed
@app.errorhandler(400)
def cannot_process(error):
    return make_response(jsonify({'error': 'Cannot process the data'}), 400)


if __name__ == '__main__':
    app.run()





# Curl command to get all data
# $ curl -i -u gerardin:jerwin16  http://localhost:5000/family/api/v1/details

# Curl command to get a particular data based on the id given
# $ curl -i -u gerardin:jerwin16  http://localhost:5000/family/api/v1/details/2


# Curl command to create a new record
# $ curl -i -u gerardin:jerwin16 -H "Content-Type: application/json" -X POST -d '{"name": "Maria", "age": 1, "DOB":"01-01-2020"}' http://localhost:5000/family/api/v1/details

# Curl command to create a new record
# $ curl -i -u gerardin:jerwin16 -H "Content-Type: application/json" -X PUT -d '{"age":41}' http://localhost:5000/family/api/v1/details/1

# Curl command to delete a record
# $ curl -i -u gerardin:jerwin16 -H "Content-Type: application/json" -X DELETE  http://localhost:5000/family/api/v1/details/1