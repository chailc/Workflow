from database import Base
from sqlalchemy_utils import EmailType
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid


class WorkflowRoles(Base):
    __tablename__ = 'workflowroles'

    role_id = Column(String, primary_key=True)
    rolename = Column(String, unique=True)
    description = Column(String)
    status = Column(Boolean, default = False)
    type = Column(String)
    min_users = Column(Integer, default=0)
    max_users = Column(Integer, default=0)
    current_users = Column(Integer, default=0)
    created_at = Column(DateTime)
    created_by = Column(String)
    modified_at = Column(DateTime)
    modified_by = Column(String)


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(String, primary_key = True)
    role_id = Column(String, ForeignKey("workflowroles.role_id"))
    stage = Column(Integer)
    last_stage = Column(Boolean)
    sla_type = Column(String)
    sla_days = Column(Integer)
    previous_stage = Column(String, ForeignKey("workflow.id"))
    next_stage = Column(String, ForeignKey("workflow.id"))
    created_at = Column(DateTime)
    created_by = Column(String)
    modified_at = Column(DateTime)
    modified_by = Column(String)


class RolePermissions(Base):
    __tablename__ = "role_permissions"

    id = Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    role_id = Column(String, ForeignKey("workflowroles.role_id"))
    permissions = Column(String, ForeignKey("permissions.permission_id"))
    is_true = Column(Boolean)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    last_modified_on = Column(DateTime)


class Permissions(Base):
    __tablename__ = "permissions"

    permission_id = Column(String, primary_key=True)
    module = Column(String)
    submodule = Column(String)
    action = Column(String)


class WorkflowAssignments(Base):
    __tablename__ = "category_workflow"

    id = Column(String, primary_key = True)
    attribute_id = Column(String, ForeignKey("attributes.id"))
    attribute_group_id = Column(String, primary_key = True)
    reference_master_id = Column(String, primary_key = True)
    category_id = Column(String, primary_key = True)
    workflow_id = Column(String), ForeignKey("workflow.id")


class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    role_id = Column(String)
    user_id = Column(String)
    group_id = Column(String)


class UserGroups(Base):
    __tablename__ = 'user_groups'

    user_id = Column(String, primary_key = True)
    group_id = Column(String, primary_key = True)


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(String, primary_key = True)
    group_name = Column(String)


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(EmailType)
    status = Column(Boolean, default=False)


class UserAttributes(Base):
    __tablename__ = 'user_attributegroup'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey('users.id'))
    attribute_id = Column(String)
    attribute_group_id = Column(String)


class AttributeGroup(Base):
    __tablename__ = 'attribute_groups'

    id = Column(String, primary_key = True)
    attribute_group_name = Column(String)


class Attributes(Base):
    __tablename__ = 'attributes'

    id = Column(String, primary_key = True)
    attribute_name = Column(String)
    attribute_group_id = Column(String)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(String, primary_key = True)
    category_name = Column(String)


class Requests(Base):
    __tablename__ = 'requests'

    id = Column(String, primary_key = True)
    requested_on = Column(DateTime)
    requested_by = Column(String)
    requester_role = Column(String)
    attribute_id = Column(String)
    attribute_group_id = Column(String)
    reference_master_id = Column(String)
    category_id = Column(String)
    workflow_id = Column(String), ForeignKey("workflow.id")
    sku_id = Column(String)
    request_status = Column(String)
    last_modified_on = Column(DateTime(timezone=True))


class RequestWorkflow(Base):
    __tablename__ = 'request_workflow'

    id = Column(String, primary_key = True)
    request_id = Column(String, ForeignKey("requests.id"))
    workflow_id = Column(String), ForeignKey("workflow.id")
    workflow_stage = Column(String), ForeignKey("workflow.stage")
    last_stage = Column(Boolean)
    user_group_id = Column(String)
    current_user_id = Column(String)
    user_role_type = Column(String)
    comment = Column(String)
    task_accepted_on = Column(DateTime) 
    sla_end_on = Column(DateTime)
    status = Column(String, ForeignKey("status.type"))


class Status(Base):
    __tablename__ = 'status'

    type = Column(String, primary_key = True)




