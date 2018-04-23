'use strict';


 angular.module('catalogueApp')
 .factory('proposalHistoryService', ['machadaloHttp','$stateParams','$rootScope','$routeParams', '$location',
  function (machadaloHttp, $stateParams, $rootScope, $routeParams, $location) {

  	var url_base = 'v0/ui/website/';
  	var proposalHistory = {};

  	proposalHistory.getProposalHistory = function(proposal_id){
      console.log(proposal_id);
      var url = url_base + "child-proposals/" + proposal_id + "/?account_id=0";
  		return machadaloHttp.get(url);
  	}
  	return proposalHistory;
}]);
