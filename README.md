# Social value orientation measure
## (Murphy, Ackermann,  Handgraaf, 2011)

This is a prototype of Social value orientation measure in oTree.

It uses a set of Dictator-like decisions, that defines the measure of 
prosociality of the subject. Please, read more at the author's (Ryan Murphy) 
page [here](http://vlab.ethz.ch/styled-2/index.html).


The specific values of SVO are taken from [SVO file](http://ryanomurphy.com/styled-2/downloads/files/SVO_slider_va_p1.pdf)
and are stored in `svo_choices.csv` file in a root directory. 

The app consists of two pages: SVO itself and the Results page.
At the Results page the SVO angle is shown using Highcharts.

The corresponding SVO angle and type are stored in a `Player`'s model, in
fields `svo_angle` and `svo_type`.

The answers for specific items are stored in a separate model `SVO` linked to 
each particular player. The answers are dumped to Player's model (for export) to a field `dump_answer` as a list
of triplets:

(*item id*, *ego value*, *alter value*),

where ego value is the decision '_You receive_' and alter value is the decision '_Other receives_' for each 
individual SVO item. *item id* is a number as they are listed in Murphy et al. paper. 

The order in which the items are shown is randomized by default. You can change that in settings. An example of
settings:

```python
    {
        'name': 'svofull',
        'display_name': 'SVO Measure. Full version (15 items)',
        'num_demo_participants': 1,
        'app_sequence': ['svo'],
        'random_order': True,
        'secondary': True,
    }
```

* `random_order` defines randomization. The order in which it is shown is `SVO.showing_order` field. Default: _random_

* `secondary` defines whether the full (15 items) or primary version of SVO will be shown. Default: _primary_ 


 