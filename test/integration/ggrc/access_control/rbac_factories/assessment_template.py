# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc.models import all_models, get_model
from integration.ggrc import Api, generator
from integration.ggrc.models import factories


class AssessmentTemplateRBACFactory(object):
  def __init__(self, audit_id, template_id, user_id):
    self.api = Api()
    self.objgen = generator.ObjectGenerator()
    self.objgen.api = self.api
    self.audit_id = audit_id
    self.template_id = template_id

    user = all_models.Person.query.get(user_id)
    self.api.set_user(user)
    self.default_assignees = "Admin"
    self.default_verifiers = "Admin"

  def create(self):
    return self.api.post(all_models.AssessmentTemplate, {
        "assessment_template": {
            "audit": {"id": self.audit_id},
            "context": None,
            "default_people": {
                "assignees": self.default_assignees,
                "verifiers": self.default_verifiers,
            },
            "title": "New Assessment Template"
          }
    })

  def read(self):
    return self.api.get_query(all_models.AssessmentTemplate, self.template_id)

  def update(self):
    template = all_models.AssessmentTemplate.query.get(self.template_id)
    return self.api.put(template, {"title": factories.random_str()})

  def delete(self):
    template = all_models.AssessmentTemplate.query.get(self.template_id)
    return self.api.delete(template)

  def read_revisions(self):
    model_class = get_model("AssessmentTemplate")
    responses = []
    for query in ["source_type={}&source_id={}",
                  "destination_type={}&destination_id={}",
                  "resource_type={}&resource_id={}"]:
      responses.append(
          self.api.get_query(
              model_class,
              query.format("assessment_template", self.template_id)
          )
      )
    return responses
