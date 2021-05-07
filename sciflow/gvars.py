"""file to store global variables and initialize them"""

ingest_session = None
ingest_data_lookup_id = None
ingest_data_file_id = None
ingest_facet_file_id = None


def init():
    """initialize workflow system global variables"""
    global ingest_session
    ingest_session = None
    global ingest_data_lookup_id
    ingest_data_lookup_id = None
    global ingest_data_file_id
    ingest_data_file_id = None
    global ingest_facet_file_id
    ingest_facet_file_id = None
