# mw-trading
====
Trading program "Buy expensive, sell more expensive"

Takes a pre-defined list, i.e. Nasdaq OMX, and ranks the stocks according to Relative strenght index (RSI)
The top candidates and shows in the Money wave:
- under 20 get ready to buy
- over 80 get ready to sell

===
Pulls the data from Yahoo! Finance
Calculate predefined values used to define candidates with associated probability
Shows the candidates as a webpage using Flask


# Features
* It could also filter the list according to
  - Large-cap
  - Mid-cap
  - Small-cap
  - Segment
	- Basic materials
	- Consumer goods
	- Consumer services
	- Finacials
	- Health care
	- Industrials
	- Oil & Gas
	- Technology
	- Telecommunications
* Shows the RSI for world indexes

* In bear market shows a list of the weakest RSI
