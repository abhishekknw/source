"use strict";
angular.module('catalogueApp')
    .controller('CurrentProposal', function($scope, $rootScope, $window, $location, currentProposalService ,$http) {

    	console.log('hi');
    	$scope.proposal = {};

    	// send proposal_id in service
    	currentProposalService.getProposal()
    	.success(function(response, status){
    		$scope.proposal = response;
    		console.log("$scope.proposal : ", $scope.proposal);
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



    	$scope.submit = function(){
    		console.log("$scope.proposal : ", $scope.proposal);
    		currentProposalService.saveProposal($scope.proposal.centers)
    		.success(function(response, status){
    			console.log("Successfully Saved");
    		})
    		.error(function(response, status){
    			console.log("Error Occured");
    			if(typeof(response) == typeof([])){
	    			console.log("Error response is :", response);
	    		}
    		})
    	}

    });