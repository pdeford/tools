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