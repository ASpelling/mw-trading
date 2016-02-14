#!venv/bin/python
# coding=UTF-8
from app import db, models
import pandas as pd

def includeStockEx():
	# Include OMX SE
	u = models.StockExchange(ticker='OMXSE', name='OMX Stockholm')
	db.session.add(u)
	db.session.commit()

	# Include OMX NO
        u = models.StockExchange(ticker='OMXNO', name='OMX Oslo')
        db.session.add(u)
        db.session.commit()

	# Include OMX DK
        u = models.StockExchange(ticker='OMXDK', name='OMX Copenhagen')
        db.session.add(u)
        db.session.commit()

	# Include OMX FI
        u = models.StockExchange(ticker='OMXFI', name='OMX Helsinki')
        db.session.add(u)
        db.session.commit()

	# Include NYSE
        u = models.StockExchange(ticker='NYSE', name='The New York Stock Exchange')
        db.session.add(u)
        db.session.commit()

	# Include Nasdaq
        u = models.StockExchange(ticker='NASDAQ', name='Nasdaq Stock Exchange')
        db.session.add(u)
        db.session.commit()

def includeCapMarket():
	u = models.CapMarket(name='Large cap')
	db.session.add(u)
	db.session.commit()
	u = models.CapMarket(name='Mid cap')
	db.session.add(u)
	db.session.commit()
	u = models.CapMarket(name='Small cap')
	db.session.add(u)
	db.session.commit()

def includeIndustries():
	u = models.Industry(name='Capital Goods')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Consumer Non-Durables')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Consumer Services')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Energy')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Finance')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Health Care')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Industries')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Technology')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Telecommunications')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Transportation')
	db.session.add(u)
	db.session.commit()
	u = models.Industry(name='Utilities')
	db.session.add(u)
	db.session.commit()

def includeCompanies(stocklist):
	for stock in stocklist.T:
		if stocklist.loc[stock,'Sector'] == 'Capital Goods':
			sector = 1
		elif stocklist.loc[stock,'Sector'] == 'Consumer Non-Durables':
                	sector = 2
                elif stocklist.loc[stock,'Sector'] == 'Consumer Services':
        	        sector = 3
		elif stocklist.loc[stock,'Sector'] == 'Energy':
       	                sector = 4
		elif stocklist.loc[stock,'Sector'] == 'Finance':
       	                sector = 5
		elif stocklist.loc[stock,'Sector'] == 'Health Care':
       	                sector = 6
		elif stocklist.loc[stock,'Sector'] == 'Industries':
               	        sector = 7
		elif stocklist.loc[stock,'Sector'] == 'Technology':
       	                sector = 8
		elif stocklist.loc[stock,'Sector'] == 'Telecommunications':
       	                sector = 9
                elif stocklist.loc[stock,'Sector'] == 'Transportation':
                        sector = 10
		elif stocklist.loc[stock,'Sector'] == 'Utilities':
       	                sector = 11
		if stocklist.loc[stock,'Marketcap'] == 'Large cap':
                       	cap = 1
		elif stocklist.loc[stock,'Marketcap'] == 'Mid cap':
			cap = 2
		elif stocklist.loc[stock,'Marketcap'] == 'Small cap':
        	        cap = 3
		indu = models.Industry.query.get(sector)
		capMar = models.CapMarket.query.get(cap)
		stockEx = models.StockExchange.query.get(stocklist.loc[stock, 'Stock exchange'])
		u = models.Company(ticker=stock, name=unicode(stocklist.loc[stock,'Name'], encoding = 'utf-8', errors = 'ignore'), industry=indu, capmarket=capMar, currency=stocklist.loc[stock,'Currency'], stock_exchange=stockEx)
		db.session.add(u)
		db.session.commit()


def includeIndexes(indexlist): 
	for index in indexlist.T:
		u = models.Index(ticker=index, name=indexlist.loc[index,'Name'])
                db.session.add(u)
                db.session.commit()


# ---   Start of program ------------------------------
doStockEx = raw_input('Include stock exchanges?:[y/n] ')
doCapMarket = raw_input('Include Cap markets?:[y/n] ')
doIndustries = raw_input('Include industries?:[y/n] ')
doCompanies = raw_input('Include companies?:[y/n] ')
doIndexes = raw_input('Include indexes?:[y/n] ')


if doStockEx.lower() ==  'y':
	print 'Including Stock Exchanges...'
	includeStockEx()
	print 'Stock Exchanges Done!'
	stockexchanges = models.StockExchange.query.all()
	for u in stockexchanges:	
		print(u.ticker, u.name)

if doCapMarket.lower() == 'y':
	print 'Including Cap Markets...'
	includeCapMarket()
	print 'Cap Markets Done!'
	capmarkets = models.CapMarket.query.all()
	for u in capmarkets:	
		print(u.id, u.name)

if doIndustries.lower() == 'y':
	print 'Including Industries...'
        includeIndustries()
	print 'Industries Done!'
	industries = models.Industry.query.all()
	for u in industries:
                print(u.id, u.name)
	
if doCompanies.lower() == 'y':
	print 'Including stocks...'
	listType = raw_input('Which list you like to include [se, us]: ')
	stocklist = pd.read_csv('stocklist_'+listType+'.csv', index_col = 'Ticker', sep=';')
        includeCompanies(stocklist)
	print 'Companies Done!'
if doIndexes.lower() == 'y':
	print 'Including Indexes...'
        indexlist = pd.read_csv('indexlist.csv', index_col = 'Ticker', sep=';')
        includeIndexes(indexlist)
	print 'Indexes Done!'
	index = models.Index.query.all()
        for u in index:
                print(u.ticker, u.name)

print 'All Done!'
