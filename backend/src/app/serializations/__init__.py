from .authentication_models import create_login_post_model, create_login_get_model, create_refresh_get_model
from .building_models import create_building_post_model, create_building_put_model, create_building_get_model, \
    create_buildings_get_model
from .department_models import create_department_post_model, create_department_put_model, create_department_get_model, \
    create_departments_get_model
from .request_models import create_request_post_model, create_request_put_model, create_request_approve_put_model, \
    create_request_get_model, create_requests_get_model
from .classrooms_models import create_classroom_post_model, create_classroom_put_model, create_classroom_get_model, \
    create_classrooms_get_model
from .user_models import create_user_post_model, create_user_put_model, create_user_get_model, create_users_get_model
