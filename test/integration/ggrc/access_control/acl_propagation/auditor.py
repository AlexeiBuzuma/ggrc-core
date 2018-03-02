import ddt

from ggrc.models import all_models
from integration.ggrc import Api
from integration.ggrc.access_control.acl_propagation import base
from integration.ggrc.models import factories
from integration.ggrc.utils import helpers


@ddt.ddt
class TestAuditorPropagation(base.TestAuditACLPropagation):
  """Test Auditor role permissions propagation"""

  PERMISSIONS = {
      "Creator": {
          "Audit": {
              "create_audit": False,
              "read": True,
              "update": False,
              "delete": False,
              "clone": False,
              "read_revisions": True,
              "map_snapshot": False,
          },
          "Assessment": {
              "create_assessment": True,
              "generate": True,
              "read": True,
              "update": False,
              "delete": False,
              "map_snapshot": False,
          },
          "Assessment Template": {
              "create_assessment_template": False,
          }
      },
      "Reader": {
          "Audit": {
              "create_audit": False,
              "read": True,
              "update": False,
              "delete": False,
              "clone": False,
              "read_revisions": True,
              "map_snapshot": False,
          },
          "Assessment": {
              "create_assessment": True,
              "generate": True,
              "read": True,
              "update": False,
              "delete": False,
              "map_snapshot": False,
          },
          "Assessment Template": {
              "create_assessment_template": False,
          }
      },
      "Editor": {
          "Audit": {
              "create_audit": True,
              "read": True,
              "update": True,
              "delete": True,
              "clone": True,
              "read_revisions": True,
              "map_snapshot": True,
          },
          "Assessment": {
              "create_assessment": True,
              "generate": True,
              "read": True,
              "update": True,
              "delete": True,
              "map_snapshot": True,
          },
          "Assessment Template": {
              "create_assessment_template": True,
          }
      },
  }

  def setUp(self):
    super(TestAuditorPropagation, self).setUp()
    self.auditor_acr = all_models.AccessControlRole.query.filter_by(
        name="Auditors"
    ).first()
    self.api = Api()
    self.setup_people()

  def setup_base_objects(self, global_role):
    with factories.single_commit():
      if global_role is not None:
        person = self.get_user_object(global_role)
      else:
        person = self.get_user_object("Administrator")

      self.program_id = factories.ProgramFactory().id
      self.audit = factories.AuditFactory(
          program_id=self.program_id,
          access_control_list=[{
              "ac_role": self.auditor_acr,
              "person": person,
          }]
      )
      self.audit_id = self.audit.id
      self.control = factories.ControlFactory()
      self.template_id = factories.AssessmentTemplateFactory(
          audit=self.audit,
      ).id
      self.assessment_id = factories.AssessmentFactory(audit=self.audit).id

  @helpers.unwrap(PERMISSIONS)
  def test_CRUD(self, role, model, action_str, expected_result):
    """Test {2} for {1} under Auditor {0}"""
    self.runtest(role, model, action_str, expected_result)
