def clean(s):
    '''removes null bytes from a string

    Attributes:
        - s: a string
    '''
    return s.replace('\0', '') if type(s) is str else s


def get_field(record, field):
    '''Get field from record

    Attributes:
        - record: a Shodan stream record
        - field: a field in the record
    '''
    return clean(record.get(field))


class WrappedSession:
    '''Wrap a SQLAlchemy session'''

    def __init__(self, session, stream_id=None):
        '''session: SQLAlchemy session'''
        self.session = session
        self.stream_id = stream_id

    def safe_commit(self):
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            return False
