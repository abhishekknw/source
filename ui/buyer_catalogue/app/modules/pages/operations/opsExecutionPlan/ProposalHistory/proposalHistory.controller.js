"use strict";
angular.module('catalogueApp')
    .controller('ProposalHistory', function($scope, $rootScope, $stateParams, $window, $location, proposalHistoryService ,$http) {
    	$scope.proposals = [];
      $(document).ready(function(){
        $('.my').slick({
          infinite: true,
         slidesToShow: 3,
         slidesToScroll: 3
        });
      });
      //defining headers for table
      $scope.proposalHeaders = [
        {name : 'Proposal_id'},
        {name : 'Proposal_name'},
        {name : 'Created By'},
        {name : 'Created On'},
        {name : ''}
      ];
      // var proposalid = $window.localStorage.proposal_id;
      $scope.proposalid = $stateParams.proposal_id;
      $stateParams.proposal_id;
      console.log($scope.proposalid);
    	proposalHistoryService.getProposalHistory($stateParams.proposal_id)
    	.then(function(response, status){
    		$scope.proposals = response.data.data;
        $scope.loading = response.data;
    		console.log("$scope.proposals : ", response.data.data);
    	})
    	.catch(function(response, status){
    		console.log("error occured");
    	});
      $scope.showDetails = function(proposal_id){
        $window.localStorage.parentProposal = false;
        $location.path('/' + proposal_id + '/showcurrentproposal');
      }
      $scope.showHistory = function(){
        $location.path('/manageCampaign/create');
      }
	});
