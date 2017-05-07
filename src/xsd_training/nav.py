from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Personal',
        'access': is_verified,
        'items': [
            ('Overview', None, 'fa fa-tachometer', 'xsd_training:training-overview', []),
            ('Lessons', None, 'fa fa-mortar-board', 'xsd_training:training-lessons', []),
            ('Feedback', None, 'fa fa-comment', 'xsd_training:all-feedback', []),
        ]
    },
    {
        'title': 'Skill Development Courses',
        'access': is_verified,
        'items': [
            ('All SDCs', None, 'fa fa-list', 'xsd_training:SDCList', []),
            ('Upcoming Courses', None, 'fa fa-calendar', 'xsd_training:PerformedSDCList', ['xsd_training:PerformedSDCDetail']),
        ]
    },
    {
        'title': 'Teaching',
        'access': is_instructor,
        'items': [
            ('Lessons', None, 'fa fa-clock-o', 'xsd_training:InstructorUpcoming', []),
            ('Trainee Profiles', None, 'fa fa-pencil-square-o', 'xsd_training:TraineeNotesSearch', []),
        ]
    },
    {
        'title': 'Trainee Administration',
        'access': is_training,
        'items': [
            ('Groups', None, 'fa fa-users', 'xsd_training:TraineeGroupList', ['xsd_training:TraineeGroupCreate',
                                                                        'xsd_training:TraineeGroupUpdate',
                                                                        'xsd_training:TraineeGroupDelete',]),
            ('Progress Report', None, 'fa fa-flag-checkered', 'xsd_training:TraineeGroupProgress', []),
            ('Update Requests', None, 'fa fa-envelope-o', 'xsd_training:TrainingUpdateRequestList', []),
        ]
    },
    {
        'title': 'Teaching Administration',
        'access': is_training,
        'items': [
            ('Session Planning', None, 'fa fa-calendar', 'xsd_training:SessionList', ['xsd_training:SessionCreate',
                                                                                'xsd_training:SessionPlanner',
                                                                                'xsd_training:SessionDelete',]),
            ('Create Pool Sheet', None, 'fa fa-file-o', 'xsd_training:PoolSheet', []),
            ('Retrospectively Add Lessons', None, 'fa fa-table', 'xsd_training:RetroAddLessons', []),
        ]
    },
    {
        'title': 'SDC Administration',
        'access': is_training,
        'items': [
            ('Plan an SDC', None, 'fa fa-calendar', 'xsd_training:PerformedSDCCreate', []),
            ('Award SDCs', None, 'fa fa-trophy', 'xsd_training:SDCAward', []),
        ]
    },
)
