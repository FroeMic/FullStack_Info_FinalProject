from app import app, _bootstrap_app_if_neccessary
_bootstrap_app_if_neccessary()
app.run(debug=True, host=app.config['HOST'], port=app.config['PORT'], use_reloader=False)

