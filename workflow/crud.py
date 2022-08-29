import workflow_pb2
from sqlalchemy.orm import Session
import model
import check
import time
from datetime import datetime

"""
Function to create role
"""


def create_role(db: Session, request: workflow_pb2.Role):
    check_role = check.check_if_role_exists(db, request.roledetails.roleid)
    if check_role:
        return "Role already exists"

    role = model.WorkflowRoles(
        role_id=request.roledetails.roleid,
        rolename=request.roledetails.rolename,
        description=request.roledetails.desc,
        status=request.roledetails.status,
        type=request.roledetails.roletype,
        created_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        created_by=request.createdby,
        modified_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        modified_by=request.modifiedby
    )
    try:
        db.add(role)
        db.commit()
        db.refresh(role)
        return "Role created"
    except Exception as e:
        db.rollback()
        return e


def update_role(db: Session, request: workflow_pb2.Role):
    check_role = check.check_if_role_exists(db, request.roledetails.roleid)
    if not check_role:
        return "Role does not exist"
    role = model.WorkflowRoles(
        rolename=request.roledetails.rolename,
        description=request.roledetails.desc,
        status=request.roledetails.status,
        type=request.roledetails.roletype,
        modified_at=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        modified_by=request.modifiedby
    )
    temp = dict(role.__dict__)
    temp.pop("_sa_instance_state", None)
    try:
        db.query(model.WorkflowRoles).filter(model.WorkflowRoles.role_id == request.roledetails.roleid).update(temp)
        db.commit()
        return "Role Updated Successfully"
    except Exception as e:
        db.rollback()
        return "Exception:", e


def get_role_details(db: Session, request: workflow_pb2.RoleId):
    check_role = check.check_if_role_exists(db, request.roleid)
    if not check_role:
        return "Role does not exist"
    role_details = db.query(model.WorkflowRoles.role_id, model.WorkflowRoles.rolename, model.WorkflowRoles.status,
                            model.WorkflowRoles.type, model.WorkflowRoles.description, model.WorkflowRoles.current_users
                            ).filter_by(role_id=request.roleid).first()
    return role_details


def get_all_roles(db: Session):
    role_details = db.query(model.WorkflowRoles.role_id, model.WorkflowRoles.rolename, model.WorkflowRoles.status,
                            model.WorkflowRoles.type, model.WorkflowRoles.description,
                            model.WorkflowRoles.current_users).all()

    roles = [
        workflow_pb2.RoleDetails(roleid=i[0], rolename=i[1], status=i[2], roletype=i[3], desc=i[4], currentusers=i[5])
        for i in role_details]
    return roles


def delete_role(db: Session, request: workflow_pb2.RoleId):
    check_role = check.check_if_role_exists(db, request.roleid)
    if not check_role:
        return "Role does not exist"

    role_to_user = check.check_if_role_assigned(db, request.roleid)
    if role_to_user:
        return "Role is assigned to user and cannot be deleted"

    # if role_assigned_to_workflow:
    #     return "Role assigned to workflow cannot be deleted"

    try:
        db.query(model.WorkflowRoles).filter_by(role_id=request.roleid).delete()
        db.commit()
        check_role = check.check_if_role_exists(db, request.roleid)
        if not check_role:
            return "Role Successfully Deleted"
    except Exception as e:
        db.rollback()
        return "Exception", e


def update_rolethreshold(db: Session, request: workflow_pb2.RoleThreshold):
    if request.minusers > request.maxusers:
        return "Minusers cannot be more than maximum users"

    threshold = model.WorkflowRoles(
        min_users=request.minusers,
        max_users=request.maxusers
    )
    temp = dict(threshold.__dict__)
    temp.pop("_sa_instance_state", None)
    try:
        db.query(model.WorkflowRoles).filter(model.WorkflowRoles.rolename == request.rolename).update(temp)
        db.commit()
        return "Threshhold Updated Sucessfully"
    except Exception as e:
        db.rollback()
        return "Exception:", e


def get_rolethreshold_by_id(db: Session, request: workflow_pb2.RoleId):
    check_role = check.check_if_role_exists(db, request.roleid)
    if not check_role:
        return "Role does not exist"
    role_threshold = db.query(model.WorkflowRoles.rolename, model.WorkflowRoles.min_users,
                              model.WorkflowRoles.max_users,
                              model.WorkflowRoles.description, model.WorkflowRoles.status).filter_by(
        role_id=request.roleid).first()
    # role_threshold = db.query(model.WorkflowRoles).options(load_only(*['rolename', 'min_users', 'max_users',
    # 'description', 'status'])).first()
    return role_threshold


def get_all_role_names(db: Session):
    rolenames = [value[0] for value in db.query(model.WorkflowRoles.rolename).all()]
    return rolenames


def get_all_users(db: Session):
    user_details = db.query(model.Users).all()
    users = [workflow_pb2.UserDetails(id=i.id, username=i.username, firstname=i.first_name, lastname=i.last_name,
                                      email=i.email, status=i.status) for i in user_details]
    return users


def get_all_role_threshold(db: Session):
    threshold_details = db.query(model.WorkflowRoles.rolename, model.WorkflowRoles.min_users,
                                 model.WorkflowRoles.max_users, model.WorkflowRoles.description,
                                 model.WorkflowRoles.status)
    roles = [workflow_pb2.RoleThreshold(rolename=i[0], minusers=i[1], maxusers=i[2], description=i[3], status=i[4])
             for i in threshold_details]
    return roles


