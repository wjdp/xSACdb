'use strict';

var gulp = require('gulp');

var gutil = require('gulp-util');
var gulpif = require('gulp-if');

var sourcemaps = require('gulp-sourcemaps');

var concat = require('gulp-concat');
var coffee = require('gulp-coffee');
var uglify = require('gulp-uglify');

var batch = require('gulp-batch');
var watch = require('gulp-watch');

var APPS = [
    'xsd_about',
    'xsd_auth',
    'xsd_frontend',
    'xsd_help',
    'xsd_kit',
    'xsd_members',
    'xsd_sites',
    'xsd_training',
    'xsd_trips'
];

// JS

var COFFEE_INCLUDE_PATHS = ['src/static_global/coffee/*.coffee'].concat(APPS.map(function (elem) {
   return './src/' + elem + '/static/coffee/*.coffee'
}));

function js_app(opts) {
    return gulp.src(COFFEE_INCLUDE_PATHS)
               .pipe(sourcemaps.init())
               .pipe(coffee({bare: true}).on('error', gutil.log))
               .pipe(concat('app.js'))
               .pipe(gulpif(opts.postprocess, uglify()))
               .pipe(sourcemaps.write('.'))
               .pipe(gulp.dest('dist/post/js'));
}

gulp.task('js_app', function () { return js_app({postprocess: true}) });
gulp.task('js_app_dev', function () { return js_app({postprocess: false}) });


gulp.task('watch', function() {
    watch(SASS_INCLUDE_PATHS.concat(['src/static_global/sass']), batch(function(events, done) {
        gulp.start('css_dev', done);
    }));
    watch(COFFEE_INCLUDE_PATHS, batch(function(events, done) {
        gulp.start('js_app_dev', done);
    }));
});
