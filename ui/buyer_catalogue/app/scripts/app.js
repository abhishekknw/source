'use strict';

/**
 * @ngdoc overview
 * @name catalogueApp
 * @description
 * # catalogueApp
 *
 * Main module of the application.
 */

var APIBaseUrl = 'http://localhost:8108/';

angular.module('Authentication', []);
angular
  .module('catalogueApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ui.router',
    'ngSanitize',
    'ngTouch',
    'machadaloCommon',
    'machadaloPages',
    'Authentication'
  ])
  .config(function ($routeProvider, $stateProvider, $urlRouterProvider, $httpProvider) {
      $routeProvider.otherwise('/');
      $stateProvider
      .state('catalogue', {
          url : '/',
          controller: 'CatalogueBaseCtrl',
          templateUrl: 'modules/pages/base/base.tmpl.html'
        })
      .state('login', {
          url : '/login',
          controller: 'LoginCtrl',
          templateUrl: 'modules/pages/login/login.tmpl.html'
        })

        /*
        .state('catalogue.home', {
          url : '/catalogue',
          templateUrl: 'views/society-home.html',
          controller: 'SocietyCtrl'
        })
        */
});
