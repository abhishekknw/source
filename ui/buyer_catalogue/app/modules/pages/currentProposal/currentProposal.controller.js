"use strict";
angular.module('catalogueApp')
    .controller('CurrentProposal', function($scope, $rootScope, $stateParams, $window, $location, currentProposalService ,$http) {

    	console.log('hi');
    	$scope.proposal = {};
        $scope.society = {society_name:'',center:'',poster_count:'',standee_count:'',stall_count:'',status:''};
        $scope.societyDetails = [];
    	// send proposal_id in service

    	currentProposalService.getProposal($stateParams.proposal_id)
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
            // alert("hi!! " + $scope.proposal.centers[0].societies_shortlisted);
            // var k=0;
            // var center_name;
            // loop1:
            // for(var i=0; i<$scope.proposal.centers.length; i++){
            //     center_name = $scope.proposal.centers[i].center.center_name;
            //     loop2:   
            //     for(var j=0; j<$scope.proposal.centers[i].societies_shortlisted.length; j++) {
            //         $scope.societyDetails[k]={};
            //         $scope.societyDetails.push($scope.society);
            //         // $scope.societyDetails.push({society_name:'',center:'',poster_count:'',standee_count:'',stall_count:'',status:''});
            //         $scope.societyDetails[k].center = center_name;
            //         $scope.societyDetails[k].society_name = $scope.proposal.centers[i].societies_shortlisted[j].society_name; 
            //         if(k==9)
            //             {
            //                 break loop1;
            //             }

            //             $scope.societyDetails[k].standee_count = $scope.proposal.inventory[k].total_standee_count;
            //             $scope.societyDetails[k].stall_count = $scope.proposal.inventory[k].total_stall_count;
            //             if($scope.proposal.inventory[k].shortlisted == true)
            //                 $scope.societyDetails[k].status = "Shortlisted";
            //             else
            //                 $scope.societyDetails[k].status = "Buffered";   
            //         k++;
            //     }
            // }
    	})
    	.error(function(response, status){
    		console.log("Error Occured");
    		if(typeof(response) == typeof([])){
    			console.log("Error response is :", response);
    		}
    	});

        console.log("proposal_id is : ", $stateParams.proposal_id);


        $scope.edit = function(){
            $scope.showEdit = true;
        },

    	$scope.submit = function(){
    		console.log("$scope.proposal : ", $scope.proposal);
    		currentProposalService.saveProposal($stateParams.proposal_id, $scope.proposal.centers)
    		.success(function(response, status){
    			console.log("Successfully Saved");
                $window.location.reload();
    		})
    		.error(function(response, status){
    			console.log("Error Occured");
    			if(typeof(response) == typeof([])){
	    			console.log("Error response is :", response);
	    		}
    		})
    	}

    });