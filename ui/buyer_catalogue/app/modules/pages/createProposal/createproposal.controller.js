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
  var count = 0;
  var suppliersData = new Array();
	$scope.addCenter = function(){
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
			supplier_codes :[],
			space_mapping : {
				society_allowed : false,
				corporate_allowed : false,
				gym_allowed : false,
				salon_allowed : false,
			},
		}
		$scope.model.centers.push({
			center : new_center,
      suppliers : suppliersData[count],
		});
    count++;
	}

	$scope.addCenter();
	$scope.areas = [];
	$scope.sub_areas = [];

	createProposalService.loadInitialData()
    .success(function (response){
			console.log(response);
        $scope.cities = response.cities;
				console.log($scope.cities);
      });
			//changes for searching societies on basis of area,subarea
  $scope.get_areas = function(id,index) {
     	var id = id;
			console.log($scope.cities);
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
	// code chnaged to send supplier_codes like RS
	$scope.checkSpace = function(supplier,center){
		if(supplier.selected == true)
			center.center.supplier_codes.push(supplier.code);
		else {
			var index = center.center.supplier_codes.indexOf(supplier.code);
			if(index > -1)
				center.center.supplier_codes.splice(index,1);
		}
		// if(center.center.space_mapping[space_name + '_allowed']){
		// 	center.center.space_mapping[space_name + '_count'] = 0;
		// 	center.center.space_mapping[space_name + '_buffer_count'] = 0;
		// 	center[space_name + '_inventory'] = {
		// 		poster_allowed : false,
		// 		standee_allowed : false,
		// 		stall_allowed : false,
		// 		flier_allowed : false,
		// 		banner_allowed : false,
		// 	};
		// 	console.log(center[space_name + '_inventory']);
		// }else{
		// 	center.center.space_mapping[space_name + '_count'] = undefined;
		// 	center.center.space_mapping[space_name + '_buffer_count'] = undefined;
		// 	delete center[space_name + '_inventory']
		// }
	}
  var checkSupplierCode = function() {
    for(var i=0;i<$scope.model.centers.length;i++){
      if($scope.model.centers[i].center.supplier_codes.length <=0){
        console.log($scope.model.centers[i].center.supplier_codes.length);
                return -1;
              }
    }
    return 0;
  }
	$scope.submit = function(){
    var status = checkSupplierCode();
    if(status >= 0){
		$scope.model.account_id = $window.localStorage.account_id;
		$scope.model.business_id = $window.localStorage.business_id;
		$scope.model.parent = $window.localStorage.proposal_id;
		console.log("vidhi inside submit", $scope.model);
		// call backend to save only if all the latitudes are found
			createProposalService.saveInitialProposal($stateParams.account_id, $scope.model)
			.success(function(response, status){
				console.log($scope.model.data);
				$scope.errormsg = undefined;
				console.log("Successfully Saved");
				console.log("response is : ", response);
				$scope.proposal_id = response;
				createProposalService.setProposalId($scope.proposal_id);
				$location.path('/' + response.data + '/mapview');
			})
			.error(function(response,status){
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
