"use strict";
angular.module('catalogueApp')
    .controller('CurrentProposal', function($scope, $rootScope, $stateParams, $window, $location, currentProposalService ,$http) {

    	$scope.proposal = {};
        $scope.society = {society_name:'',center:'',poster_count:'',standee_count:'',stall_count:'',status:''};
        $scope.societyDetails = [];
    	// send proposal_id in service

    	currentProposalService.getProposal($stateParams.proposal_id)
    	.success(function(response, status){
    		$scope.proposal = response.data;
    		console.log("inside proposal details : ", $scope.proposal);
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

        currentProposalService.getShortlistedSuppliers($stateParams.proposal_id)
        .success(function(response, status){
          console.log(response);
          $scope.center_data = response.data;
          getAvailableSuppliers($scope.center_data);
          getFilters($scope.center_data);
        })
        .error(function(response, status){
          console.log("Error Occured");
          if(typeof(response) == typeof([])){
            console.log("Error response is :", response);
          }
        });
        var filters = {
          inv_poster:false,
          inv_stall:false,
          inv_standee:false,
          inv_flier:false,
        };
        // function added to show suppliers selected in centers and to show filters
        var getAvailableSuppliers = function(spaces){
          $scope.center_id_list = Object.keys($scope.center_data);
          angular.forEach(spaces, function(supplier) {
            supplier.filters = {};
            if('RS' in supplier.suppliers){
              supplier.filters.society_allowed = true;
              supplier.societyFilters = angular.copy(filters);
            }
            if('CP' in supplier.suppliers){
              supplier.filters.corporate_allowed = true;
              supplier.corporateFilters = angular.copy(filters);
            }
          });
        }
        var getFilters = function(spaces){
          angular.forEach(spaces, function(supplier) {
            if(supplier.suppliers_meta){
              if(supplier.suppliers_meta['RS']){
                var Filters = supplier.suppliers_meta['RS'].inventory_type_selected;
                checkInventories(supplier.societyFilters,Filters);
              }
              if(supplier.suppliers_meta['CP']){
                var Filters = supplier.suppliers_meta['CP'].inventory_type_selected;
                checkInventories(supplier.corporateFilters,Filters);
              }
            }
          });
        }
        var checkInventories = function(supplier,filters){
          if((filters.indexOf('PO') > -1) || (filters.indexOf('POFL') > -1) || (filters.indexOf('POSLFL') > -1) || (filters.indexOf('POCDFL') > -1)){
            supplier.inv_poster = true;
          }
          if((filters.indexOf('ST') > -1) || (filters.indexOf('STFL') > -1) || (filters.indexOf('STSLFL') > -1) || (filters.indexOf('STCDFL') > -1)){
            supplier.inv_standee = true;
          }
          if((filters.indexOf('SL') > -1) || (filters.indexOf('SLFL') > -1) || (filters.indexOf('POSLFL') > -1) || (filters.indexOf('STSLFL') > -1)){
            supplier.inv_stall = true;
          }
          if((filters.indexOf('FL') > -1) || (filters.indexOf('POFL') > -1) || (filters.indexOf('STFL') > -1) || (filters.indexOf('SLFL') > -1) || (filters.indexOf('CDFL') > -1) || (filters.indexOf('POSLFL') > -1) || (filters.indexOf('STSLFL') > -1) || (filters.indexOf('POCDFL') > -1) || (filters.indexOf('STCDFL') > -1)){
            supplier.inv_flier = true;
          }
        }
        $scope.current_center_id = null;

        $scope.selectCenter = function(center_index){
          if(center_index != null){
            for(var i=0;i<$scope.center_id_list.length; i++){
              if($scope.center_id_list[i] == center_index){
                $scope.current_center_data = $scope.center_data[center_index];
              }
            }
          }
        }
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
       $window.localStorage.proposal_id = proposalId;
       $location.path('/' + proposalId + '/createproposal');
     }
    });
