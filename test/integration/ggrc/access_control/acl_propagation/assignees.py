# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control roles Assignees propagation"""

import ddt

from ggrc.models import all_models
from integration.ggrc import Api
from integration.ggrc.access_control import rbac_factories
from integration.ggrc.access_control.acl_propagation import base
from integration.ggrc.models import factories
from integration.ggrc.utils import helpers


@ddt.ddt
class TestAssigneesPropagation(base.TestACLPropagation):
  """Test Assignees role permissions propagation"""

  PERMISSIONS = {
      "Creator": {
          "Assessment": {
              "read": True,
              "update": True,
              "delete": False,
              "map_snapshot": False,
              "read_revisions": True,
          },
      },
      "Reader": {
          "Assessment": {
              "read": True,
              "update": True,
              "delete": False,
              "map_snapshot": False,
              "read_revisions": True,
          },
      },
      "Editor": {
          "Assessment": {
              "read": True,
              "update": True,
              "delete": True,
              "map_snapshot": True,
              "read_revisions": True,
          },
      },
  }

  def setUp(self):
    super(TestAssigneesPropagation, self).setUp()
    self.api = Api()
    self.assignees_acr = all_models.AccessControlRole.query.filter_by(
        name="Assignees"
    ).first()
    self.setup_people()

  def init_factory(self, role, model):
    with factories.single_commit():
      audit_id = factories.AuditFactory().id
      assessment_id = factories.AssessmentFactory(
        audit_id=audit_id,
        access_control_list=[{
          "ac_role": self.assignees_acr,
          "person": self.people[role]
        }]
      ).id
    rbac_factory = rbac_factories.get_factory(model)(
      audit_id, assessment_id, self.people[role].id
    )
    return rbac_factory

  @helpers.unwrap(PERMISSIONS)
  def test_CRUD(self, role, model, action_name, expected_result):
    """Test {2} for {1} under Assignee {0}"""
    rbac_factory = self.init_factory(role, model)
    if not rbac_factory:
      raise Exception("There is no factory for model '{}'".format(model))

    action = getattr(rbac_factory, action_name, None)
    if not action:
      raise NotImplementedError(
          "Action {} is not implemented for this test.".format(action_name)
      )
    self.assert_result(action(), expected_result)
