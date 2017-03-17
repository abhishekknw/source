'use strict';

/**
 * @ngdoc overview
 * @name societyCatalogApp
 * @description
 * # societyCatalogApp
 *
 * Main module of the application.
 */
angular
  .module('societyCatalogApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
	'slick',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
     .when('/', {
        templateUrl: 'views/societyDetails.html',
        controller: 'societyDetailsCtrl',
        controllerAs: 'society'
      })
      .when('/details', {
        templateUrl: 'details.html',
        controller: 'societyDetailsCtrl',
        controllerAs: 'main'
      })

      .otherwise({
        redirectTo: '/'
      });
  });
