# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from integration.ggrc.access_control.rbac_factories import audit, assessment, \
  assessment_template


def get_factory(model):
  factories = {
      "Audit": audit.AuditRBACFactory,
      "Assessment": assessment.AssessmentRBACFactory,
      "AssessmentTemplate": assessment_template.AssessmentTemplateRBACFactory,
  }
  return factories[model]
