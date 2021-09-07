from __init__ import app
import config

if __name__ == '__main__':
    app.run(host=config.RUN_HOST,port=config.RUN_PORT,debug=config.DEBUG)
