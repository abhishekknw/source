 'use strict';
 angular.module('catalogueApp')
 .factory('releaseCampaignService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location', '$http',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location, $http) {

    var url_base = 'v0/ui/website/';
    var releaseCampaignService = {};


    releaseCampaignService.getCampaignReleaseDetails = function(proposal_id){
         var url = url_base + "proposal/"+ proposal_id + "/";
    	return machadaloHttp.get(url);
    }

    return releaseCampaignService;
}]);
