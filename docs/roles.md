# Roles of users in xSACdb

## Ordinary member
When a member joins they have no special permissions, nothing really changes when their record is updated with memberhship types or id numbers.

## Instructor
Instructors have access to feedback lists of members, upcoming lessons and can provide feedback after lessons.

## Training Officer
This member has access to all training records, all the permissions of an instructor, can plan training sessions, can award lessons (including experience dives), can award qualifications, can plan and award SDCs.

## Trip Organiser
A trip organiser can create trips and edit their own.

## Site Administrator
Can add/edit sites, trusted and qualified members. All non-ordinary roles are site admins.

## Members Officer/Moderator
Can edit all members records, once a member joins you'll need to update fields that they can't, these people can.

## Diving Officer
Encompasses all of the roles, without full admin rights.

## Administrator
Everything, including the backend django admin. This user is the ONLY one that can assign rights to others, with the exception of the instructor role which is automatically given when a training officer adds an instructor qualification.
