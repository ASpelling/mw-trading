from app import db
from datetime import date
from pandas.tseries.offsets import BDay
import pandas_datareader.data as web
from .update import updatingSCTR, updatingMoneyWave, updatingEMA50, updatingEMALTvsST

class StockExchange(db.Model):
        __tablename__ = 'stockexchange'

        ticker = db.Column(db.String(10), primary_key=True)
        name = db.Column(db.String(40))

	stock_tickers = db.relationship('Company', backref='stock_exchange')

        def __rep__(self):  # pragma : no cover
                return  '<Stock exchange %r>' % (self.symbol)

class Industry(db.Model):
	__tablename__ = 'industry'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), index=True)

	stock_tickers = db.relationship('Company', backref='industry') 

	def __rep__(self): # pragma : no cover
		return '<Industry %r>' % (self.name)

class CapMarket(db.Model):
	__tablename__ = 'capmarket'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), index=True, unique=True)

	stock_tickers= db.relationship('Company', backref='capmarket')

	def __rep__(self):  # pragma : no cover
		return '<Capital market %r>' % (self.name)

class Company(db.Model):
	__tablename__ = 'company'
	
	ticker = db.Column(db.String(10), primary_key=True)
	name = db.Column(db.String(40))
	currency = db.Column(db.String(5))
	
	price = db.Column(db.Float)
	lastPrice = db.Column(db.Float)
	average = db.Column(db.Float, index=True)
	moneywave = db.Column(db.Float)	
	overEma50 = db.Column(db.Boolean, index=True)


	stockexchange_id = db.Column(db.String(10), db.ForeignKey('stockexchange.ticker'))
#	index_id = db.Column(db.String(10), db.ForeignKey('index.ticker'))
	industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'))
	capmarket_id = db.Column(db.Integer, db.ForeignKey('capmarket.id'))


	def update_all(self, startDate, endDate):
		try:
                        daily = web.DataReader(self.ticker, 'yahoo', startDate, endDate)
			readOutTime = daily.iloc[-1].name - (date.today() - BDay(1))
			if readOutTime.days < 0:
				self.average = None
				db.session.commit()
				raise Exception
			adjClose = daily['Adj Close'].values
			high = daily['High'].values
			low = daily['Low'].values
			close = daily['Close'].values
			
			self.price = adjClose[-1]
			self.lastPrice = adjClose[-2]			
			self.average = updatingSCTR(adjClose)
			self.moneywave = updatingMoneyWave(high, low, close)
			self.overEma50 = updatingEMA50(adjClose)


			db.session.commit()
                except Exception,e:
                        print str(e), 'failed to pull pricing data'	


	def __rep__(self):  # pragma : no cover
		return 	'<Company %r>' % (self.ticker)

class Index(db.Model):
        __tablename__ = 'index'

        ticker = db.Column(db.String(10), primary_key=True)
        name = db.Column(db.String(40))

        price = db.Column(db.Float)
        lastPrice = db.Column(db.Float)
        average = db.Column(db.Float, index=True)
        moneywave = db.Column(db.Float)
	
	coppockCurve = db.Column(db.Float)
	emaLTvsST = db.Column(db.Boolean)


#	stock_tickers = db.relationship('Company', backref='index')

	def update_all(self, startDate, endDate):
                try:
                        daily = web.DataReader(self.ticker, 'yahoo', startDate, endDate)
                        adjClose = daily['Adj Close'].values
			close = daily['Close'].values
                        high = daily['High'].values
                        low = daily['Low'].values

                        self.price = adjClose[-1]
                        self.lastPrice = adjClose[-2]
                        self.average = updatingSCTR(adjClose)
                        self.moneywave = updatingMoneyWave(high, low, close)
                        self.emaLTvsST = updatingEMALTvsST(daily)

                        db.session.commit()
                except Exception,e:
                        print str(e), 'failed to pull pricing data'


        def __rep__(self):  # pragma : no cover
                return  '<Index %r>' % (self.ticker)

# To be included
"""
class Commodity(db.Model):
        __tablename__ = 'commodity'

        ticker = db.Column(db.String(10), primary_key=True)
        name = db.Column(db.String(40))

        price = db.Column(db.Float)
        lastPrice = db.Column(db.Float)
        average = db.Column(db.Float, index=True)
        moneywave = db.Column(db.Float)

        coppockCurve = db.Column(db.Float)
        emaLTvsST = db.Column(db.Float)

#       date = db.Column(db.String)
#       plot = db.Column(db.String(15))

        def __rep__(self):  # pragma : no cover
                return  '<Commodity %r>' % (self.symbol)
"""

# To be included
"""
class Currencies(db.Model):
        __tablename__ = 'currencies'

        ticker = db.Column(db.String(10), primary_key=True)
        name = db.Column(db.String(40))

        price = db.Column(db.Float)
        lastPrice = db.Column(db.Float)
        average = db.Column(db.Float, index=True)
        moneywave = db.Column(db.Float)

        coppockCurve = db.Column(db.Float)
        emaLTvsST = db.Column(db.Float)

#       date = db.Column(db.String)
#       plot = db.Column(db.String(15))

        def __rep__(self):  # pragma : no cover
                return  '<Currencies %r>' % (self.symbol)
"""



"""
class SCRT(db.Model):
	__tablename__ = 'SCTR'

	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, index=True)
	sctr = db.Column(db.Decimal(4,2), index=True)
        company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

	def __rep__(self):  # pragma : no cover
		return '<SCRT %r>' % (self.date)
"""
