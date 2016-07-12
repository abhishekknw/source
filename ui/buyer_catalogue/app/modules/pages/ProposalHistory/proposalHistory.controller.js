"use strict";
angular.module('catalogueApp')
    .controller('ProposalHistory', function($scope, $rootScope, $stateParams, $window, $location, proposalHistoryService ,$http) {

    	$scope.proposals = [];
        
    	proposalHistoryService.getProposalHistory($stateParams.proposal_id)
    	.success(function(response, status){
    		$scope.proposals = response;
    		console.log("$scope.proposals : ", $scope.proposals);
    	})
    	.error(function(response, status){
    		console.log("error occured");
    	});

	});
