"use strict";
angular.module('catalogueApp')
.controller('ProposalCtrl', function($scope, $rootScope, $q, $stateParams, $window, pagesService, createProposalService, $location,$http, constants,commonDataShare){
	$scope.loadingSpinner = true;
	$scope.model = {}
	$scope.model.centers = new Array();
	$scope.society = 'RS';
	$scope.suppliers = [
		{name:"Societies", code:"RS", selected:"false"},
		{name:"Corporate Parks", code:"CP", selected:"false"},
		{name:"Bus Shelter", code:"BS", selected:"false"},
		{name:"Gym", code:"GY", selected:"false"},
		{name:"Saloon", code:"SA", selected:"false"},
		{name:"Retail Shop", code:"RE", selected:"false"},
	];
	$scope.proposalheaders = [
        {header : 'Advertising Area'},
        {header : 'Location Address'},
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
		.then(function onSuccess(response){
			$scope.model.name = response.data.data.name;
			$scope.model.tentative_cost = response.data.data.tentative_cost;
		})
		.catch(function onError(response){
			console.log("Error Occured");
			commonDataShare.showErrorMessage(response);
		});

		//for centers if proposal is editable
		createProposalService.getProposalCenters($window.localStorage.proposal_id)
		.then(function onSuccess(response){
			$scope.centers = response.data.data;
			for(var i=0; i<$scope.centers.length; i++){
				$scope.addCenter();
				$scope.model.centers[i].center = $scope.centers[i];
				$scope.model.centers[i].center.pincode =  $scope.centers[i].pincode.toString();
				$scope.model.centers[i].isEditProposal = false;
				$scope.model.centers[i].center.codes = $scope.centers[i].codes;
				selectSuppliers($scope.model.centers[i].suppliers,$scope.centers[i].codes);
			}
		}).catch(function onError(response){
			console.log("Error Occured");
			commonDataShare.showErrorMessage(response);
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
    .then(function onSuccess(response){
        $scope.cities = response.data.cities;
				$scope.loading = response.data;
      }).catch(function onError(response){
				commonDataShare.showErrorMessage(response);
				console.log("Error occured");
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
      .then(function onSuccess(response){
          $scope.areas[index] = response.data;
        }).
        catch(function onError(response){
					commonDataShare.showErrorMessage(response);
        });
    }
  $scope.get_sub_areas = function(id,index) {
    console.log($scope.cities);
      var id = id;
			for(var i=0;i<$scope.areas[index].length;i++){
				if($scope.areas[index][i].id == id){
					$scope.model.centers[index].center.area = $scope.areas[index][i].label;
				}
			}
   createProposalService.getLocations('sub_areas', id)
      .then(function onSuccess(response){
          $scope.sub_areas[index] = response.data;
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
			if(centers[i].center.pincode)
				centers[i].center.pincode = centers[i].center.pincode.toString();
			else
				centers[i].center.pincode = '';
			}
	}
	$scope.submit = function(){
	    var status = checkSupplierCode();
	    if(status >= 0){
			$scope.model.account_id = $stateParams.account_id;
			$scope.model.organisation_id = $window.localStorage.organisationId;
			// $scope.model.parent = $window.localStorage.proposal_id;
			$scope.requestData = angular.copy($scope.model);
			console.log($scope.requestData);
			convertPincodeToString($scope.requestData.centers);
			// call backend to save only if all the latitudes are found
			if($scope.requestData.centers.length > 1){
				$scope.loadingSpinner = false;
				createProposalService.saveInitialProposal($stateParams.account_id, $scope.requestData)
				.then(function onSuccess(response){
					console.log(response);
					$scope.errormsg = undefined;
					$scope.proposal_id = response.data.data;
					$scope.checkProposal = false;
					createProposalService.setProposalId($scope.proposal_id);
	        $window.localStorage.isSavedProposal = false;
	        $window.localStorage.parent_proposal_id = $scope.proposal_id;
					$location.path('/' + response.data.data + '/mapview');
				})
				.catch(function onError(response){
					$scope.loadingSpinner = true;
					commonDataShare.showErrorMessage(response);
					// swal(constants.name,constants.geo_location_error,constants.error);
					console.log("Error");
					if(typeof(response) != typeof(12)){
						console.log("response is ", response);
						$scope.errormsg = response.message;
						// $scope.model.centers = new Array();
						// $scope.addCenter();
					}
				});
			}else {
				swal({
					 title: 'Are you sure ?',
					 text: constants.center_warning,
					 type: constants.warning,
					 showCancelButton: true,
					 confirmButtonClass: "btn-success",
					 confirmButtonText: "Yes, Continue!",
					 closeOnConfirm: true
				 },
				 function(){
					 $scope.loadingSpinner = false;
					 createProposalService.saveInitialProposal($stateParams.account_id, $scope.requestData)
		 			.then(function onSuccess(response){
						console.log(response);
		 				$scope.errormsg = undefined;
		 				$scope.proposal_id = response.data.data;
		 				$scope.checkProposal = false;
		 				createProposalService.setProposalId($scope.proposal_id);
		         $window.localStorage.isSavedProposal = false;
		         $window.localStorage.parent_proposal_id = $scope.proposal_id;
		 				$location.path('/' + response.data.data + '/mapview');
		 			})
		 			.catch(function onError(response){
		 				$scope.loadingSpinner = true;
						commonDataShare.showErrorMessage(response);
						// 	swal(constants.name,constants.geo_location_error,constants.error);
		 				console.log("Error");
		 				if(typeof(response) != typeof(12)){
		 					console.log("response is ", response);
		 					$scope.errormsg = response.message;
		 					// $scope.model.centers = new Array();
		 					// $scope.addCenter();
		 				}
		 			});
				 })
			}
	    }
	    else {
	      alert("Please Provide Space Type");
				$scope.loadingSpinner = true;
	    }
		}
});
