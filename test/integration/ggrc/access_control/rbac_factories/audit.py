# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc.models import all_models, get_model
from integration.ggrc import Api, TestCase, generator
from integration.ggrc.models import factories


class AuditRBACFactory(object):
  def __init__(self, program_id, audit_id=None, user_id=None):
    self.api = Api()
    self.objgen = generator.ObjectGenerator()
    self.objgen.api = self.api
    self.program_id = program_id
    self.audit_id = audit_id

    if user_id:
      user = all_models.Person.query.get(user_id)
      self.api.set_user(user)

  def create(self):
    return self.api.post(all_models.Audit, {
        "audit": {
            "title": "New audit",
            "program": {"id": self.program_id},
            "context": None,
            "access_control_list": [],
        }
    })

  def read(self):
    return self.api.get_query(all_models.Audit, self.audit_id)

  def update(self):
    audit = all_models.Audit.query.get(self.audit_id)
    return self.api.put(audit, {"title": factories.random_str()})

  def delete(self):
    audit = all_models.Audit.query.get(self.audit_id)
    return self.api.delete(audit)

  def clone(self):
    return self.api.post(all_models.Audit, {
        "audit": {
            "program": {"id": self.program_id},
            "context": None,
            "operation": "clone",
            "cloneOptions": {
                "sourceObjectId": self.audit_id,
                "mappedObjects": "AssessmentTemplate"
            }
        }
    })

  def read_revisions(self):
    model_class = get_model("Audit")
    responses = []
    for query in ["source_type={}&source_id={}",
                  "destination_type={}&destination_id={}",
                  "resource_type={}&resource_id={}"]:
      responses.append(
          self.api.get_query(model_class, query.format("audit", self.audit_id))
      )
    return responses

  def map_snapshot(self):
    control = factories.ControlFactory()
    audit = all_models.Audit.query.get(self.audit_id)
    snapshot = TestCase._create_snapshots(audit, [control])[0]

    return self.objgen.generate_relationship(
        source=audit,
        destination=snapshot,
    )[0]

  def unmap_snapshot(self):
    pass

  def deprecate(self):
    audit = all_models.Audit.query.get(self.audit_id)
    return self.api.modify_object(audit, {
        "status": "Deprecated"
    })

  def archive(self):
    audit = all_models.Audit.query.get(self.audit_id)
    return self.api.modify_object(audit, {
        "archived": True
    })

  def unarchive(self):
    audit = all_models.Audit.query.get(self.audit_id)
    return self.api.modify_object(audit, {
        "archived": False
    })

  def map_issue(self):
    audit = all_models.Audit.query.get(self.audit_id)
    issue = factories.IssueFactory()

    return self.objgen.generate_relationship(
        source=audit,
        destination=issue
    )[0]
