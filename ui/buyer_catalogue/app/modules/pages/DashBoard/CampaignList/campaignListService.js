'use strict';

angular.module('catalogueApp')
.factory('campaignListService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',

function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

  var url_base = 'v0/ui/website/';
  var campaignListService = {};

  campaignListService.getCampaignDetails = function(userId){
    var url = url_base + "campaign-assignment/?include_assigned_by=0&to="+userId;
      return machadaloHttp.get(url);
    }

  return campaignListService;
}]);
