'use strict';


 angular.module('catalogueApp')
 .factory('ongoingCampaignService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

    var url_base = 'v0/ui/website/';
    var ongoingCampaignService = {};
    return ongoingCampaignService;

 }]);
