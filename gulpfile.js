const { src, dest, watch, parallel, series } = require("gulp");
const scss = require("gulp-sass");
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

const browsersync = () => {
  browserSync.init({
    notify: false,
    proxy: "localhost:5000",
    browser: "google chrome",
  });
};

const styles = () => {
  return src("ui/scss/style.scss")
    .pipe(scss({ outputStyle: "compressed" }))
    .pipe(concat("style.min.css"))
    .pipe(
      autoprefixer({
        overrideBrowserslist: ["last 10 versions"],
        grid: true,
      })
    )
    .pipe(dest("app/static/css"))
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
  return src(["app/static/js/main.js"])
    .pipe(concat("main.min.js"))
    .pipe(uglify())
    .pipe(dest("app/static/js"))
    .pipe(browserSync.stream());
};

const cleanDist = () => {
  return del("dist");
};

const build = () => {
  return src(["app/**/*.html", "app/css/styles.min.css", "app/js/main.min.js"], { base: "app" }).pipe(dest("dist"));
};

const watcher = () => {
  watch(["scss/**/*.scss"], styles);
  watch(["app/static/js/**/*.js", "!app/js/main.min.js"], scripts);
  watch(["app/templates/**/*.html"]).on("change", browserSync.reload);
  watch(["app/static/images/icons/*.svg", "!app/images/icons/sprite.svg"], svg);
};

exports.styles = styles;
exports.scripts = scripts;
exports.browsersync = browsersync;
exports.images = images;
exports.cleanDist = cleanDist;
exports.watcher = watcher;
exports.svg = svg;

exports.build = series(cleanDist, images, build);
exports.default = parallel(styles, scripts, svg, browsersync, watcher);
