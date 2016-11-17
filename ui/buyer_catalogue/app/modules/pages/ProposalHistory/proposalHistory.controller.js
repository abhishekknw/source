"use strict";
angular.module('catalogueApp')
    .controller('ProposalHistory', function($scope, $rootScope, $stateParams, $window, $location, proposalHistoryService ,$http) {
    	$scope.proposals = [];
      var proposalidtest = 'LPkKDMxa';//Hard coded for intial development need to be made dynamic
    	proposalHistoryService.getProposalHistory(proposalidtest)
    	.success(function(response, status){
    		$scope.proposals = response.data;
    		console.log("$scope.proposals : ", response.data);
    	})
    	.error(function(response, status){
    		console.log("error occured");
    	});
	});
