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
}
TOPIC_CODE = {
    '001': u'AUDIT PLANNING AND CONTROL PROCEDURE',
    '002': u'FUNDAMENTALS AND PRINCIPLES OF AUDIT',
    '003': u'REGULATORY AND ETHICAL ISSUES',
    '004': u'INTERNAL AUDIT AND CONTROL',
    '005': u'APPLICATION OF INFORMATION TECHNOLOGY IN AUDITING',
    '006': u'INTRODUCTION TO PUBLIC SECTOR AUDIT',
    '007': u'AUDIT REPORT',
    '008': u'INTRODUCTION TO ASSURANCE',
    '009': u'VERIFICATION OF ASSETS AND LIABILITIES',
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
    def __init__(self):
        self.exam_codes = EXAM_CODE
        self.level_codes = LEVEL_CODE
        self.paper_codes = PAPER_CODE
        self.topic_codes = TOPIC_CODE
        self.decoded = {}

    def decode(self, code):
        """
        Tries to analyse a code and return a dictionary of the
        categorisations.
        Code *MUST* be 8 character unicode string.
        Whenever *ANY* failure occurs it returns an empty dictionary.
        """
        if isinstance(code, unicode) and len(code) == 8:
            self.decoded['exam'] = self.exam_codes.get(code[0], None)
            self.decoded['level'] = self.level_codes.get(code[1:3], None)
            self.decoded['paper'] = self.paper_codes.get(code[3:5], None)
            self.decoded['topic'] = self.topic_codes.get(code[5:8], None)

        if None in self.decoded.values():
            self.decoded = {}

        return self.decoded
        
    def translate_code(self, code, category):
        """
        Analyse code and return the category it represents.
        Returns `str`
        """
        decoded = self.decode(code)
        return decoded.get(category, 'FAILED')

    def get_category_code(self, code, category):
        relevant_code = ''

        if category == 'exam' and code[0] in self.exam_codes:
            relevant_code = code[0]
        elif category == 'level' and code[1:3] in self.level_codes:
            relevant_code = code[1:3]
        elif category == 'paper' and code[3:5] in self.paper_codes:
            relevant_code = code[3:5]
        elif category == 'topic' and code[5:8] in self.topic_codes:
            relevant_code = code[5:8]

        return relevant_code

    def translate_sub_code(self, code, category):
        translation = None
        
        if category == 'exam' and code in self.exam_codes:
            translation = self.exam_codes[code]
        elif category == 'level' and code in self.level_codes:
            translation = self.level_codes[code]
        elif category == 'paper' and code in self.paper_codes:
            translation = self.paper_codes[code]
        elif category == 'topic' and code in self.topic_codes:
            translation = self.topic_codes[code]

        return translation

    def get_code_list(self, code, code_list, category):
        """
        code: sub-code
        code_list: list of complete codes
        category: ['exam', 'level', 'paper', 'topic']

        Because exam code is at the beginning of the code and topic code
        is at the end of the complete code, exam and topic categories
        are not recommended here
        """
        import itertools
        iterator = None
        final_list = []
        
        if category == 'exam':
            iterator = itertools.ifilter(lambda x: x[0] == code, code_list)
        elif category == 'level':
            iterator = itertools.ifilter(lambda x: x[1:3] == code, code_list)
        elif category == 'paper':
            iterator = itertools.ifilter(lambda x:x[3:5] == code, code_list)
        elif category == 'topic':
            iterator = itertools.ifilter(lambda x:x[5:8] == code, code_list)

        final_list = list(iterator)

        return final_list


    def translate_to_code(self, topic_name, exam_name='ICAN',
                          level_name='Intermediate',
                          paper_name='Auditing and Assurance',
                          ):
        codes = []
        inverted_exam_codes = dict([[v,k] for k,v in self.exam_codes.items()])
        inverted_level_codes = dict([[v,k] for k,v in self.level_codes.items()])
        inverted_paper_codes = dict([[v,k] for k,v in self.paper_codes.items()])
        inverted_topic_codes = dict([[v,k] for k,v in self.topic_codes.items()])

        codes.append(inverted_exam_codes[exam_name])
        codes.append(inverted_level_codes[level_name])
        codes.append(inverted_paper_codes[paper_name])
        codes.append(inverted_topic_codes[topic_name])

        return ''.join(codes)