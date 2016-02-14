from flask import render_template, flash, redirect, url_for
from app import app, db
from .models import StockExchange, Company, Index #, Industry, CapMarket
from .grapher import graphData
from config import POST_PER_PAGE
from config import SCTR_AVERAGE
from datetime import date
import time
from dateutil.relativedelta import relativedelta
import numpy as np

stockex = 'OMXSE'
cap = 3
overviewList = 10

@app.route('/')
@app.route('/index')
def index():
	top = Company.query.filter(Company.average != None, Company.stockexchange_id == stockex, Company.capmarket_id != cap).order_by(Company.average.desc())[:overviewList]
	flop = Company.query.filter(Company.average != None, Company.stockexchange_id == stockex, Company.capmarket_id != cap).order_by(Company.average.desc())[-1*overviewList:]
	indexes = Index.query.order_by(Index.average.desc()).all()

	stocksAboveEma50 = (float(Company.query.filter(Company.average != None, Company.overEma50 == True, Company.stockexchange_id == stockex).count())/float(Company.query.filter(Company.average != None, Company.stockexchange_id == stockex).count()))*100

	return render_template("overview.html", title='Overview', tops=top, flops=flop, indexes = indexes, stocksAboveEma50=stocksAboveEma50)


@app.route('/stocks')
@app.route('/stocks/<int:page>')
def stocks(page=1):
	stocklist = Company.query.filter(Company.average != None, Company.stockexchange_id == stockex, Company.capmarket_id != cap).order_by(Company.average.desc()).paginate(page, POST_PER_PAGE, False)
	indexes = Index.query.order_by(Index.average.desc()).all()
	return render_template("stocks.html", title='Stocks', stocklist=stocklist, page=page, indexes=indexes)


@app.route('/stockupdater')
def stockupdater():
	startTime = time.time()

        startDate = date.today() + relativedelta(weeks=-60)
        endDate = date.today() 
        print 'Getting data from {} to {} averaging the SCTR over {} days' .format(startDate,endDate,SCTR_AVERAGE)

	stocklist = Company.query.all() 
	# -- Update stocks -----------
        count = len(stocklist) + 1
        n = 1
        for asset in stocklist:
                print asset.name
                print "{} of {}" .format(n, count - 1)
                n += 1
		asset.update_all(startDate, endDate)


	flash('Stocklist is updated')

        endTime = time.time()
        print "Updating took {} {}" .format(int(endTime - startTime), 's')

	return redirect(url_for('index'))

@app.route('/indexupdater')
def indexupdater():
	startTime = time.time()

        startDate = date.today() + relativedelta(weeks=-90)
        endDate = date.today() 
        print 'Getting data from {} to {} averaging the SCTR over {} days' .format(startDate,endDate,SCTR_AVERAGE)

	indexlist = Index.query.all()
	# -- Update index ----------
        count = len(indexlist) + 1
        n = 1
        for asset in indexlist:
                print asset.name
                print "{} of {}" .format(n, count - 1)
                n += 1
                asset.update_all(startDate, endDate)

	flash('Indexlist is updated')

        endTime = time.time()
        print "Updating took {} {}" .format(int(endTime - startTime), 's')

	return redirect(url_for('index'))

@app.route('/grapher/<ticker>')
def grapher(ticker):
	if ticker[0] == "^":
		asset = Index.query.get(ticker)
	else:
		asset = Company.query.get(ticker)
	indexes = Index.query.order_by(Index.average.desc()).all()
	graphData(asset)
	return render_template("graph.html", stock=asset.ticker, indexes = indexes)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def not_found_error(error):
	db.session.rollback()
        return render_template('500.html'), 500
