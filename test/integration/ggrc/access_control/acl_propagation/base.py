# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control roles propagation base class"""
from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.models import factories
from integration.ggrc_basic_permissions.models \
    import factories as rbac_factories


class TestACLPropagation(TestCase):
  """TestACLPropagation base class with batch of helper methods"""

  GLOBAL_ROLES = ["Creator", "Reader", "Editor", "Administrator"]

  STATUS_SUCCESS = [200, 201]
  STATUS_FORBIDDEN = [403,]

  def setup_people(self):
    """Setup people with global roles"""
    roles_query = all_models.Role.query.filter(
        all_models.Role.name.in_(self.GLOBAL_ROLES)
    )
    global_roles = {role.name: role for role in roles_query}

    self.people = {}
    with factories.single_commit():
      for role_name in self.GLOBAL_ROLES:
        user = factories.PersonFactory()
        self.people[role_name] = user
        rbac_factories.UserRoleFactory(
            role=global_roles[role_name],
            person=user
        )

  def assert_result(self, responses, expected_res):
    exp_status = self.STATUS_SUCCESS if expected_res else self.STATUS_FORBIDDEN
    if not isinstance(responses, list):
      responses = [responses]
    for response in responses:
      self.assertIn(
          response.status_code,
          exp_status,
          "Response for current operation has wrong status.{} expected, "
          "{} received".format(str(exp_status), response.status_code)
      )
