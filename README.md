# tools
*General tools for general projects*

###pubmed_PMC_querier
[pubmed_PMC_querier](https://github.com/pdeford/tools/blob/master/pubmed_PMC_querier.py) is a tool that lets you query NCBI's PubMed database, take the resulting PMIDs, converts them to PMCIDs, and uses those to download the full text for all of the articles whose text is freely available. It also downloads the front matter (title, abstract, authors, etc.) for all available articles.

*Usage:*

    $ ~/tools/pubmed_PMC_querier.py outputFileBasename "your search query[&additional=options]"

*Example output:*

    $ ~/tools/pubmed_PMC_querier.py nonRed_enhancers  "human cis regulatory elements enhancers&mindate=2001"
    Querying PMC for 'human cis regulatory elements enhancers&mindate=2001'
    PMIDs: 317
    Converting PMIDs to PMCIDs
    PMCIDs: 127
    Downloading full text of articles. Minimum time = 0.7 minutes
    Full text retrieved for 59 articles
    
    real	1m3.847s
    user	0m0.695s
    sys 	0m0.975s

    $ ls
    nonRed_enhancers.articles.txt	parser_log
    
###seq_logos
[PWM_logo](https://github.com/pdeford/tools/blob/master/seq_logos/PWM_logo.py) is a module
for creating quick and dirty sequence logos for a given PWM.

*Usage:*

```
#!/usr/bin/env python

import PWM_logo

pwm = """0.00 4000.00  27.00 3887.00 3550.00 799.00 
0.00   0.00  29.00   0.00   4.00 681.00 
4000.00   0.00 109.00   6.00 383.00 2296.00 
0.00   0.00 3835.00 107.00  63.00 224.00"""

PWM_logo.main(pwm)
```

*Example output:*

![](https://github.com/pdeford/tools/blob/master/seq_logos/logo.png)

[gui](https://github.com/pdeford/tools/blob/master/seq_logos/gui.py) provides a quick GUI 
for generating these logos on the fly, outside of a python script.