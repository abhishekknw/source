'use strict';


 angular.module('catalogueApp')
 .factory('proposalHistoryService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';
  	var proposalHistory = {};

  	proposalHistory.getProposalHistory = function(proposal_id){
  		var url = url_base + "proposal/" + proposal_id + '/child_proposals/';
  		return machadaloHttp.get(url);
  	}
  	return proposalHistory;
}]);
