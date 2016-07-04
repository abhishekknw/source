"use strict";

angular.module('catalogueApp')
.controller('ProposalCtrl', function($scope, $rootScope, $window, createProposalService, $location,$http){

	$scope.model.centers = new Array();
	$scope.addCenter();
	$scope.addCenter();

	$scope.addCenter = function(){
		$scope.model.centers.push({
			center_name : '',
			address : '',
			latitude : '',
			longitude : '',
			radius : '',
			subarea : '',
			area  : '',
			city : 'Mumbai',
			pincode : '400072',
		});
	}

	console.log("Inside Controller");

	$scope.removeCenter = function(index){
		$scope.centers.splice(index,1);
	}

});