from dotenv import load_dotenv
import os
import time
import logging
import grpc
from concurrent import futures
import model
from database import SessionLocal, engine
import crud

import workflow_pb2
import workflow_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

load_dotenv()

model.Base.metadata.create_all(bind=engine)


def get_db():
    return SessionLocal()


class WorkFlow(workflow_pb2_grpc.WorkFlowServicer):

    def CreateRole(self, request, context):
        db = get_db()
        result = crud.create_role(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def CreateThreshold(self, request, context):
        db = get_db()
        result = crud.update_rolethreshold(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def UpdateRole(self, request, context):
        db = get_db()
        result = crud.update_role(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def GetRole(self, request, context):
        db = get_db()
        result = crud.get_role_details(db, request)
        return workflow_pb2.RoleDetails(roleid=result[0], rolename=result[1],
                                        status=result[2], roletype=result[3], desc=result[4],
                                        currentusers=result[5])

    def GetAllRole(self, request, context):
        db = get_db()
        result = crud.get_all_roles(db)
        return workflow_pb2.Roles(roles=result)

    def DeleteRole(self, request, context):
        db = get_db()
        result = crud.delete_role(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def GetRoleThreshold(self, request, context):
        db = get_db()
        result = crud.get_rolethreshold_by_id(db, request)
        return workflow_pb2.RoleThreshold(rolename=result[0], minusers=result[1],
                                          maxusers=result[2], description=result[3], status=result[4])

    def GetRoleNames(self, request, context):
        db = get_db()
        result = crud.get_all_role_names(db)
        return workflow_pb2.RoleNames(rolenames=result)

    def GetAllRoleThreshold(self, request, context):
        db = get_db()
        result = crud.get_all_role_threshold(db)
        return workflow_pb2.AllRoleThresholds(rolethresholds=result)

    def GetUserDetails(self, request, context):
        db = get_db()
        result = crud.get_all_users(db)
        return workflow_pb2.Users(users=result)

    def AssignRoletoUser(self, request, context):
        db = get_db()
        result = crud.assign_role_to_user(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def AssignRoletoUserGroup(self, request, context):
        db = get_db()
        result = crud.assign_role_to_user_group(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def AssignAttributestoUser(self, request, context):
        db = get_db()
        result = crud.assign_attribute_to_user(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def AssignAttributeGroupstoUser(self, request, context):
        db = get_db()
        result = crud.assign_attribute_group_to_user(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def GetUserforRole(self, request, context):
        db = get_db()
        result = crud.get_users_assigned_to_role(db, request)
        return workflow_pb2.Users(users=result)

    def AssignPermissionToRole(self, request, context):
        db = get_db()
        result = crud.assign_permission_to_role(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def GetRolePermissions(self, request, context):
        db = get_db()
        result = crud.get_role_permissions(db, request)
        return workflow_pb2.RolePermissions(roleid=result['roleid'], createdby=result['created_by'], permissions=result['permissions'])

    def UpdateRolePermissions(self, request, context):
        db = get_db()
        result = crud.update_role_permissions(db, request)
        return workflow_pb2.StatusResponse(message=result)

    def DeleteRolePermissions(self, request, context):
        db=get_db()
        result = crud.delete_role_permissions(db, request)
        return workflow_pb2.StatusResponse(message=result)




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    workflow_pb2_grpc.add_WorkFlowServicer_to_server(WorkFlow(), server)
    server.add_insecure_port('GRPC_PORT')
    server.start()
    try:
        while True:
            time.sleep(int(os.getenv('_ONE_DAY_IN_SECONDS')))
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    print('Starting Server...')
    logging.basicConfig(filename="logs.log", level=logging.DEBUG)
    logging.info("Server started")
    serve()
