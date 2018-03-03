import ddt

from ggrc.models import all_models
from integration.ggrc import Api
from integration.ggrc.access_control import rbac_factories
from integration.ggrc.access_control.acl_propagation import base
from integration.ggrc.models import factories
from integration.ggrc.utils import helpers


@ddt.ddt
class TestAuditorsPropagation(base.TestACLPropagation):
  """Test Auditor role permissions propagation"""

  PERMISSIONS = {
      "Creator": {
          "Audit": {
              "create": False,
              "read": True,
              "update": False,
              "delete": False,
              "clone": False,
              "read_revisions": True,
              "map_snapshot": False,
          },
          "Assessment": {
              "create": True,
              "generate": True,
              "read": True,
              "update": False,
              "delete": False,
              "read_revisions": True,
              "map_snapshot": False,
          },
          "AssessmentTemplate": {
              "create": False,
              "read": True,
              "update": False,
              "delete": False,
              "read_revisions": True,
          }
      },
      "Reader": {
          "Audit": {
              "create": False,
              "read": True,
              "update": False,
              "delete": False,
              "clone": False,
              "read_revisions": True,
              "map_snapshot": False,
          },
          "Assessment": {
              "create": True,
              "generate": True,
              "read": True,
              "update": False,
              "delete": False,
              "map_snapshot": False,
          },
          "AssessmentTemplate": {
              "create": False,
              "read": True,
              "update": False,
              "delete": False,
              "read_revisions": True,
          }
      },
      "Editor": {
          "Audit": {
              "create": True,
              "read": True,
              "update": True,
              "delete": True,
              "clone": True,
              "read_revisions": True,
              "map_snapshot": True,
          },
          "Assessment": {
              "create": True,
              "generate": True,
              "read": True,
              "update": True,
              "delete": True,
              "map_snapshot": True,
          },
          "AssessmentTemplate": {
              "create": True,
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
          }
      },
  }

  def setUp(self):
    super(TestAuditorsPropagation, self).setUp()
    self.auditor_acr = all_models.AccessControlRole.query.filter_by(
        name="Auditors"
    ).first()
    self.api = Api()
    self.setup_people()

  def init_factory(self, role, model):
    with factories.single_commit():
      program_id = factories.ProgramFactory().id
      audit_id = factories.AuditFactory(
        program_id=program_id,
        access_control_list=[{
          "ac_role": self.auditor_acr,
          "person": self.people[role],
        }]
      ).id

    rbac_factory = None
    if model == "Audit":
      rbac_factory = rbac_factories.get_factory(model)(
        program_id, audit_id, self.people[role].id
      )
    elif model == "Assessment":
      assessment_id = factories.AssessmentFactory(audit_id=audit_id).id
      rbac_factory = rbac_factories.get_factory(model)(
        audit_id, assessment_id, self.people[role].id
      )
    elif model == "AssessmentTemplate":
      template_id = factories.AssessmentTemplateFactory(audit_id=audit_id).id
      rbac_factory = rbac_factories.get_factory(model)(
        audit_id, template_id, self.people[role].id
      )
    return rbac_factory

  @helpers.unwrap(PERMISSIONS)
  def test_CRUD(self, role, model, action_name, expected_result):
    """Test {2} for {1} under Auditor {0}"""
    rbac_factory = self.init_factory(role, model)
    if not rbac_factory:
      raise Exception("There is no factory for model '{}'".format(model))

    action = getattr(rbac_factory, action_name, None)
    if not action:
      raise NotImplementedError(
          "Action {} is not implemented for this test.".format(action_name)
      )
    self.assert_result(action(), expected_result)
