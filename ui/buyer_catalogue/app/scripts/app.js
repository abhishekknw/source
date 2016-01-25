'use strict';

/**
 * @ngdoc overview
 * @name catalogueApp
 * @description
 * # catalogueApp
 *
 * Main module of the application.
 */
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
    'machadaloPages'
  ])
  .config(function ($routeProvider, $stateProvider, $urlRouterProvider, $httpProvider) {
      $routeProvider.otherwise('/');
      $stateProvider
      .state('catalogue', {
          url : '/',
          controller: 'CatalogueBaseCtrl',
          templateUrl: 'modules/pages/base/base.tmpl.html'
        })
        /*
        .state('catalogue.home', {
          url : '/catalogue',
          templateUrl: 'views/society-home.html',
          controller: 'SocietyCtrl'
        })
        */
});
