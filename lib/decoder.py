__author__ = 'tunde'

# Constants for ExamCodeDecoder class.
# When there needs to be a change in any of the exam categorisation, it
# should be done here not in the ExamCodeDecoder class
########################################################################

EXAM_CODE = {'1': u'ICAN'}
LEVEL_CODE = {
    '01': u'Intermediate'
}
PAPER_CODE = {
    '01': u'Auditing and Assurance',
    '02': u'Business Communications and Research Methods',
    '03': u'Taxation',
    '04': u'Costing and Quantitative Techniques'
}
TOPIC_CODE = {
    '001': u'AUDIT PLANNING AND CONTROL PROCEDURE',
    '002': u'FUNDAMENTALS AND PRINCIPLES OF AUDIT',
    '003': u'REGULATORY AND ETHICAL ISSUES',
    '004': u'INTERNAL AUDIT AND CONTROL',
    '005': u'APPLICATION OF INFORMATION TECHNOLOGY IN AUDITING',
    '006': u'INTRODUCTION TO PUBLIC SECTOR AUDIT',
    '007': u'AUDIT REPORTING',
    '008': u'INTRODUCTION TO ASSURANCE',
    '009': u'VERIFICATION OF ASSETS AND LIABILITIES',
    '010': u'COMMUNICATION AND LANGUAGE',
    '011': u'CONCEPTS OF LANGUAGE AND COMMUNICATION',
    '012': u'COMMUNICATION SKILLS',
    '013': u'REPORT WRITING - COMMUNICATION PERSPECTIVES',
    '014': u'NATURE AND TYPES OF RESEARCH',
    '015': u'PROBLEM IDENTIFICATION',
    '016': u'LITERATURE REVIEW',
    '017': u'RESEARCH DESIGN, POPULATION AND SAMPLING PROCEDURE',
    '018': u'DATA COLLECTION - QUESTIONNAIRE AND MEASUREMENT SCALES',
    '019': u'VALIDATION OF RESEARCH INSTRUMENT AND PROCESS',
    '020': u'INTRODUCTION TO RESEARCH STATISTICAL ANALYSIS',
    '021': u'STATISTICAL ANALYSIS AND PRESENTATION I',
    '022': u'STATISTICAL ANALYSIS AND PRESENTATION II',
    '023': u'STATISTICAL ANALYSIS AND PRESENTATION III',
    '024': u'THE USE OF INFORMATION TECHNOLOGY (IT) IN RESEARCH ANALYSIS',
    '025': u'THE RESEARCH REPORT',
    '026': u'EVALUATION PROCEDURES',
    '027': u'INTRODUCTION TO NIGERIAN TAX SYSTEM',
    '028': u'ADMINISTRATION OF TAXES',
    '029': u'DETERMINATION OF RESIDENCE AND INCOMES CHARGEABLE',
    '030': u'TAXATION OF EMPLOYMENT INCOME',
    '031': u'RELIEFS AND ALLOWANCES',
    '032': u'RETIREMENT BENEFITS SCHEME',
    '033': u'SETTLEMENTS, TRUSTS AND ESTATES',
    '034': u'NATURE OF COMPANIES INCOME TAX',
    '035': u'ASCERTAINMENT OF COMPANIES  PROFITS/LOSSES',
    '036': u'ASCERTAINMENT OF ASSESSABLE PROFIT/TOTAL PROFIT',
    '037': u'CAPITAL ALLOWANCE',
    '038': u'LOSS RELIEF',
    '039': u'COMPUTATION OF COMPANIES INCOME TAX',
    '040': u'EDUCATION TAX',
    '041': u'TAXATION OF SPECIALISED COMPANIES',
    '042': u'ACCOUNTING FOR TAXES',
    '043': u'RETURNS, ASSESSMENTS AND COLLECTION PROCEDURES',
    '044': u'OBJECTIONS AND APPEAL PROCEDURES',
    '045': u'VALUE ADDED TAX',
    '046': u'STAMP DUTIES',
    '047': u'WITHHOLDING TAX',
    '048': u'COMPUTER ASSISTED TAX PLANNING AND MANAGEMENT',
    '049': u'INTRODUCTION TO COST ACCOUNTING',
    '050': u'MATERIAL ACCOUNTING AND CONTROL',
    '051': u'LABOUR ACCOUNTING AND AND CONTROL',
    '052': u'OVERHEAD COST ACCOUNTING AND CONTROL',
    '053': u'COST ANALYSIS',
    '054': u'COST METHODS',
    '055': u'PROCESS COST AND PRODUCT COSTING',
    '056': u'BUDGETING AND BUDGETARY',
    '057': u'STANDARD COSTING',
    '058': u'COST DATA FOR SHORT RUN TACTICAL DECISION MAKING',
    '059': u'COST CONTROL',
    '060': u'COST LEDGER ACCOUNTS',
    '061': u'THEORY OF INDEX NUMBERS',
    '062': u'BASIC PROBABILITY CONCEPTS',
    '063': u'SET THEORY',
    '064': u'INTRODUCTION TO MATRICES',
    '065': u'BASIC CONCEPTS OF DIFFERENTIATION',
    '066': u'BASIC LINEAR PROGRAMMING',
    '067': u'NETWORK ANALYSIS',
    '068': u'REPLACEMENT ANALYSIS',
    '069': u'TRANSPORTATION MODEL',
    '070': u'COMPUTER ASSISTED COSTING TECHNIQUES',
}

