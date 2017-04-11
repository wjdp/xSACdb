'use strict';

var gulp = require('gulp');

var gutil = require('gulp-util');
var gulpif = require('gulp-if');
var shell = require('gulp-shell');

var sourcemaps = require('gulp-sourcemaps');

var sass = require('gulp-sass');

var postcss = require('gulp-postcss');
var cssnext = require('postcss-cssnext');
var cssnano = require('cssnano');
var concat = require('gulp-concat');
var coffee = require('gulp-coffee');
var uglify = require('gulp-uglify');

var batch = require('gulp-batch');
var watch = require('gulp-watch');

// CSS

function css(opts) {
    if (opts.postprocess) {
        var processors = [
            cssnext(),
            cssnano({autoprefixer: false}),
        ];
    } else { var processors = [] }

    return gulp.src('src/static_global/sass/build.sass')
        .pipe(sourcemaps.init())
        .pipe(sass(
            {includePaths: ['./lib']}
         ).on('error', sass.logError))
        .pipe(postcss(processors))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('dist/post/css'));
}

gulp.task('css', function () { return css({postprocess: true}) });
gulp.task('css_dev', function () { return css({postprocess: false}) });

// JS

function js_app(opts) {
    return gulp.src('src/static_global/coffee/*.coffee')
               .pipe(sourcemaps.init())
               .pipe(coffee({bare: true}).on('error', gutil.log))
               .pipe(concat('app.js'))
               .pipe(gulpif(opts.postprocess, uglify()))
               .pipe(sourcemaps.write('.'))
               .pipe(gulp.dest('dist/post/js'));
}

gulp.task('js_app', function () { return js_app({postprocess: true}) });
gulp.task('js_app_dev', function () { return js_app({postprocess: false}) });

var JS_LIBS = [
    './lib/jquery/dist/jquery.js',
    './lib/jquery-form/jquery.form.js',
    './lib/jquery-tokeninput/src/jquery.tokeninput.js',
    './lib/jquery-form/jquery.form.js',
    './lib/js/jquery.cookie.js">',
    './lib/tether/dist/js/tether.js',
    './lib/bootstrap/dist/js/bootstrap.js',
    './lib/raven-js/dist/raven.min.js',
];

function js_lib(opts) {
    return gulp.src(JS_LIBS)
               .pipe(sourcemaps.init())
               .pipe(concat('lib.js'))
               .pipe(gulpif(opts.postprocess, uglify()))
               .pipe(sourcemaps.write('.'))
               .pipe(gulp.dest('dist/post/js'));
}

gulp.task('js_lib', function () { return js_lib({postprocess: true}) });
gulp.task('js_lib_dev', function () { return js_lib({postprocess: false}) });

gulp.task('watch', function() {
    watch(['src/static_global/sass'], batch(function(events, done) {
        gulp.start('css_dev', done);
    }));
})

// Frontend tasks

gulp.task('frontend', ['css',
                       'js_app',
                       'js_lib'])

gulp.task('frontend_dev', ['css_dev',
                           'js_app_dev',
                           'js_lib_dev']);

gulp.task('dev', ['frontend_dev'])
gulp.task('default', ['dev'])

gulp.task('deploy', ['frontend'])
