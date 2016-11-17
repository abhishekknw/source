"use strict";
angular.module('catalogueApp')
    .controller('CurrentProposal', function($scope, $rootScope, $stateParams, $window, $location, currentProposalService ,$http) {

    	$scope.proposal = {};
        $scope.society = {society_name:'',center:'',poster_count:'',standee_count:'',stall_count:'',status:''};
        $scope.societyDetails = [];
    	// send proposal_id in service

    	currentProposalService.getProposal($stateParams.proposal_id)
    	.success(function(response, status){
    		$scope.proposal = response;
    		console.log("inside proposal details : ", $scope.proposal);
    		for(var i=0;i<$scope.proposal.centers.length;i++){
    			var center = $scope.proposal.centers[i];
    			if(center.center.space_mappings.society_allowed)
    				for(var j=0;j<center.societies_buffered.length;j++)
    					center.societies_buffered[j].buffer_status = true;
    			// ADDNEW --> for corporates gyms and saloons
    		}
    	})
    	.error(function(response, status){
    		console.log("Error Occured");
    		if(typeof(response) == typeof([])){
    			console.log("Error response is :", response);
    		}
    	});

        $scope.edit = function(){
            $scope.showEdit = true;
        },

    	$scope.submit = function(){
    		currentProposalService.saveProposal($stateParams.proposal_id, $scope.proposal.centers)
    		.success(function(response, status){
                $window.location.reload();
    		})
    		.error(function(response, status){
    			console.log("Error Occured");
    			if(typeof(response) == typeof([])){
	    		console.log("Error response is :", response);
	    		}
    		})
    	}
     $scope.editInitialProposal = function(proposalId){
       $location.path('/' + proposalId + '/createproposal');
     }
    });
