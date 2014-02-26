class SessionMixin(object):
    """
    This is a mixin for class based views. It provides methods to save objects
    to the session or retrieve objects from the session
    """
    def get_session_var(self, session_key):
        return self.request.session.get(session_key)
        
    def set_session_var(self, session_key, obj):
        self.request.session[session_key] = obj
        
    def remove_session_var(self, session_key):
        for key in session_key:
            if self.get_session_var(key):
                del self.request.session[key]

    def init_session_vars(self, to_remove, key_to_set):
        self.remove_session_var(to_remove)
        self.set_session_var(key_to_set, True)

    def set_next_question_url_params(self, **kwargs):
        for key in kwargs:
            self.set_session_var(key, kwargs[key])
