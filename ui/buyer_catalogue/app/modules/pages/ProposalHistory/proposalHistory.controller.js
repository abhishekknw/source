"use strict";
angular.module('catalogueApp')
    .controller('ProposalHistory', function($scope, $rootScope, $stateParams, $window, $location, proposalHistoryService ,$http) {
    	$scope.proposals = [];
      //defining headers for table
      $scope.proposalHeaders = [
        {name : 'Proposal_id'},
        {name : 'Proposal_name'},
        {name : 'Created By'},
        {name : 'Created On'},
        {name : ''}
      ];
      // var proposalid = $window.sessionStorage.proposal_id;
      $scope.proposalid = $window.sessionStorage.proposal_id;
    	proposalHistoryService.getProposalHistory($scope.proposalid)
    	.success(function(response, status){
    		$scope.proposals = response.data;
        $scope.loading = response;
    		console.log("$scope.proposals : ", response.data);
    	})
    	.error(function(response, status){
    		console.log("error occured");
    	});
      $scope.showDetails = function(proposal_id){
        $window.sessionStorage.parentProposal = false;
        $location.path('/' + proposal_id + '/showcurrentproposal');
      }
      $scope.showHistory = function(){
        $location.path('/manageCampaign/create');
      }
	});
