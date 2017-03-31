'use strict';

angular.module('catalogueApp')
.factory('campaignListService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',

function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

  var url_base = 'v0/ui/website/';
  var campaignListService = {};

  campaignListService.getCampaignDetails = function(assigned_by,userId,fetch_all){
    var url = url_base + "campaign-assignment/?include_assigned_by="+ assigned_by +  "&to="+userId + "&fetch_all=" + fetch_all;
      return machadaloHttp.get(url);
    }

  campaignListService.getAllCampaignDetails = function(fetch_all){
    var url = url_base + "campaign-assignment/?fetch_all=" + fetch_all;
      return machadaloHttp.get(url);
    }
  return campaignListService;
}]);
