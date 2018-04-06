from app import app
app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'])
