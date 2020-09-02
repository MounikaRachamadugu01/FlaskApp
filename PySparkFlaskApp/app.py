from flask import Flask, redirect, url_for, request, render_template
from pyspark.sql import SparkSession
from pyspark.shell import sqlContext
import numpy as np
import pandas as pd


sc = SparkSession.builder.appName("TwitterAPIQueryExecutor").config ("spark.sql.shuffle.partitions", "50").config("spark.driver.maxResultSize","5g").config ("spark.sql.execution.arrow.enabled", "true").getOrCreate()
app = Flask(__name__)

@app.route('/')
def index():
    """Routes user to /welcome page"""
    return redirect(url_for('welcome'))

@app.route("/welcome", methods = ["GET", "POST"])
def welcome():
    """The index page where user can query the data"""
    if request.method == 'POST':
        query = request.form["queryDef"]
        return redirect(url_for('results', query_def=query))
    else:
        return render_template("index.html")

@app.route('/results/<query_def>')
def results(query_def):
    """Query execution logic """
    # Read JSON
    data_frame = sc.read.json("dataset/tweetsdata_v1.json")
    data_frame.createOrReplaceTempView("tweetDatatable")
    
    query = sqlContext.sql(query_def)
    # Getting contents of df as Pandas 
    data_frame = query.toPandas()
    # data_frame_dropna = data_frame.dropna()
    # return data_frame_dropna.to_html()
    # Display results in HTML
    #data_frame = pd.DataFrame(np.random.randn(20, 5))
    
   # return data_frame.to_html(classes = 'styles')
   #myhtml = data_frame.style.set_properties(**{'font-size': '11pt', 'font-family': 'Calibri','border-collapse': 'collapse','border': '1px solid black'}).render()

#with open('myhtml.html','w') as f:
    #f.write(myhtml)

    return data_frame.to_html()

 #return render_template("analysis.html")
 #s = data_frame.style.set_properties(**{'text-align': 'center'})
#s.render()



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    sc.stop()