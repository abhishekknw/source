"use strict";
angular.module('catalogueApp')
.controller('ProposalCtrl', function($scope, $rootScope, $q, $stateParams, $window, pagesService, createProposalService, $location,$http){
	$scope.model = {}
	$scope.model.centers = new Array();
	$scope.society = 'RS';
	$scope.suppliers = [
		{name:"Societies", code:"RS", selected:"false"},
		{name:"Corporate Parks", code:"CP", selected:"false"},
	];
	$scope.proposalheaders = [
        {header : 'Advertising Location'},
        {header : 'Address'},
        {header : 'City'},
        {header : 'Area'},
        {header : 'SubArea'},
        {header : 'Pincode'},
        {header : 'Radius'},
        {header : 'Space Type'},
        {header : 'Action'}
      ];
  var count = 0;
  var suppliersData = new Array();
	$scope.addCenter = function(){
		// $scope.editProposal = false;
    suppliersData[count] = angular.copy($scope.suppliers);
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
			codes :[],
		}
		$scope.model.centers.push({
			center : new_center,
      suppliers : suppliersData[count],
			isEditProposal : true,
		});
    count++;
	}

	// $scope.addCenter();
	$scope.areas = [];
	$scope.sub_areas = [];

	if($window.localStorage.proposal_id != '0'){
		createProposalService.getProposal($window.localStorage.proposal_id)
		.success(function(response, status){
			$scope.model.name = response.data.name;
			$scope.model.tentative_cost = response.data.tentative_cost;
		})
		.error(function(response, status){
			console.log("Error Occured");
			if(typeof(response) == typeof([])){
				console.log("Error response is :", response);
			}
		});

		//for centers if proposal is editable
		createProposalService.getProposalCenters($window.localStorage.proposal_id)
		.success(function(response, status){
			$scope.centers = response.data;
			for(var i=0; i<$scope.centers.length; i++){
				$scope.addCenter();
				$scope.model.centers[i].center = $scope.centers[i];
				$scope.model.centers[i].center.pincode =  $scope.centers[i].pincode.toString();
				$scope.model.centers[i].isEditProposal = false;
				$scope.model.centers[i].center.codes = $scope.centers[i].codes;
				selectSuppliers($scope.model.centers[i].suppliers,$scope.centers[i].codes);
			}
		}).error(function(response, status){
			console.log("Error Occured");
			// alert("Error Occured");
		});
	}
	else {
			$scope.addCenter();
	}

	var selectSuppliers = function(space,codes){
		for(var i=0;i<codes.length;i++){
			for(var j=0;j<space.length; j++){
				if(codes[i] == space[j].code)
					space[j].selected = true;
			}
		}
	}
	createProposalService.loadInitialData()
    .success(function (response){
        $scope.cities = response.cities;
				$scope.loading = response;
      });
			//changes for searching societies on basis of area,subarea
  $scope.get_areas = function(id,index) {
     	var id = id;
			for(var i=0;i<$scope.cities.length;i++){
				if($scope.cities[i].id == id){
					$scope.model.centers[index].center.city = $scope.cities[i].city_name;
				}
			}
   createProposalService.getLocations('areas', id,index)
      .success(function (response){
          $scope.areas[index] = response;
        });
    }
  $scope.get_sub_areas = function(id,index) {
      var id = id;
			for(var i=0;i<$scope.areas[index].length;i++){
				if($scope.areas[index][i].id == id){
					$scope.model.centers[index].center.area = $scope.areas[index][i].label;
				}
			}
   createProposalService.getLocations('sub_areas', id)
      .success(function (response){
          $scope.sub_areas[index] = response;
        });
    }
	$scope.removeCenter = function(index){
		$scope.model.centers.splice(index,1);
    count--;
	}
	// code chnaged to send codes like RS,CP..etc
	$scope.checkSpace = function(supplier,center){
		if(supplier.selected == true)
			center.center.codes.push(supplier.code);
		else {
			var index = center.center.codes.indexOf(supplier.code);
			if(index > -1)
				center.center.codes.splice(index,1);
		}
	}
  var checkSupplierCode = function() {
    for(var i=0;i<$scope.model.centers.length;i++){
      if($scope.model.centers[i].center.codes.length <=0){
                return -1;
              }
    }
    return 0;
  }
	var convertPincodeToString = function(centers){
		for(var i=0;i<centers.length; i++){
			centers[i].center.pincode = centers[i].center.pincode.toString();
		}
	}
	$scope.submit = function(){
    var status = checkSupplierCode();
    if(status >= 0){
		$scope.model.account_id = $window.localStorage.account_id;
		$scope.model.business_id = $window.localStorage.business_id;
		$scope.model.parent = $window.localStorage.proposal_id;
		$scope.requestData = angular.copy($scope.model);
		convertPincodeToString($scope.requestData.centers);
		// call backend to save only if all the latitudes are found
			createProposalService.saveInitialProposal($stateParams.account_id, $scope.requestData)
			.success(function(response, status){
				console.log(response);
				$scope.errormsg = undefined;
				$scope.proposal_id = response.data;
				$scope.checkProposal = false;
				createProposalService.setProposalId($scope.proposal_id);
				console.log(response.data);
        $window.localStorage.isSavedProposal = false;
        $window.localStorage.parent_proposal_id = $scope.proposal_id;
				$location.path('/' + response.data + '/mapview');
			})
			.error(function(response,status){
				// alert("Error Occured");
				console.log("Error");
				if(typeof(response) != typeof(12)){
					console.log("response is ", response);
					$scope.errormsg = response.message;
					// $scope.model.centers = new Array();
					// $scope.addCenter();
				}
			});
    }
    else {
      alert("Please Provide Space Type");
    }
	}
});
