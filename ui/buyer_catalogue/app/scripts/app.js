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
    // 'ngAnimate',
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
    'ui.bootstrap',
    'angular.filter',
    'angularUtils.directives.dirPagination',
    'angularjs-dropdown-multiselect',
    'ngFileUpload',
    'uiGmapgoogle-maps',
    'ncy-angular-breadcrumb',
    'slickCarousel',
  ])
  .config(function ($routeProvider, $stateProvider, $urlRouterProvider, $httpProvider, $qProvider, $locationProvider) {
      $stateProvider
      .state('society', {
          url : '/society',
          controller: 'CatalogueBaseCtrl',
          templateUrl: 'modules/pages/base/base.tmpl.html'
        })
        .state('campaign', {
          url : '/campaign/:campaignId',
          templateUrl: 'index.html',
          controller: ''
        })
        .state('campaign.societyList', {
          url : '/societyList', //:societyId/
          templateUrl: 'modules/pages/societylist/societylist.tmpl.html',
          controller: 'SocietyListCtrl'
        })
          .state('MapView',{
           url : '/:proposal_id/mapview',
           templateUrl : 'modules/pages/mapview/mapview.tmpl.html',
           controller : 'MapCtrl',
           ncyBreadcrumb: {
             label:'mapview',
             parent: function($rootScope) {
              return $rootScope.getCurState();
            },
           }
        })
        .state('createProposalMe',{
          url : '/:account_id/createproposal',
          templateUrl : 'modules/pages/createProposal/createproposal.tmpl.html',
          controller : 'ProposalCtrl',
          ncyBreadcrumb: {
            label:'createProposal',
            parent: 'manageCampaign.create'
          }
        })
        .state('showCurrentProposal',{
           url : '/:proposal_id/showcurrentproposal',
           templateUrl : 'modules/pages/currentProposal/currentProposal.tmpl.html',
           controller : 'CurrentProposal',
           ncyBreadcrumb: {
             label:'proposalSummary',
             parent : 'manageCampaign.create'
           }
        })
        .state('showProposalHistory',{
          url : '/:proposal_id/showproposalhistory',
          templateUrl : 'modules/pages/ProposalHistory/proposalHistory.tmpl.html',
          controller : 'ProposalHistory',
          ncyBreadcrumb: {
            label:'proposalHistory',
            parent : 'manageCampaign.create'
          }
        })
        .state('campaign.societyDetails', {
          url : '/societyDetails/:societyId', //:societyId/
          templateUrl: 'modules/pages/societydetails/societydetails.tmpl.html',
          controller: 'SocietyCtrl'
        })
        .state('campaign.societyList.filter', {
          url : '/societyList/:filter',
          templateUrl: 'modules/pages/societylist/societylist.tmpl.html',
          controller: 'SocietyFilterCtrl'
        })
        .state('showSocietyDetails', {
          url : '/societyDetails/:societyId',
          templateUrl: 'modules/pages/supplierDetails/societyDetails/newsocietyDetails.tmpl.html',
          controller: 'NewSocietyCtrl'
        })
      .state('login', {
          url : '/login',
          controller: 'LoginCtrl',
          templateUrl: 'modules/pages/login/login.tmpl.html'
        })
      .state('manageCampaign', {
          url : '/manageCampaign',
          controller: 'CreateCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/manage-campaign.tmpl.html',
          ncyBreadcrumb: {
            skip: true // Never display this state in breadcrumb.
          }
        })
      .state('manageCampaign.create', {
          url : '/create',
          controller: 'CreateCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/create/create-campaign.tmpl.html',
          ncyBreadcrumb: {
            label: 'Home page'
          }
        })
      .state('manageCampaign.createaccount', {
            url : '/createAccount',
            controller: 'CreateAccountCtrl',
            templateUrl: 'modules/pages/manageCampaign/createaccount/create-account.tmpl.html',
            ncyBreadcrumb: {
              label: 'Create Account',
              parent : 'manageCampaign.create'
            }

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
      .state('manageCampaign.finalized.finalbooking', {
          url : '/:campaignId/finalbooking',
          controller: 'FinalBookingCampaignCtrl',
          templateUrl: 'modules/pages/manageCampaign/finalbooking/finalbooking.tmpl.html'
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
        .state('manageCampaign.release', {
            url : '/release',
            controller: 'ReleaseCampaignCtrl',
            templateUrl: 'modules/pages/manageCampaign/release/release-campaign.tmpl.html'
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
        })
      .state('manageCampaign.ongoingcampaign', {
            url : '/ongoingcampaign',
            controller: 'OngoingCampaignCtrl',
            templateUrl: 'modules/pages/manageCampaign/ongoingcampaign/ongoing-campaign.tmpl.html'
          })
      .state('mapView',{
            url : '/mapview',
            controller : 'MapCtrl',
            templateUrl : 'modules/pages/mapview/mapview.tmpl.html',
        })
      .state('releasePlan',{
           url : '/:proposal_id/releasePlan',
           controller : 'ReleaseCampaignCtrl',
           templateUrl : 'modules/pages/releaseCampaignPlan/releaseCampaign.tmpl.html',
           ncyBreadcrumb: {
             label:'ReleasePlan',
             parent : 'OpsDashBoard'
           }
       })
      .state('OpsDashBoard',{
           url : '/OpsDashBoard',
           controller : 'OpsDashCtrl',
           templateUrl : 'modules/pages/DashBoard/OperationsDashBoard/opsdashboard.tmpl.html',
           ncyBreadcrumb: {
             label:'DashBoard',
             parent : 'manageCampaign.create'
           }
       })
      .state('manageUsers',{
           url : '/manageUser',
           controller : 'userCtrl',
           templateUrl : 'modules/pages/manageUsers/user.tmpl.html'
       })
      .state('auditReleasePlan',{
            url : '/:proposal_id/auditReleasePlan',
            controller : 'AuditReleasePlanCtrl',
            templateUrl : 'modules/pages/operations/auditReleasePlan/auditReleasePlan.tmpl.html',
            ncyBreadcrumb: {
              label:'AuditReleasePlan',
              parent : 'releasePlan'
            }
      })
      .state('opsExecutionPlan',{
            url : '/:proposal_id/opsExecutionPlan',
            controller : 'OpsExecutionPlanCtrl',
            templateUrl : 'modules/pages/operations/opsExecutionPlan/opsExecutionPlan.tmpl.html',
            ncyBreadcrumb: {
              label:'ExecutionPlan',
              parent : 'OpsDashBoard'
            }
      })
      .state('guestHomePage',{
            url : '/guestHomePage',
            controller : 'guestHomePageController',
            templateUrl : 'modules/pages/guestPage/homepage.tmpl.html',
            ncyBreadcrumb: {
              label:'Homepage',
            }
      });
      //$qProvider.errorOnUnhandledRejections(false);
      $locationProvider.hashPrefix('');
})
.run(['$rootScope', '$window', '$location', 'AuthService','$state',
     function ($rootScope, $window, $location, AuthService, $state) {
       $rootScope.globals = $rootScope.globals || {};
       $rootScope.globals.currentUser = AuthService.UserInfo();
       $rootScope.getCurState = function() {
            if($window.localStorage.isSavedProposal == 'true')
              return 'showCurrentProposal';
            else if($window.localStorage.isSavedProposal == 'false')
              return 'createProposalMe';
            else if($window.localStorage.user_code == 'guestUser')
              return 'guestHomePage';
        }
       var whence = $location.path();
       $rootScope.$on('$locationChangeStart', function (event, next, current) {
         var whence = $location.path();
         console.log("location change start - Whence: " + whence);

         // redirect to login page if not logged in
         $rootScope.globals.currentUser = AuthService.UserInfo();
         if (!$rootScope.globals.currentUser) {
           $location.path('/login');
         }else if ($rootScope.globals.currentUser && $location.path() == '/guestHomePage') {
           $location.path("/guestHomePage");
         }else if ($rootScope.globals.currentUser && $location.path() == '/logout'){
           AuthService.Logout();
           $location.path("/login");
         }else if ($rootScope.globals.currentUser && ($location.path() == '/login' || $location.path() == '/') && ($window.localStorage.user_code != 'guestUser')){
           $location.path("/manageCampaign/create");
         }else {
           $location.path(whence);
         }
       });
     }]);
