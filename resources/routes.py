from resources.auth import RegisterComplainer, LoginComplainer
from resources.complaint import ComplaintListCreateResource, ComplaintApproveResource, ComplaintRejectResource

routes = (
    (RegisterComplainer, "/register"),
    (LoginComplainer, "/login"),
    (ComplaintListCreateResource, "/complaints"),
#     TODO URL for single complaint
    (ComplaintApproveResource, "/complaints/<int:pk>/approve"),
    (ComplaintRejectResource, "/complaints/<int:pk>/reject")
)
