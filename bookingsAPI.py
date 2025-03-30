import flask
import pandas 

app = flask()

testStr = "String"
filename = 'test.csv'

# MAKE API GET CALL
# Load data from csv 
def load_date():

    csv = panda.read_csv(filename)
    return testStr