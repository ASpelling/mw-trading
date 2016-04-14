# ---------------- AStrading - Update --------------
# --------------- Created by Aron Svedin -----------
# -------------------- 2016-01-25 ------------------
'''
Update functions for Classes in Models

- Update SCTR - updatingSCTR()
in: array (Adj Close)
out: float (Average SCTR over SCTR_AVERAGE days, EMA50)

- Update Money wave - updatingMoneyWave()
in: array (High, Low, Adj Close, nextMWPrice = False, MW)
out: float (Money Wave)

- Sub func
Update next stock price for a fixed MW - if nextMWPrice = True
out: float (Price)

- Update weekly EMA Long Term (50) vs Sort Term (10) - updatingEMALTvsST()
in: array (Adj Close)
out: Boolean (or array for plot)

- Update CoppockCurve - updatingCoppock()
Not yet implemented!
in: ?
out: Boolean (or array for plot)

- Update plot - updatingPlot()
Not yet implemented!
in:
out:
'''

import pandas as pd
import numpy as np
import talib as tb
from config import SCTR_AVERAGE

def updatingSCTR(adjClose):
	if len(adjClose) > 250:
	# -- Long term SCTR --------------------
		ema200 = tb.EMA(adjClose, timeperiod=200)
		sctrEMA200 = ((adjClose/ema200)-1)

		sctrROC125 = tb.ROC(adjClose, timeperiod=125)

		longTerm = ((sctrEMA200*0.3) + (sctrROC125*0.3))

	# -- Medium term SCTR ------------------
		ema50 = tb.EMA(adjClose, timeperiod=50)
		sctrEMA50 = ((adjClose/ema50)-1)

		sctrROC20 = tb.ROC(adjClose, timeperiod=20)

		mediumTerm = ((sctrEMA50*0.15) + (sctrROC20*0.15))

	# -- Short term SCTR -------------------
		ppo = tb.PPO(adjClose, fastperiod=12, slowperiod=26, matype=1)
		ppoEMA = tb.EMA(ppo, timeperiod=9)
		ppoHist = ppo - ppoEMA
		ppoHistSlope = (ppoHist - np.roll(ppoHist,3))/3
		ppoHistSlope[ppoHistSlope > 1] = 1
		ppoHistSlope[ppoHistSlope < -1] = -1

		rsi14 = tb.RSI(adjClose, timeperiod=14)

		shortTerm = (((ppoHistSlope+1)*50)*0.05) + (rsi14*0.05)
		sctr =  (longTerm + mediumTerm + shortTerm)
		return sctr[-1]     #*SCTR_AVERAGE):].mean()

	# Throw exception?
	return None

def updatingMoneyWave(highp, lowp, closep, nextMWPrice = False):
	if len(closep) > 10:
#		slowk, slowd = tb.STOCH(highp, lowp, closep, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=1, slowd_matype=0)
		lowest, highest =  pd.rolling_min(lowp, 5), pd.rolling_max(highp, 5)
		stoch = 100 * (closep - lowest) / (highest - lowest)
#		if nextMWPrice:
		MWhigh = 80
		MWlow = 20
		slowk = pd.rolling_mean(stoch, 3)[-1]

		if slowk > MWhigh:
			newPrice = ((highest[-1]-lowest[-1])*(((MWhigh*3)-stoch[-1]-stoch[-2])/100)+lowest[-1])
			print 'Buy below '
			print newPrice
			if nextMWPrice:
				return newPrice
		elif slowk < MWlow:
			newPrice = ((highest[-1]-lowest[-1])*(((MWlow*3)-stoch[-1]-stoch[-2])/100)+lowest[-1])
			print 'Buy above '
			print newPrice
			if nextMWPrice:
				return newPrice
		if nextMWPrice:
			return 0
#			preStoch = ((MW*3) - slowd[-1] - slowd[-2])/100
#			newPrice = ((max(highp[-4:]) - min(lowp[-4:]))*preStoch)+min(lowp[-4:])

		return slowk
	# Throw exception?
	return (None, None)


def updatingEMA50(adjClose):
        if len(adjClose) > 60:
                ema50 =  tb.EMA(adjClose, timeperiod=50)

                return adjClose[-1] > ema50[-1]


def updatingEMALTvsST(daily):
	if len(daily['Adj Close']) > 300:
		weekly = daily.asfreq('W-FRI', method='pad', how='end')
		shortTerm =  tb.EMA(weekly['Adj Close'].values, timeperiod=10)
		longTerm =  tb.EMA(weekly['Adj Close'].values, timeperiod=50)

		return shortTerm[-1] > longTerm[-1]

	# Throw exception
	return None

def updatingCoppock():
	return True

def updatingPlot():
	return True
