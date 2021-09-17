tmpl = {
    "@context": [
        "https://stuchalk.github.io/scidata/contexts/scidata.jsonld",
        {
            "sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#",
            "iao": "http://purl.obolibrary.org/obo/iao.owl",
            "chebi": "http://purl.obolibrary.org/obo/chebi.owl",
            "ncit": "http://purl.obolibrary.org/obo/ncit.owl",
            "ss": "https://semanticchemistry.github.io/semanticchemistry/ontology/cheminf.owl",
            "sio": "https://semanticscience.org/ontology/sio.owl",
            "atc": "https://purl.bioontology.org/ontology/ATC/",
            "w3i": "https://w3id.org/skgo/modsci#"
        },
        {"@base": "https://scidata.unf.edu/chalklab:gene:<chemblid>/"}
    ],
    "@id": "",
    "generatedAt": "<datetime>",
    "version": 1,
    "@graph": {
        "@id": "https://scidata.unf.edu/chalklab:gene:<chemblid>",
        "@type": "sdo:scidataFramework",
        "uid": "chalklab:gene:<chemblid>",
        "title": "Gene SciData JSON-LD for <chemblid>",
        "author": [
            {
                "@id": "author/1/",
                "@type": "dc:author",
                "name": "Stuart Chalk",
                "orcid": "0000-0002-0703-7776"
            }
        ],
        "description": "Metadata, identifiers and descriptors about a gene",
        "publisher": "Chalk Research Laboratory, University of North Florida",
        "version": "1.0",
        "keywords": ["gene"],
        "permalink": "https://scidata.unf.edu/chalklab:gene:<chemblid>",
        "toc": [
            "sdo:scientificData",
            "sdo:system",
            "sdo:gene",
            "dc:source",
            "dc:rights"
        ],
        "ids": [
            # "iao:IAO_0000578",
            # "ss:CHEMINF_000123",
            "ss:CHEMINF_000022",
            "ncit:NCIT_C1940",
            "chebi:CHEBI_25555",
            "sio:SIO_011118",
            "sio:SIO_010035",
        ],
        "scidata": {
            "@id": "scidata",
            "@type": "sdo:scientificData",
            "discipline": "w3i:Chemistry",
            "system": {
                "@id": "system/",
                "@type": "sdo:system",
                "facets": [
                    {
                        "@id": "targets/1/",
                        "@type": ["sio:SIO_010035", "ncit:NCIT_C17021"],
                        "name": "<prefname>",
                        # "identifiers": {
                        #     "@id": "identifier/",
                        #     "@type": "iao:IAO_0000578"
                        # },
                        # "descriptors": {
                        #     "@id": "descriptor/",
                        #     "@type": "ss:CHEMINF_000123"
                        # }
                    }
                ]
            }
        },
        "sources": [
            {
                "@id": "source/1/",
                "@type": "dc:source",
                "title": "UNF SciFlow System",
                "url": "https://sciflow.unf.edu"
            }
        ],
        "rights": [
            {
                "@id": "rights/1/",
                "@type": "dc:rights",
                "licensor": "University of North Florida",
                "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
            }
        ]
    }
}
