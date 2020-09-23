if "x" == "y":

    """
    Backend Scheme
    1) Load JSON-LD (workflow.ingestion)
    2) Check if compound is already present in SQL DB (substances.*)
    ) Scrape for compound data (substances.sources)
    ) Add compound to SQL DB (substances.*)
    ) Check if compound is already present in GraphDB and add if not
    ) Process JSON-LD to add links to GraphDB (workflow.graph_link)
    )
    ) Add JSON-LD to GraphDB (workflow.graphdb)
    
    Frontend Scheme
    ) Views
    ) Manually add compounds
    ) 
    """

# crosswalks

# datasets
    from datasets.mysql import *
    getdatasetnames
    getsourcecodes
    getcodesnames

# substances
    from substances.functions import *
    addsubstance
    getidtype
    getsubdata
    pubchemkey
    createsubjld
    get_item
    get_items
    saveids
    savedescs

    from substances.mysql import *
    getsubid
    ingraph
    getinchikey
    addsubgraphname
    updatesubstancefield
    clearsubstancefield
    addidentifier
    createsubstance
    subsearch

    from substances.sources import *
    pubchem
    classyfire
    wikidata
    chembl
    pubchemsyns

# users
    from users.requests import *
    makerequest
    rejectrequest
    approverequest

# workflow
    from workflow.graph_link import *
    Post
    GraphLinkA
    GraphLinkB

    from workflow.graphdb import *
    addgraph
    isgraph
    getgraphname
    graphadd
    graphsize
    graphdownload
    graphrepos
    graphcontexts
    graphstatementsget
    graphstatementedit
    graphqueryrun
    graphqueryget
    graphqueryedit
    graphquerycreate
    graphquerydelete
    graphnamespaceget
    graphnamespacecreate

    from workflow.ingestion import *
    getfiles
    ingest
    finalize
    autoingest
    wait

    from workflow.logwriter import *
    errloginit
    actloginit
    logwrite
    logprint

    from workflow.normalization import *
    normalize
    findsub
    getfacet
    findprofile
    getprofile
    makeprofile
    addprofile
    normalizationcheck

    from workflow.updatedb import *
    updatedb
    updategraphdb
    updatemysql

    from workflow.utils import *
    file2sds
    movesdsfile

    from workflow.validation import *
    validate
    check_scidata
    check_type
