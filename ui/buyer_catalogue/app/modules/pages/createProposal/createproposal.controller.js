"use strict";

angular.module('catalogueApp')
.controller('ProposalCtrl', function($scope, $rootScope, $q, $stateParams, $window, pagesService, createProposalService, $location,$http){

	console.log("Inside Controller");

	console.log("account_id : ", $stateParams.account_id);
	$scope.model = {}
	$scope.model.centers = new Array();

	$scope.addCenter = function(){
		var new_center = {
			center_name : '',
			address : '',
			latitude : '',
			longitude : '',
			radius : '',
			subarea : '',
			area  : '',
			city : '',
			pincode : '',
			space_mapping : {
				society_allowed : false,
				society_count : undefined,
				society_buffer_count : undefined,
				corporate_allowed : false,
				corporate_count : undefined,
				corporate_buffer_count : undefined,
				gym_allowed : false,
				gym_count : undefined,
				gym_buffer_count : undefined,
				salon_allowed : false,
				salon_count : undefined,
				salon_buffer_count : undefined,
			},
		}
		$scope.model.centers.push({
			center : new_center,
		});
	}

	$scope.addCenter();
	$scope.areas = [];
	$scope.sub_areas = [];

	createProposalService.loadInitialData()
    .success(function (response){
        $scope.cities = response.cities;
      });

     $scope.get_areas = function(id,index) {
     	var id = id;
			console.log(index);
      createProposalService.getLocations('areas', id,index)
      .success(function (response){
          $scope.areas[index] = response;
        });
    }
    $scope.get_sub_areas = function(id,index) {
      var id = id;
      createProposalService.getLocations('sub_areas', id)
      .success(function (response){
          $scope.sub_areas[index] = response;
        });
    }

	$scope.removeCenter = function(index){
		$scope.model.centers.splice(index,1);
	}

	$scope.checkSpace = function(center, space_name){
		console.log(center.center.space_mapping[space_name + '_allowed'])
		if(center.center.space_mapping[space_name + '_allowed']){
			center.center.space_mapping[space_name + '_count'] = 0;
			center.center.space_mapping[space_name + '_buffer_count'] = 0;
			center[space_name + '_inventory'] = {
				poster_allowed : false,
				standee_allowed : false,
				stall_allowed : false,
				flier_allowed : false,
				banner_allowed : false,
			};
			console.log(center[space_name + '_inventory']);
		}
		else{
			center.center.space_mapping[space_name + '_count'] = undefined;
			center.center.space_mapping[space_name + '_buffer_count'] = undefined;
			delete center[space_name + '_inventory']
		}
	}

	// $scope.

	$scope.submit = function(){
		//alert("hi1!!!!!!!!!");
		console.log("$scope.model", $scope.model);

		// call backend to save only if all the latitudes are found
			createProposalService.saveInitialProposal($stateParams.account_id, $scope.model)
			.success(function(response, status){
				$scope.errormsg = undefined;
				console.log("Successfully Saved");
				console.log("response is : ", response);
				$scope.proposal_id = response;
				createProposalService.setProposalId($scope.proposal_id);
				alert("Proposal created");
				$location.path('/' + $scope.proposal_id + '/mapview');

			})
			.error(function(response,status){
				console.log("Error");
				if(typeof(response) != typeof(12)){
					console.log("response is ", response);
					$scope.errormsg = response.message;
					$scope.model.centers = new Array();
					$scope.addCenter();
				}
			});
	}
});
