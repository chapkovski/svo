# Social value orientation measure
## (Murphy, Ackermann,  Handgraaf, 2011)

This is a prototype of Social value orientation measure in oTree.

It uses a set of 6 Dictator-like decisions, that defines the measure of 
prosociality of the subject. Please, read more at the author's (Ryan Murphy) 
page [here](http://vlab.ethz.ch/styled-2/index.html).

Setting `Constants.random` to `True` will randomize the order of the items. 
The order is stored in `item_order` of `Player` model.

The specific values of SVO are taken from [SVO file](http://ryanomurphy.com/styled-2/downloads/files/SVO_slider_va_p1.pdf)
and are stored in `svo_choices.csv` file in a root directory. So if you 
would like to expand it for example to the full version (15 items), you 
just need to change the csv file.

The app consists of two pages: SVO itself and the Results page.
At the Results page the SVO angle is shown using Highcharts.

The corresponding SVO angle and type are stored in a `Player`'s model, in
fields `svo_angle` and `svo_type`.

 