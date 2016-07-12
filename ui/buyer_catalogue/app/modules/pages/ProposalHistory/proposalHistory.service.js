'use strict';


 angular.module('catalogueApp')
 .factory('proposalHistoryService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';

  	var proposalHistory = {};

  	proposalHistory.getProposalHistory = function(){
  		// send proposal_id here
  		var url = url_base + 'getProposalVersion/';
  		return machadaloHttp.get(url);
  	}

  	return proposalHistory;
  	
}]);