from _config._config import *
import importlib as lib

sts = lib.import_module(CH_STREAMLIT_IMPORT)
report_thread = lib.import_module(CH_STREAMLIT_REPORTTHREAD)
server = lib.import_module(CH_STREAMLIT_SERVER)

class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": None,
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)

#@st.cache(allow_output_mutation=True)
def _get_session():
    session_id = report_thread.get_report_ctx().session_id
    
    print("*****", session_id, "*****")
    
    session_info = server.Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)
        
    return session._custom_session_state

@sts.cache(hash_funcs={ _SessionState: id})
def get_state(hash_funcs=None):
    return _get_state(hash_funcs=hash_funcs)

#global session functions
def save_global_session_objet(session, key, values):
   session[key] = values
    
def get_global_session_objet(session, key):
    try: return session[key]
    except:return None
    
def del_global_session_objet(session, key):
    save_global_session_objet(session=session, key=key, values=None)