def assign_role_to_user(db: Session, request: workflow_pb2.RoletoUser):
    check_user = check.check_if_user_exists(db, request.user_id)
    if not check_user:
        return "User does not exist"

    check_role = check.check_if_role_exists(db, request.role_id)
    if not check_role:
        return "Role does not exist"

    # role_assigned_or_not = check_if_role_assigned(db, request.roleid)
    # if role_assigned_or_not:
    #     return 'Role already assigned'

    # role_to_user_group = check_if_role_assigned_to_user_group(db, request.role_id, request.user_id)
    # if role_to_user_group:
    #     return "Role already assigned to user"

    user_role = model.UserRoles(
        role_id=request.role_id,
        user_id=request.user_id
    )
    try:
        db.add(user_role)
        db.commit()
        return "Role Assigned Successfully"
    except Exception as e:
        db.rollback()
        return "Exception:", e


def assign_role_to_user_group(db: Session, request: workflow_pb2.RoletoUsergroup):
    check_user = check.check_if_user_group_exists(db, request.user_group_id)
    if not check_user:
        return "User group does not exist"

    check_role = check.check_if_role_exists(db, request.role_id)
    if not check_role:
        return "Role does not exist"

    user_role = model.UserRoles(
        role_id=request.role_id,
        group_id=request.user_group_id
    )
    try:
        db.add(user_role)
        db.commit()
        return "Role Assigned Successfully"
    except Exception as e:
        db.rollback()
        return "Exception:", e


def assign_attribute_to_user(db: Session, request: workflow_pb2.AttributetoUser):
    check_user = check.check_if_user_exists(db, request.user_id)
    if not check_user:
        return "User does not exist"

    check_role = check.check_if_attribute_exists(db, request.attribute_id)
    if not check_role:
        return "Attribute does not exist"

    user_attribute = model.UserAttributes(
        user_id=request.user_id,
        attribute_id=request.attribute_id
    )
    try:
        db.add(user_attribute)
        db.commit()
        return "Attribute Assigned Successfully"
    except Exception as e:
        db.rollback()
        return "Exception:", e


def assign_attribute_group_to_user(db: Session, request: workflow_pb2.AttributetoUser):
    check_user = check.check_if_user_exists(db, request.user_id)
    if not check_user:
        return "User does not exist"

    check_role = check.check_if_attribute_group_exists(db, request.attribute_group_id)
    if not check_role:
        return "Attribute group does not exist"

    user_attribute = model.UserAttributes(
        user_id=request.user_id,
        attribute_group_id=request.attribute_group_id
    )
    try:
        db.add(user_attribute)
        db.commit()
        return "Attribute Assigned Successfully"
    except Exception as e:
        db.rollback()
        return "Exception:", e


def assign_permission_to_role_add_all(db: Session, request: workflow_pb2.RolePermissions):
    start = time.time()
    permissions = []
    for per in request.modules:
        permission = model.RolePermissions(
            role_id=request.roleid,
            module=per.module,
            submodule=per.submodule,
            view=per.permissions.View,
            create=per.permissions.Create,
            update=per.permissions.Update,
            archive=per.permissions.Archive,
            export=per.permissions.Export,
            download=per.permissions.Download,
            modified_by=request.modifiedby,
            last_modified_on=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        )
        permissions.append(permission)

    try:
        db.add_all(permissions)
        db.commit()
        print(time.time() - start)
        return "Permission successfully assigned"
    except Exception as e:
        db.rollback()
        return e


def assign_permission_to_role(db: Session, request: workflow_pb2.RolePermissions):
    check_role_permissions = check.check_if_permission_assigned_to_role(db, request.roleid)
    if check_role_permissions:
        return "Permissions already assigned"

    rolepermissions = []
    for per in request.permissions:
        for a in per.actions:
            permission = model.RolePermissions(
                role_id=request.roleid,
                permissions=get_permission_id(db, per.module, per.submodule, a.action),
                is_true=a.value,
                created_by=request.createdby
            )
            rolepermissions.append(permission)
    try:
        db.add_all(rolepermissions)
        db.commit()
        return 'Permissions assigned Successfully'
    except Exception as e:
        db.rollback()
        return e


def get_users_assigned_to_role(db:Session, request:workflow_pb2.RoleId):
    pass


def get_permission_id(db: Session, module: str, submodule: str, action: str):
    per_id = db.query(model.Permissions.permission_id).filter_by(module=module, submodule=submodule, action=action) \
        .one_or_none()
    return per_id[0]


def get_role_permissions(db: Session, request: workflow_pb2.RoleId):

    result = dict()
    modules = db.query(model.Permissions.module, model.Permissions.submodule, model.RolePermissions.created_by).join(model.RolePermissions, model.RolePermissions.permissions == model.Permissions.permission_id).filter(
                              model.RolePermissions.role_id == request.roleid).distinct()
    permissions = [workflow_pb2.RolePermissions.Permissions(module=i[0], submodule=i[1], actions = get_actions(db, request.roleid, i[0], i[1])) for i in modules]
    result['roleid']= request.roleid
    result['created_by'] = modules[0][2]
    result['permissions']= permissions
    return result


def get_actions(db: Session, roleid: str, module: str, submodule: str):
    actions = db.query(model.Permissions.action, model.RolePermissions.is_true).join(model.Permissions, model.RolePermissions.permissions == model.Permissions.permission_id).filter(
        model.RolePermissions.role_id == roleid, model.Permissions.module == module, model.Permissions.submodule == submodule).all()
    return [workflow_pb2.RolePermissions.Actions(action=i.action, value=i.is_true) for i in actions]


def update_role_permissions(db:Session, request:workflow_pb2.RolePermissions):
    pass


def delete_role_permissions(db:Session, request:workflow_pb2.RoleId):
    start = time.time()
    db.query(model.RolePermissions).filter_by(role_id = request.roleid).delete()
    db.commit()
