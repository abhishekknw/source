"use strict";
angular.module('catalogueApp')
    .controller('ProposalHistory', function($scope, $rootScope, $stateParams, $window, $location, proposalHistoryService ,$http) {
    	$scope.proposals = [];
      var proposalid = $window.localStorage.proposal_id;
    	proposalHistoryService.getProposalHistory(proposalid)
    	.success(function(response, status){
    		$scope.proposals = response.data;
    		console.log("$scope.proposals : ", response.data);
    	})
    	.error(function(response, status){
    		console.log("error occured");
    	});
      $scope.showDetails = function(proposal_id){
        $window.localStorage.parentProposal = false;
        $location.path('/' + proposal_id + '/showcurrentproposal');
      }
	});
