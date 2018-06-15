'''
run script to start the app
'''


#checks if the script got executed as the main program
if __name__ == '__main__':
    #import the main app from the file __init__.py in the directory app
    from app import app
    #runs the flask app on the port 5000
    app.run(port=5000)
