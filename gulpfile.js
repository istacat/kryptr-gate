'use strict';

const { src, dest, watch, parallel, series } = require("gulp");
const sass = require("gulp-sass");
const concat = require("gulp-concat");
const autoprefixer = require("gulp-autoprefixer");
const uglify = require("gulp-uglify");
const imagemin = require("gulp-imagemin");
const svgmin = require("gulp-svgmin");
const svgSprite = require("gulp-svg-sprite");
const cheerio = require("gulp-cheerio");
const replace = require("gulp-replace");
const del = require("del");
const browserSync = require("browser-sync").create();
const sourcemaps = require("gulp-sourcemaps");

sass.compiler = require('node-sass');

const browsersync = () => {
  browserSync.init({
    notify: false,
    proxy: "localhost:5000",
    browser: "google chrome",
  });
};

const styles = () => {
  return src("ui/scss/style.scss")
    .pipe(sourcemaps.init())
    .pipe(sass({ outputStyle: "compressed"}).on('error', sass.logError))
    .pipe(dest("./app/static/css/"))
    .pipe(sourcemaps.write())
    .pipe(
      autoprefixer({
        overrideBrowserslist: ["last 10 versions"],
        grid: true,
      })
    )
    .pipe(browserSync.stream());
};

const images = () => {
  return src("ui/images/**/*.*")
    .pipe(
      imagemin([
        imagemin.gifsicle({ interlaced: true }),
        imagemin.mozjpeg({ quality: 75, progressive: true }),
        imagemin.optipng({ optimizationLevel: 5 }),
        imagemin.svgo({
          plugins: [{ removeViewBox: true }, { cleanupIDs: false }],
        }),
      ])
    )
    .pipe(dest("app/static/images"));
};

const svg = () => {
  return src(["ui/images/icons/*.svg", "!ui/images/icons/sprite.svg"])
    .pipe(
      svgmin({
        js2svg: {
          pretty: true,
        },
      })
    )
    .pipe(
      cheerio({
        run: ($) => {
          $("[fill]").removeAttr("fill");
          $("[stroke]").removeAttr("stroke");
          $("[style]").removeAttr("style");
        },
        parserOptions: { xmlMode: true },
      })
    )
    .pipe(replace("&gt;", ">"))
    .pipe(
      svgSprite({
        mode: {
          stack: {
            sprite: "../sprite.svg",
          },
        },
      })
    )
    .pipe(dest("app/static/images/icons"));
};

const scripts = () => {
  return src(["app/static/js/main.js", "app/static/js/account.js"])
    .pipe(sourcemaps.init())
    .pipe(concat("main.min.js"))
    .pipe(uglify())
    .pipe(sourcemaps.write())
    .pipe(dest("app/static/js"))
    .pipe(browserSync.stream());
};

const cleanDist = () => {
  return del("dist");
};

const build = () => {
  return src(
    [
      "app/**/*.html",
      "app/static/css/style.css",
      "app/static/js/main.min.js",
    ],
    { base: "app" }
  ).pipe(dest("dist"));
};

const jsSrcFiles = ["app/static/js/main.js"];

const watcher = () => {
  watch(["ui/scss/**/*.scss"], styles);
  watch(jsSrcFiles, scripts);
  watch(["app/templates/**/*.html"]).on("change", browserSync.reload);
  watch(["ui/images/icons/*.svg", "!ui/icons/sprite.svg"], svg);
};

exports.styles = styles;
exports.scripts = scripts;
exports.browsersync = browsersync;
exports.images = images;
exports.cleanDist = cleanDist;
exports.watcher = watcher;
exports.svg = svg;


exports.build = series(cleanDist, images, build, styles, scripts, svg);
exports.default = parallel(styles, scripts, svg, browsersync, watcher);