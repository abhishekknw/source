// Karma configuration
// http://karma-runner.github.io/0.12/config/configuration-file.html
// Generated on 2016-01-25 using
// generator-karma 1.0.1

module.exports = function(config) {
  'use strict';

  config.set({
    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,

    // base path, that will be used to resolve files and exclude
    basePath: '../',

    // testing framework to use (jasmine/mocha/qunit/...)
    // as well as any additional frameworks (requirejs/chai/sinon/...)
    frameworks: [
      "jasmine"
    ],

    // list of files / patterns to load in the browser
    files: [
      // bower:js
      'bower_components/jquery/dist/jquery.js',
      'bower_components/angular/angular.js',
      'bower_components/bootstrap/js/dropdown.js',
      'bower_components/moment/moment.js',
      'bower_components/fullcalendar/dist/fullcalendar.js',
      'bower_components/leaflet/dist/leaflet-src.js',
      'bower_components/slimScroll/jquery.slimscroll.js',
      'bower_components/angular-cookies/angular-cookies.js',
      'bower_components/angular-resource/angular-resource.js',
      'bower_components/angular-route/angular-route.js',
      'bower_components/angular-sanitize/angular-sanitize.js',
      'bower_components/angular-touch/angular-touch.js',
      'bower_components/angular-ui-router/release/angular-ui-router.js',
      'bower_components/slick-carousel/slick/slick.js',
      'bower_components/angular-slick-carousel/dist/angular-slick.js',
      'bower_components/angular-rangeslider/angular.rangeSlider.js',
      'bower_components/angularjs-slider/dist/rzslider.js',
      'bower_components/angular-filter/dist/angular-filter.js',
      'bower_components/angularUtils-pagination/dirPagination.js',
      'bower_components/myforce-angularjs-dropdown-multiselect/dist/angularjs-dropdown-multiselect.min.js',
      'bower_components/ng-file-upload/ng-file-upload.js',
      'bower_components/ng-file-upload-shim/ng-file-upload-shim.js',
      'bower_components/angular-simple-logger/dist/angular-simple-logger.js',
      'bower_components/lodash/lodash.js',
      'bower_components/markerclustererplus/src/markerclusterer.js',
      'bower_components/google-maps-utility-library-v3-markerwithlabel/dist/markerwithlabel.js',
      'bower_components/google-maps-utility-library-v3-infobox/dist/infobox.js',
      'bower_components/google-maps-utility-library-v3-keydragzoom/dist/keydragzoom.js',
      'bower_components/js-rich-marker/src/richmarker.js',
      'bower_components/angular-google-maps/dist/angular-google-maps.js',
      'bower_components/angular-breadcrumb/release/angular-breadcrumb.js',
      'bower_components/bootstrap-sweetalert/dist/sweetalert.js',
      'bower_components/angular-aria/angular-aria.js',
      'bower_components/angular-scrollable-table/angular-scrollable-table.js',
      'bower_components/angular-loading-bar/build/loading-bar.js',
      'bower_components/angular-recaptcha/release/angular-recaptcha.js',
      'bower_components/angular-animate/angular-animate.js',
      'bower_components/angular-messages/angular-messages.js',
      'bower_components/angular-material/angular-material.js',
      'bower_components/d3/d3.js',
      'bower_components/nvd3/build/nv.d3.js',
      'bower_components/angular-nvd3/dist/angular-nvd3.js',
      'bower_components/chart.js/dist/Chart.js',
      'bower_components/angular-chart.js/dist/angular-chart.js',
      'bower_components/angular-percent-circle-directive/dist/percent-circle-directive.js',
      'bower_components/angularjs-dropdown-multiselect/src/angularjs-dropdown-multiselect.js',
      'bower_components/ng-table-to-csv/dist/ng-table-to-csv.js',
      'bower_components/angular-ui-grid/ui-grid.js',
      'bower_components/js-xlsx/dist/xlsx.core.min.js',
      'bower_components/angular-js-xlsx/angular-js-xlsx.js',
      'bower_components/toastr/toastr.js',
      'bower_components/angular-smart-table/dist/smart-table.js',
      'bower_components/angular-xeditable/dist/js/xeditable.js',
      'bower_components/angular-slimscroll/angular-slimscroll.js',
      'bower_components/jstree/dist/jstree.js',
      'bower_components/ng-js-tree/dist/ngJsTree.js',
      'bower_components/angular-progress-button-styles/dist/angular-progress-button-styles.min.js',
      'bower_components/jquery-ui/jquery-ui.js',
      'bower_components/angular-ui-sortable/sortable.js',
      'bower_components/angular-toastr/dist/angular-toastr.tpls.js',
      'bower_components/AngularJS-Toaster/toaster.js',
      'bower_components/amcharts3/amcharts/amcharts.js',
      'bower_components/amcharts-stock/dist/amcharts/amstock.js',
      'bower_components/eve-raphael/eve.js',
      'bower_components/raphael/raphael.min.js',
      'bower_components/mocha/mocha.js',
      'bower_components/morris.js/morris.js',
      'bower_components/angular-morris/build/module/angular-morris/angular-morris.min.js',
      'bower_components/ammap/dist/ammap/ammap.js',
      'bower_components/ammap/dist/ammap/maps/js/worldLow.js',
      'bower_components/chartist/dist/chartist.min.js',
      'bower_components/angular-chartist.js/dist/angular-chartist.js',
      'bower_components/angular-morris-chart/src/angular-morris-chart.min.js',
      'bower_components/ionrangeslider/js/ion.rangeSlider.js',
      'bower_components/rangy/rangy-core.js',
      'bower_components/rangy/rangy-classapplier.js',
      'bower_components/rangy/rangy-highlighter.js',
      'bower_components/rangy/rangy-selectionsaverestore.js',
      'bower_components/rangy/rangy-serializer.js',
      'bower_components/rangy/rangy-textrange.js',
      'bower_components/textAngular/dist/textAngular.js',
      'bower_components/textAngular/dist/textAngular-sanitize.js',
      'bower_components/textAngular/dist/textAngularSetup.js',
      'bower_components/angular-ui-select/dist/select.js',
      'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
      'bower_components/aws-sdk/dist/aws-sdk.js',
      'bower_components/angular-circular-progress/dist/circularProgress.min.js',
      'bower_components/ngmap/build/scripts/ng-map.js',
      'bower_components/angular-mocks/angular-mocks.js',
      // endbower
      "app/scripts/**/*.js",
      "test/mock/**/*.js",
      "test/spec/**/*.js"
    ],

    // list of files / patterns to exclude
    exclude: [
    ],

    // web server port
    port: 8080,

    // Start these browsers, currently available:
    // - Chrome
    // - ChromeCanary
    // - Firefox
    // - Opera
    // - Safari (only Mac)
    // - PhantomJS
    // - IE (only Windows)
    browsers: [
      "PhantomJS"
    ],

    // Which plugins to enable
    plugins: [
      "karma-phantomjs-launcher",
      "karma-jasmine"
    ],

    // Continuous Integration mode
    // if true, it capture browsers, run tests and exit
    singleRun: false,

    colors: true,

    // level of logging
    // possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
    logLevel: config.LOG_INFO,

    // Uncomment the following lines if you are using grunt's server to run the tests
    // proxies: {
    //   '/': 'http://localhost:9000/'
    // },
    // URL root prevent conflicts with the site root
    // urlRoot: '_karma_'
  });
};
