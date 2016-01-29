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
})
.run(['$rootScope', '$window', '$location', 'AuthService',
     function ($rootScope, $window, $location, AuthService) {
       $rootScope.globals = $rootScope.globals || {};
       $rootScope.globals.currentUser = AuthService.UserInfo();

       var whence = $location.path();
       $rootScope.$on('$locationChangeStart', function (event, next, current) {
         var whence = $location.path();
         console.log("location change start - Whence: " + whence);

         // redirect to login page if not logged in
         $rootScope.globals.currentUser = AuthService.UserInfo();
         /*if (!$rootScope.globals.currentUser) {
           $location.path('/login');
         }
         else*/ if ($rootScope.globals.currentUser && $location.path() == '/logout')
         {
           AuthService.Logout();
           $location.path("/login");
         }
         else if ($rootScope.globals.currentUser && ($location.path() == '/login' || $location.path() == '/'))
         {
           $location.path("/");
         }
         else {
           $location.path(whence);
         }
       });
     }]);

      
