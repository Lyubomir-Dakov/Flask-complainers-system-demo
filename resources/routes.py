from resources.auth import RegisterComplainer, LoginComplainer
from resources.complaint import ComplaintListCreateResource

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (ComplaintListCreateResource, "/complaints")
)
