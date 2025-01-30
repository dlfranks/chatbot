from api import create_app

app = create_app()

@app.route('/cause-error')
def cause_error():
    raise Exception("Intentional error for testing.")

if __name__ == '__main__':
    app.run(port=5001, debug=True)