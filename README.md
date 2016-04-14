# mw-trading
====
Trading program "Buy on momentum"

Checks which assets, on a pre-defined list, are MW* < 20. These assets are put on a candidate list with a buy price, if the asset closes above this buy price it is a buy. When the assets after a trading day's close have MW > 20 a ML aglorithm ranks if it is a buy or not together with stopp loss and risk (but no reward). 

This could also be used to sell short.

Money wave:
- under 20 get ready to buy
- over 80 get ready to sell

===
Pulls the data from Yahoo! Finance
Calculate predefined values used to define candidates with associated probability
Shows the candidates as a webpage using Flask

### Features
- Asset indicators
- Related assets/indexes indicators

*MW is the slow stochastics. 
