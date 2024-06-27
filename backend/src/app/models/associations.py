from ..orm import orm

# Association table for a many-to-many relationship between Users and Classrooms.
# This table links users with the classrooms they occupy.
user_occupied_classroom_association = orm.Table(
    'user_occupied_classroom_association', orm.Model.metadata,
    orm.Column('user_id', orm.Integer, orm.ForeignKey('user_table.id')),
    orm.Column('classroom_id', orm.Integer, orm.ForeignKey('classroom_table.id'))
)

# Association table for a many-to-many relationship between Users and Requests.
# This table links users with the requests they are involved in.
user_request_association = orm.Table(
    'user_request_association', orm.Model.metadata,
    orm.Column('user_id', orm.Integer, orm.ForeignKey('user_table.id')),
    orm.Column('request_id', orm.Integer, orm.ForeignKey('request_table.id'))
)
