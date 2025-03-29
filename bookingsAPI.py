import flask
import pandas 

app = flask()

testStr = "String"
filename = 'test.csv'

# Load data from csv 
def load_date():

    csv = panda.read_csv(filename)
    return testStr