# CHANGELOG

All notable changes to this project will be documented in this file. Notes should be geared towards the managers of
xSACdb instances. This project will soon adhere to [Semantic Versioning](http://semver.org/).


## [0.8.1] - 2019-11-07

### Fixed

- #342 Scheduler health check crashing
- #340 Trip date in list should only show one date if starts and ends on same day

### Refactored

- Replaced the outdated bower/gulp frontend build system with Webpack.


## [0.8.0] - 2019-11-02

### Changed

- Upgraded Python version from v2 to v3.
- Show 2 weeks of past lessons to instructors in the upcoming lessons view. 


## [0.7.0] - 2019-05-18

### Added

- #324 Ability to retire qualifications and lessons (for hiding old OD syllabus for new trainees).

### Fixed

- Approve new member button showing for new member on their profile (button did not actually do anything).


## [0.6.0] - 2019-01-12

### Added
- Version inspection API endpoint. Allows checking the version of instances programmatically.

### Changed
- Deployment now handled in straight docker (add docker compose to maintain sanity). Dokku support has been removed as it was a PITA.
- Link for medical form updated to use correct website (http://www.ukdmc.org), they appear to have lost control of their previous domain.

### Removed
- Instructor qualification 'setter' on trainee notes view. All qualifications go through the 'Award New Qualification' form.


## [0.5.3] - 2017-06-18

### Added
- #308 Add modal detail view for lessons to trainee notes view. Allow adding, editing and deleting performed lessons from trainee notes view.

### Changes
- The trainee's lesson detail view uses the same template as the new modal detail view.
- The Django admin site shows the club name in the header in the same style as the server's shell.


## [0.5.2] - 2017-05-20

### Fixes
- #300 Fix geoposition field on sites using @wjdp's patch for dependency django-geoposition. 


## [0.5.1] - 2017-05-14

### Fixes
- Pre-deployment script was failing on new installs.


## [0.5.0] - 2017-05-10

This is a provisional release, club instances will be upgraded to it after a test period.

### Changes
- Upgrade our core framework (Django) to the newly released long term support version. This upgrade required a certain amount of refactoring of various parts of the project.


## [0.4.0] - 2017-05-08

### Added
- Several timestamps (pre, post and deploy), relating to the time the application was built, are shown on the about page.
- Date-picker widgets to some date fields.

### Changes
- Qualifications now have additional information attached: mode (internal, external, XO, other), XO from, signed off by and date and a notes field. Current qualifications are migrated with these details blank. Award, update and remove all via the trainee profile.
- Upgraded Bootstrap (frontend framework) to v4.a6, required some adjusting of some frontend components. Now using Gulp to build frontend assets.
- Member and trainee search templates have been improved.
- Rendering of the map on site overview has been improved, made to fill more available space.

### Removed
- 'Award Qualifications' tool. As qualifications now want more details, adding in bulk isn't a good idea.

### Fixes
- #292 Archived members were unable to restore their profiles after logging in.
- Some internal fields were showing on the diff for profile updates. These have been hidden.


## [0.3.7] - 2017-04-07

### Changes
- Minor upgrades of upstream packages.


## [0.3.6] - 2017-03-25

### Changes
- We now attempt to load `conf/local_settings.py` for development. Creating this file is optional we fo not fail if it is missing.
- Upgrade to geoposition plugin now requires Google maps API key `GOOGLE_MAPS_API_KEY` to be set in local_settings.


## [0.3.5] - 2017-03-23

### Added
- Placeholder feed 'Your updates here' box shows for members with less than six items in their feed. See http://i.imgur.com/ZWmhjaD.png.
- `manage refresh` command to wipe ephemeral stores—i.e. the cache—and rebuild them without knowledge of which commands are needed for all that.

### Changes
- Some caching improvements.

### Fixes
- Application nav module titles were incorrectly changed to blue, now back to grey
- Trip attendee list now sorted.


## [0.3.4] - 2017-03-22

### Fixes
- Bug #284: Far too many warnings logged, apply a result timeout to periodic tasks to prevent this.


## [0.3.3] - 2017-02-25

### Fixes
- Fix qualification and SDC award forms. See #280.


## [0.3.2] - 2017-02-25

### Added
- Background task worker health check.
- Any application template can be overridden from the config directory `conf/templates`. Useful for custom email templates.
- Health check for background task worker.

### Changes
- Made the email confirm templates a little friendlier.
- Colour and styling tweaks.

### Fixes
- Fixed side navigation scrolling bug on mobile – #279


## [0.3.1] - 2017-02-23

### Added
- Pagination for dashboard/activity feed and trips. Setting `PAGINATE_BY` defaults to 20. Prevents long page build times for long datasets, also silly long pages.
- Notice for empty trip list.
- Members officers can click on actors in activity feed.

### Fixes
- `manage auth_send_confirmations` no longer sends confirmation emails to archived members.
- Corrected wording on trip CSV export modal.


## [0.3.0] - 2017-02-23

### Upgrade
- There is a problem with a single migration. After upgrade you will need to work through the following process. See issue [#272](https://gitlab.com/wjdp/xSACdb/issues/272) for more information.
    - Enter the shell
    - Disable the migration `xsd_frontend.0002_xsdaction_xsdversion`
    - Run other migrations; `manage migrate`
    - Reinstate the `xsd_frontend.0002_xsdaction_xsdversion` migration.
    - Run `manage migrate` one more time.
- Run `manage update_follow_defaults` to make current users follow changes to their profiles. New users have this set automatically.
- Run `manage build_version_cache` to speed up initial load times of user feeds.
- At some point run `migrate` manually from the shell. It will prompt to delete the model `xsd_trips | tripattendee` as it is no longer used by the application. Answer yes.
- Run `manage auth_sync` to synchronise the internal user/email table with the allauth email table. Needed for email validation. Only needs to be run once.

### Added
- **Trips:** Trip planning has been added. Any user may add a trip, a trip officer (currently GROUP_ADMIN, GROUP_TRAINING, GROUP_TRIPS, GROUP_DO) must approve before the trip organiser/owner may take it public.
- **Activity feed:** users see activity they are involved with — currently their own profiles and trips they're on. Adding _activities_ for the training module is being held back until the next minor version.
- **History Pages:** most objects now have a browsable history.
- User _email management_ interface. Users can be associated with multiple emails with a set primary.
- Management commands `auth_sync`
- Nice big 'All Done' pageon signup completion. See https://i.imgur.com/WGPwF7m.png. Text is customisable through the CLUB dictionary.

### Changed
- Users without **avatars** now use the Gravatar retro generator to create an identicon to use instead. The generator is customisable through the CLUB dictionary.
- All signups now trigger sending a validation email.
- You can trigger sending validation emails to all unverified addresses with `manage auth_send_confirmations`. Ensure `auth_sync` is run first.
- Improved styling of account pages.

### Fixes
- A number of styling fixes.
- Cache and page speed improvements.
- `manage createsuperuser` now pre-approves and add the superuser to the admin group.
- Dockerfile deployment now caches depedancy installation between versions.


## [0.2.1] - 2017-02-16

### Added
- Ability to _archive_ old members. Archived members will not show on most members listings and will have personal details expunged from their profile.
- Listing of archived members, ability to restore. Archived members are also restored when they log in again and re-fill-out the profile form.

### Changed
- The _'Remove New Flag'_ button on new members has been changed to _'Approve'_.
- Tweaked production config for better performance.

### Fixed
- Favicons and application manifests (add to homescreen on mobile) were broken in 0.2.0. Now fixed. See #243 and #246.


## [0.2.0] - 2017-02-13

Using Docker/Dokku support added in 0.1.0 we are recommending that all deployments of xSACdb are done via a Dokku
server. This ensures that your production environment is identical to that used in development and testing. Deployments
and upgrades are also much faster.

### Upgrade
- Upgrade notes will now pertain to Dokku installations.
- Orphaned users, users without member profiles, may exist in your database due to bug #88.
  Run `manage delete_orphaned_users` in the shell to remove them. A summary of users followed by a y/n prompt will be
  presented.
- Set the correct name and URL of your instance in /admin/sites/site/. This data is used when sending email.
- Forgot password and password reset now need email. A valid set of SMTP credentials is now required in your config.

### Added
- If you're using Sentry for error logging user is asked for feedback when a 500 happens.
- Added task runner support. You now need to run some task runners and a task scheduler alongside the server.
  This depends on Redis, a Redis server is needed and must be configured in local_settings.py for bare installs.
- Added styling to the application shell.
- Added health check page `/health/`, provides 'ready-to-go' signal for Dokku deployment.
- Added fake data generation for staging environments. See [next.xsacdb.wjdp.uk](https://next.xsacdb.wjdp.uk). Login as
  su/su.
- Login page now features a 'forgot password' feature.
- Added email templates for verification and password reset. Currently only social login triggers email verification.
  Manual signup will trigger it in the next minor.

### Changed
- Upgraded the UI framework from Bootstrap v2 to v4, includes *significant UI improvements* especially on mobile. Some
  areas of the site haven't quite been fully optimised for the new styling, this will come with later versions.
- Redesigned, mobile friendly login and register pages.
- Because we have Redis, cache backend has switched from in-memory to Redis.
- Temporarily removed the ability to express interest in an SDC. This will be re-implemented in a later version.

### Fixed
- Bug #88, user instances are orphaned after their member profiles are deleted. Users are now deleted at the same time.

## Development
- Tests have been optimised and now utilise the Faker library with a predefined seed to reliably generate test data.
- Added PyCharm configuration
- Added automatic deployment to next.xsacdb.wjdp.uk from development branch via CI job.


## [0.1.2] - 2016-07-05

### Changed
- Display qualification list on training dash for users without any qualifications or training_for, #144

### Fixed
- Updating planned SDC dates and notes fails.
- Upcoming SDC sorted by date.
- Server error when generating pool sheet, #223


## [0.1.1] - 2016-05-24

### Fixed
- Long email addresses would cause an exception when used for registering a local account. Issue #198.


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
