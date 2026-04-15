from flask import Flask, jsonify, request, make_response
from models import *
from flask_migrate import Migrate
from flask_bcrypt import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///entries.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app=app)

migrate = Migrate(app, db)

@app.route('/', methods=['GET'])
def index():
    return make_response({'message': 'Welcome to the Journal Entries'}, 200)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print('Received data:', username , password)

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

@app.route('/entries', methods=['GET'])
def get_journal_entries():
    # entries = JournalEntry.query.all()
    
    # entries_dict = JournalEntrySchema().dump(entries, many=True)

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)

    pagination = JournalEntry.query.paginate(page=page, per_page=per_page, error_out=False)

    entries = pagination.items
    
    return make_response({
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "items": [JournalEntrySchema().dump(e) for e in entries]
    }, 200)
    
@app.route('/entries', methods=['POST'])
def create_journal_entry():
    try:
        # Deserializing incoming data
        incoming_data = JournalEntrySchema().load(request.get_json())
        
        db.session.add(incoming_data)
        db.session.commit()
        
        # Serializing
        incoming_data_dict = JournalEntrySchema().dump(request.get_json())
        
        return make_response(incoming_data_dict, 201)
        
    except ValidationError as e:
        return make_response({'message': f'Could not load the data: {e}'})
    
@app.route('/entries/<int:id>', methods=['PATCH'])
def update_journal_entry(id):
    try:
        # Deserializing incoming data
        incoming_data = JournalEntrySchema().load(request.get_json(), many=False)
        
        entry = JournalEntry.query.filter_by(id=id).first()
        
        if not entry:
            return make_response({'Error': f'Could not find data with id: {id}'}, 404)
            
        if 'title' in incoming_data:
            incoming_data['title'] = entry.title
        if 'content' in incoming_data:
            incoming_data['content'] = entry.content
            
        db.session.commit()
        return make_response({'message': 'Data updated successfully'}, 200)
        
    except Exception as e:
        return make_response({'Error': f'An error occurred while updating the data with id: {id}'}, 404)
    
@app.route('/entries/<int:id>', methods=['DELETE'])
def delete_journal_entry(id):
    try:        
        entry = JournalEntry.query.filter_by(id=id).first()
        
        if not entry:
            return make_response({'Error': f'Could not find data with id: {id}'}, 404)
            
        db.session.delete(id)
        db.session.commit()
        return make_response({}, 200)
        
    except Exception as e:
        return make_response({'Error': f'An error occurred while deleting the data with id: {id}'}, 404)
    
if __name__ == "__main__":
    app.run(port=5555, debug=True)