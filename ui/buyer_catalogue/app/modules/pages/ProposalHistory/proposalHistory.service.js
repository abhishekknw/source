'use strict';


 angular.module('catalogueApp')
 .factory('proposalHistoryService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';

  	var proposalHistory = {};

  	proposalHistory.getProposalHistory = function(proposal_id){
  		// send proposal_id here
  		var url = url_base + proposal_id + '/getProposalVersion/';
  		return machadaloHttp.get(url);
  	}

  	return proposalHistory;
  	
}]);