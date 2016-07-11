"use strict";

angular.module('catalogueApp')
.controller('CreateProposalCtrl', function($scope, $rootScope, $window, createProposalService, $location,$http){

	console.log("Inside Controller");

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
			city : 'Mumbai',
			pincode : '400072',
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
				saloon_allowed : false,
				saloon_count : undefined,
				saloon_buffer_count : undefined,
			},
		}
		$scope.model.centers.push({
			center : new_center,
		});
	}

	$scope.addCenter();

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

	$scope.submit = function(){
		console.log("$scope.model", $scope.model);
		createProposalService.saveInitialProposal($scope.model)
		.success(function(response, status){
			console.log("Successfully Saved");
		})
		.error(function(response,status){
			console.log("Error");
			if(typeof(response) != typeof(12)){
				console.log("response is ", response);
			}
		});
	}

});