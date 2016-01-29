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
      .state('society', {
          url : '/society',
          controller: 'CatalogueBaseCtrl',
          templateUrl: 'modules/pages/base/base.tmpl.html'
        })
        .state('society.list', {
          url : '/list', //:societyId/
          templateUrl: 'modules/pages/societydetails/societydetails.tmpl.html',
          controller: 'SocietyListCtrl'
        })
        .state('society.details', {
          url : '/details', //:societyId/
          templateUrl: 'modules/pages/societydetails/societydetails.tmpl.html',
          controller: 'SocietyCtrl'
        });
});
