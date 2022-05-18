from flask import Flask, jsonify, abort, request
from src.controllers.controller import Controller

from src.util.globals import get_global_variable as ggv

app = Flask('todoapp')
controller = Controller()

@app.route('/')
def ping():
    return jsonify({'version': ggv('version')}), 200

@app.route('/<uid>/item', methods=['POST', 'DELETE'])
def checkout(uid):
    item = request.form.to_dict()
    try:
        if request.method == 'POST':
            controller.add_item_to_cart(uid=uid, item=item)
            return jsonify({'user': uid, 'added': item}), 200
        elif request.method == 'DELETE':
            controller.remove_item_from_cart(uid=uid, item=item)
            return jsonify({'user': uid, 'removed': item}), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

@app.route('/<uid>/checkout', methods=['POST'])
def checkout(uid):
    try:
        total = controller.checkout(uid=uid)
        return jsonify({'user': uid, 'total': total}), 200
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
        abort(500, 'Unknown server error')

if __name__ == '__main__':
    print(app.url_map)
    app.run()