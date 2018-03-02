from integration.ggrc.access_control.rbac_factories import audit, assessment, \
  assessment_template


def get_factory(model):
  factories = {
      "Audit": audit.AuditRBACFactory,
      "Assessment": assessment.AssessmentRBACFactory,
      "AssessmentTemplate": assessment_template.AssessmentTemplateRBACFactory,
  }
  return factories[model]