########################################################################

class ExamCodeDecoder:
    """
    This is a class that decodes exam codes and returns the
    categorisation for that code. It is meant to be used with Question
    objects.

    The codes are 8 character codes.

    This is how the code is analysed:
    *   The first digit represents the EXAM e.g ICAN. Only numerals are
        allowed.
    *   The next two digits represent the LEVEL e.g Foundation,
        Intermediate. Only numerals are allowed
    *   The next two digits represent the PAPER e.g Auditing and Assurance.
        It is alphanumeric.
    *   The next three digits represent the TOPIC. It is alphanumeric

    The decoder uses this information to determine what EXAM, LEVEL,
    PAPER and TOPIC.
    """
    def __init__(self, exam_codes=EXAM_CODE, level_codes=LEVEL_CODE, paper_codes=PAPER_CODE, topic_codes=TOPIC_CODE,
                 exam_code_key='exam', paper_code_key='paper', level_code_key='level', topic_code_key='topic'):
        self.exam_codes = exam_codes
        self.level_codes = level_codes
        self.paper_codes = paper_codes
        self.topic_codes = topic_codes
        self.exam_code_key = exam_code_key
        self.level_code_key = level_code_key
        self.paper_code_key = paper_code_key
        self.topic_code_key = topic_code_key

        #TODO: self.decoded should be static!
        self.decoded = {}

    def _decode(self, code):
        """
        Tries to analyse a code and return a dictionary of the
        categorisations.
        Code *MUST* be 8 character unicode string.
        Whenever *ANY* failure occurs it returns an empty dictionary.

        >>> decoder = ExamCodeDecoder()
        >>> decoder._decode('AA')
        {}
        >>> decoder._decode('aAaAaAaA')
        {}
        >>> decoder._decode(00000000)
        {}
        >>> decoder._decode(10101011)
        {}
        >>> decoder._decode('10102013')
        {}
        >>> code = decoder._decode(u'10103038')
        >>> code == {'paper': u'Taxation', 'topic': u'LOSS RELIEF', 'exam': u'ICAN', 'level': u'Intermediate'}
        True

        """
        if isinstance(code, unicode) and len(code) == 8:
            self.decoded[self.exam_code_key] = self.exam_codes.get(code[0], None)
            self.decoded[self.level_code_key] = self.level_codes.get(code[1:3], None)
            self.decoded[self.paper_code_key] = self.paper_codes.get(code[3:5], None)
            self.decoded[self.topic_code_key] = self.topic_codes.get(code[5:8], None)

        if None in self.decoded.values():
            self.decoded = {}

        return self.decoded
        
    def code_to_text(self, code, key):
        """
        Consumes a code and return the categorisation of the code.

        key argument should be the same as one of exam_code_key, level_code_key, paper_code_key or topic_code_key (case
         sensitive)

        >>> decoder = ExamCodeDecoder()
        >>> decoder.code_to_text('1', 'exam')
        'FAILED'
        >>> decoder.code_to_text('10103038', 'exam')
        'FAILED'
        >>> decoder.code_to_text(u'10103038', 'level')
        u'Intermediate'
        >>> decoder.code_to_text('10103038', 'foo')
        'FAILED'

        """
        decoded = self._decode(code)
        return decoded.get(key, 'FAILED')

    def text_to_sub_code(self, code, category):
        """
        use this to determine the code for the category supplied as argument. category must be the same as exam_code_key
        , level_code_key, paper_code_key or topic_code_key otherwise it returns an empty string

        >>> decoder = ExamCodeDecoder()
        >>> decoder.text_to_sub_code(u'AaA', u'exam')
        ''
        >>> decoder.text_to_sub_code(u'10103038', u'exam')
        u'1'
        >>> decoder.text_to_sub_code(u'10103038', u'nothing')
        ''

        """
        relevant_code = ''

        if category == self.exam_code_key and code[0] in self.exam_codes:
            relevant_code = code[0]
        elif category == self.level_code_key and code[1:3] in self.level_codes:
            relevant_code = code[1:3]
        elif category == self.paper_code_key and code[3:5] in self.paper_codes:
            relevant_code = code[3:5]
        elif category == self.topic_code_key and code[5:8] in self.topic_codes:
            relevant_code = code[5:8]

        return relevant_code

    def sub_code_to_text(self, code, category):
        """
        Use this to convert a sub code into what it represents. It returns None if it fails

        >>> decoder = ExamCodeDecoder()
        >>> decoder.sub_code_to_text(u'1', u'exam')
        u'ICAN'
        >>> decoder.sub_code_to_text(u'038', u'topic')
        u'LOSS RELIEF'
        >>> decoder.sub_code_to_text(u'038', u'magic')

        """
        translation = None
        
        if category == self.exam_code_key and code in self.exam_codes:
            translation = self.exam_codes[code]
        elif category == self.level_code_key and code in self.level_codes:
            translation = self.level_codes[code]
        elif category == self.paper_code_key and code in self.paper_codes:
            translation = self.paper_codes[code]
        elif category == self.topic_code_key and code in self.topic_codes:
            translation = self.topic_codes[code]

        return translation

    def filter_code_list_by_sub_code(self, sub_code, code_list, key):
        """
        Use this to filter a list of codes by those that contain the given `sub_code`. The `key` should be one of
        self.exam_code_key, self.level_code_key, self.paper_code_key or self.topic_code_key

        >>> decoder = ExamCodeDecoder()
        >>> list1 = [u'10103038']
        >>> decoder.filter_code_list_by_sub_code(u'038', list1, u'topic')
        [u'10103038']
        >>> list2 = [u'10103038', u'10103039']
        >>> decoder.filter_code_list_by_sub_code(u'038', list2, u'topic')
        [u'10103038']
        >>> decoder.filter_code_list_by_sub_code(u'038', [], u'topic')
        []
        >>> decoder.filter_code_list_by_sub_code(u'038', [u'10103039'], u'topic')
        []

        """
        import itertools
        iterator = None
        final_list = []
        
        if key == self.exam_code_key:
            iterator = itertools.ifilter(lambda x: x[0] == sub_code, code_list)
        elif key == self.level_code_key:
            iterator = itertools.ifilter(lambda x: x[1:3] == sub_code, code_list)
        elif key == self.paper_code_key:
            iterator = itertools.ifilter(lambda x:x[3:5] == sub_code, code_list)
        elif key == self.topic_code_key:
            iterator = itertools.ifilter(lambda x:x[5:8] == sub_code, code_list)

        final_list = list(iterator)

        return final_list


    def get_code(self, topic_name, exam_name='ICAN', level_name='Intermediate',
                          paper_name='Auditing and Assurance'):
        """
        Supply the name of a topic, exam, level, paper  and it will return its code (not sub-code)

        >>> decoder = ExamCodeDecoder()
        >>> decoder.get_code(u'LOSS RELIEF', paper_name=u'Taxation')
        u'10103038'

        """
        codes = []
        inverted_exam_codes = dict([[v, k] for k, v in self.exam_codes.items()])
        inverted_level_codes = dict([[v ,k] for k, v in self.level_codes.items()])
        inverted_paper_codes = dict([[v, k] for k, v in self.paper_codes.items()])
        inverted_topic_codes = dict([[v, k] for k, v in self.topic_codes.items()])

        codes.append(inverted_exam_codes[exam_name])
        codes.append(inverted_level_codes[level_name])
        codes.append(inverted_paper_codes[paper_name])
        codes.append(inverted_topic_codes[topic_name])

        return u''.join(codes)

if __name__ == "__main__":
    import doctest
    doctest.testmod()