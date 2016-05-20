from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Personal',
        'access': is_all,
        'items': (
            ('Overview', 'fa fa-tachometer', 'xsd_training:training-overview', []),
            ('Lessons', 'fa fa-mortar-board', 'xsd_training:training-lessons', []),
            ('Feedback', 'fa fa-comment', 'xsd_training:all-feedback', []),
        )
    },
    {
        'title': 'Skill Development Courses',
        'access': is_all,
        'items': (
            ('All SDCs', 'fa fa-list', 'xsd_training:SDCList', []),
            ('Lessons', 'fa fa-calendar', 'xsd_training:PerformedSDCList', ['xsd_training:PerformedSDCDetail']),
        )
    },
    {
        'title': 'Teaching',
        'access': is_instructor,
        'items': (
            ('Lessons', 'fa fa-clock-o', 'xsd_training:InstructorUpcoming', []),
            ('Trainee Notes', 'fa fa-pencil-square-o', 'xsd_training:TraineeNotesSearch', []),
        )
    },
    {
        'title': 'Trainee Administration',
        'access': is_training,
        'items': (
            ('Groups', 'fa fa-users', 'xsd_training:TraineeGroupList', ['xsd_training:TraineeGroupCreate',
                                                                        'xsd_training:TraineeGroupUpdate',
                                                                        'xsd_training:TraineeGroupDelete',]),
            ('Progress Report', 'fa fa-flag-checkered', 'xsd_training:TraineeGroupProgress', []),
            ('Update Requests', 'fa fa-envelope-o', 'xsd_training:TrainingUpdateRequestList', []),
        )
    },
    {
        'title': 'Teaching Administration',
        'access': is_training,
        'items': (
            ('Session Planning', 'fa fa-calendar', 'xsd_training:SessionList', ['xsd_training:SessionCreate',
                                                                                'xsd_training:SessionPlanner',
                                                                                'xsd_training:SessionDelete',]),
            ('Create Pool Sheet', 'fa fa-file-o', 'xsd_training:PoolSheet', []),
            ('Retrospectively Add Lessons', 'fa fa-table', 'xsd_training:RetroAddLessons', []),
            ('Award Qualifications', 'fa fa-trophy', 'xsd_training:QualificationAward', []),
        )
    },
    {
        'title': 'SDC Administration',
        'access': is_training,
        'items': (
            ('Plan an SDC', 'fa fa-calendar', 'xsd_training:PerformedSDCCreate', []),
            ('Award SDCs', 'fa fa-trophy', 'xsd_training:SDCAward', []),
        )
    },
)
