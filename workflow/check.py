import model
from sqlalchemy.orm import Session


def check_if_role_exists(db:Session, roleid: str):
    return bool(db.query(model.WorkflowRoles).filter_by(role_id=roleid).scalar())


def check_if_user_exists(db:Session, userid: str):
    return bool(db.query(model.Users).filter_by(id=userid).scalar())


def check_if_user_group_exists(db:Session, groupid: str):
    return bool(db.query(model.Groups).filter_by(id=groupid).scalar())


def check_if_role_assigned_to_user_group(db:Session, roleid:str, userid:str):
    role_assigned = check_if_role_assigned(db, roleid)
    if not role_assigned:
        return False

    # user_id = db.query(model.UserGroups.user_id).join(model.UserRoles).all()
    # print(user_id)
    # return True


def check_if_role_assigned(db:Session, roleid:str):
    return bool(db.query(model.UserRoles).filter_by(role_id=roleid).first())


def check_if_attribute_exists(db:Session, attribute_id:str):
    return bool(db.query(model.Attributes).filter_by(id=attribute_id).scalar())


def check_if_attribute_group_exists(db:Session, attribute_group_id:str):
    return bool(db.query(model.AttributeGroup).filter_by(id=attribute_group_id).scalar())


def check_if_permission_assigned_to_role(db: Session, roleid: str ):
    return bool(db.query(model.RolePermissions).filter_by(role_id=roleid).first())

