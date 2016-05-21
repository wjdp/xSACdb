# CHANGELOG

All notable changes to this project will be documented in this file. Notes should be geared towards the managers of
xSACdb instances. This project will soon adhere to [Semantic Versioning](http://semver.org/).

## [0.1.1] - Unreleased

### Fixed
- Updating planned SDC dates and notes fails.
- Upcoming SDC sorted by date.

## [0.1.0] - 2016-05-19

### Upgrading
The following is needed to upgrade from nu-8 to unreleased
- `src/manage.py migrate --fake-initial`. Faking is required for an upgrade to the authentication framework.
- `src/manage.py update_mp_cached` to initialise caches.
- `src/manage.py update_mp_training_for` to set training_for fields based on new logic.
- `src/manage.py createinitialrevisions` to create initial revisions for the version control system.

Please note the `./manage.py` command has changed to `src/manage.py`

### Added
- **Docker support**, Dockerfile for docker deployments added. Settings tweaked to allow for easy docker deployment.
  Database settings now configurable by environment variables to allow for non-predetermined values.
- **Static files** are now served by the application. Please remove aliases for /static and /media in your web server
  configs.
- **Hijack feature**, super-users now have the ability to assume the identity of any other user on the site via a
  hijack button on profile pages. Useful for issue finding and testing how others see the web interface.
- Unique ID numbers are displayed on all objects in the database to aid with recognition. IDs are prefixed with
  letters to designate their type, for example members are M1234, sessions are S1234.
- Instructor numbers are now prefixed with their code (OWI/AI/NI) automatically.
- **Revision history** via django-reversion.
- Field `hidden` in MemberProfile to hide member across entire site, useful for non-club supporting staff.
- Simple logo customisation, specify your logo in `conf/static/images/logo.png`, a 300x300 PNG is ideal.
- Support for error logging to [getsentry.com](getsentry.com).

### Changed
- Upgraded to Django 1.8 LTS.
- Major cleanup of project files. All source files now reside in the src/ directory. ./manage.py command is now
  src/manage.py command. local_settings.py now lives in conf/ folder.
- Much improvements to unit testing across the project. Automated testing via GitLab CI is now part of the development
  pipeline.
- **Training For field automation**, the training for field now automatically updates when a trainee has any lessons
  assigned for a particular qualification. Will not overwrite with a lower ranked qualification.
- Many third-party packages have been updated. django-allauth requires fake initials for it's migration from South.

### Fixed
- Fixed: Map would fail to load in sites overview.
- Fixed: Incompatibility with latest Dokku 0.5.x
- Fixed: Member profile fields allergies, veggie and other_qualifications added to detail and edit pages. Bug fixed where
  they were previously cleared by member updates. Will require manual data fixing.

## [nu-8] - 2015-03-28

[enhancement] Data structure re-jigging, allows upgrade of third-party background bits and skeleton members
[feature] Instructor dropdown on session planning page shows full names and limits choices to instructors
[feature] Poolsheets can be ordered by instructor, trainee or lesson
[bug] Google maps not showing when site is HTTPS
[bug] Google maps zoom function on edit page unusable, styling fix


## [nu-7] - 2014-11-09

[feature] Clicking Facebook title when open on login will activate login
[enhancement] More profile data is cached, some pages will load faster
[feature] Instructors are shown on the database officers page
[feature] Planned sessions can have names
[feature] Can search by first or last name in member search and trainee search
[feature] Member table additional information and design improvements
[bug] Members age was occasionally miscalculated, function performing this now adheres to the social norm of age
[bug] Performed lesson mouseover popup now shows long comments and works when scrolling
[feature] Group list page allows clicking on trainee names
[feature] Set personal qualifications on trainee record
[feature] Set instructor qualifications on trainee record
[feature] Set SDCs on trainee record
[bug] Pool sheets with undefined lessons would cause server error
[feature] `Award SDC` page implemented, allows awarding a single SDC to multiple trainees
[feature] Can have multiple lessons per trainee per session. Works on individual and group selections. Trainees in session list are now sorted by last name. (Trainees added individually cannot be added multiple times in the same selection, the process must be repeated.)
[bug] Deleting member present in a session without assigned lessons caused server error

## [nu-6] - 2014-10-27

[enhancement] Internal project refactoring

## [nu-5] - 2014-10-14

[bug] Facebook app id failure
[bug] Some views failed to load during permissions checking

## [nu-4] - 2014-09-28

[enhancement] Reduce Facebook detail scope
[enhancement] Add fill tool to bulk add forms
[enhancement] Clean up bulk add forms
[enhancement] Clean up qualification award

## [nu-3] - 2014-09-26

[bug] SiteForm missing from VC

## [nu-2] - 2014-09-26

[enhancement] Nice 404, 403, 500 pages
[enhancement] Login page styling and layout improved, now using SASS
[feature] Version numbering, inline with VC tags
[enhancement] Some site fields are now multiline
[bug] SDC icons displaying incorrectly

## [nu-1] ~ 2014-09-25

Changes previous to this are not included
