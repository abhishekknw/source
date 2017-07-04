'use strict';


 angular.module('catalogueApp')
 .factory('upcomingCampaignService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';
    var upcomingCampaignService = {};
    return upcomingCampaignService;

 }]);
