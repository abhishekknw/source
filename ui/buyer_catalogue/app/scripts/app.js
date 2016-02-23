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
    'Authentication',
    'rzModule',
    'ui.bootstrap'
  ])
  .config(function ($routeProvider, $stateProvider, $urlRouterProvider, $httpProvider) {
      $routeProvider.otherwise('/');
      $stateProvider
      .state('society', {
          url : '/society',
          controller: 'CatalogueBaseCtrl',
          templateUrl: 'modules/pages/base/base.tmpl.html'
        })
        .state('campaign', {
          url : '/campaign/:campaignId', //:societyId/
          templateUrl: 'index.html',
          controller: ''
        })

        .state('campaign.societyList', {
          url : '/societyList', //:societyId/
          templateUrl: 'modules/pages/societylist/societylist.tmpl.html',
          controller: 'SocietyListCtrl'
        })

        .state('campaign.societyDetails', {
          url : '/societyDetails/:societyId', //:societyId/
          templateUrl: 'modules/pages/societydetails/societydetails.tmpl.html',
          controller: 'SocietyCtrl'
        })
        
        .state('campaign.societyList.filter', {
          url : '/societyList/:filter', //:societyId/for filter
          templateUrl: 'modules/pages/societylist/societylist.tmpl.html',
          controller: 'SocietyFilterCtrl'
        })

      .state('login', {
          url : '/login',
          controller: 'LoginCtrl',
          templateUrl: 'modules/pages/login/login.tmpl.html'
        })
      .state('manageCampaign', {
          url : '/manageCampaign',
          //controller: '',
          templateUrl: 'modules/pages/manageCampaign/manage-campaign.tmpl.html'
        })

      .state('manageCampaign.create', {
          url : '/create',
          controller: 'CreateCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/create/create-campaign.tmpl.html'
        })
      .state('manageCampaign.shortlisted', {
          url : '/shortlisted',
          controller: 'ShortlistedCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/shortlisted/shortlisted.tmpl.html'
        })
      .state('manageCampaign.shortlisted.societies', {
          url : '/:campaignId/societies',
          controller: 'ShortlistedSocietiesCtrl',
          templateUrl: 'modules/pages/manageCampaign/shortlisted/shortlisted-societies.tmpl.html'
        })

      .state('manageCampaign.requested', {
          url : '/requested',
          controller: 'RequestedCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/shortlisted/shortlisted.tmpl.html'
        })
      .state('manageCampaign.requested.societies', {
          url : '/:campaignId/societies',
          controller: 'RequestedSocietiesCtrl',
          templateUrl: 'modules/pages/manageCampaign/shortlisted/shortlisted-societies.tmpl.html'
        })

      .state('manageCampaign.finalized', {
          url : '/finalized',
          controller: 'FinalizedCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/shortlisted/shortlisted.tmpl.html'
        })
      .state('manageCampaign.finalized.societies', {
          url : '/:campaignId/societies',
          controller: 'FinalizedSocietiesCtrl',
          templateUrl: 'modules/pages/manageCampaign/shortlisted/shortlisted-societies.tmpl.html'
        })

      .state('manageCampaign.finalize', {
          url : '/finalize',
          controller: 'FinalizeCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/finalize/finalize.tmpl.html'
        })
      .state('manageCampaign.finalize.finalizeInventory', {
          url : '/:campaignId/finalizeInventory/',
          controller: 'FinalizeInventoryCtrl',
          templateUrl: 'modules/pages/manageCampaign/finalize/finalizeInventory.tmpl.html'
        })

      .state('society.details.poster', {
          url : '/poster', //:societyId/
          templateUrl: 'modules/common/postertab/poster-tab.tmpl.html',
          controller: ''
        })
      .state('society.details.info', {
          url : '/info', //:societyId/
          templateUrl: 'modules/common/infotab/societyinfo-tab.tmpl.html',
          controller: ''
        });

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
         /*$rootScope.globals.currentUser = AuthService.UserInfo();
         if (!$rootScope.globals.currentUser) {
           $location.path('/login');
         }
         else*/ if ($rootScope.globals.currentUser && $location.path() == '/logout')

         {
           AuthService.Logout();
           $location.path("/login");
         }
         else if ($rootScope.globals.currentUser && ($location.path() == '/login' || $location.path() == '/'))
         {
           $location.path("/manageCampaign/create");
         }
         else {
           $location.path(whence);
         }
       });
     }]);
