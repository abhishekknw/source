"use strict";
angular.module('catalogueApp')
    .controller('CurrentProposal', function($scope, $rootScope, $stateParams, $window, $location, currentProposalService ,$http) {

    	$scope.proposal = {};
      $scope.society = {society_name:'',center:'',poster_count:'',standee_count:'',stall_count:'',status:''};
      $scope.societyDetails = [];
      $scope.isParentProposal = $window.localStorage.parentProposal;// send proposal_id in service
      $scope.campaign_start_date;
      $scope.campaign_end_date;

      $scope.centerheaders = [
        {header : 'Serial No'},
        {header : 'Center Name'},
        {header : 'Area'},
        {header : 'SubArea'},
        {header : 'Radius'}
      ];
      var filters = {
        inv_poster:false,
        inv_stall:false,
        inv_standee:false,
        inv_flier:false,
      };
      //For date Functionality
      $scope.clear = function() {
        $scope.dt = null;
      };

      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;
      $scope.error = false;

      $scope.setDate = function(year, month, day) {
        $scope.dt = new Date(year, month, day);
      };

      $scope.sel_account_id = null;
      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];

    	currentProposalService.getProposal($stateParams.proposal_id)
    	.success(function(response, status){
    		$scope.proposal = response.data.proposal;
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

        // this service get the all shortlisted suppliers for this proposal
      currentProposalService.getShortlistedSuppliers($stateParams.proposal_id)
        .success(function(response, status){
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
      //function checks if center contain s suppliers_meta, if it contains then it collects it's inventory_type_selected filters
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
      // function used to show available inventory_type_selected filters
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
      //function used to select one center & also store selected center data to show details
      $scope.selectCenter = function(center_index){
        if(center_index != null){
          for(var i=0;i<$scope.center_id_list.length; i++){
            if($scope.center_id_list[i] == center_index){
                $scope.current_center_data = $scope.center_data[center_index];
            }
          }
        }
      }

      //Setting status of suppliers like shortlisted, removed or buffer
      $scope.setSupplierStatus = function (supplier,value){
        supplier.status = value;
      };
      //Function used to update the status of suppliers
      $scope.updateProposal = function() {
        $scope.current_center_data.proposal = $stateParams.proposal_id;
        currentProposalService.updateProposal($stateParams.proposal_id, $scope.current_center_data)
        .success(function(response, status){
                $window.location.reload();
        })
        .error(function(response, status){
          console.log("Error Occured");
        })
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
       $location.path('/' + $window.localStorage.account_id + '/createproposal');
     }
     $scope.showHistory = function(){
       $location.path('/' + $stateParams.proposal_id + '/showproposalhistory');
     }

     $scope.saveInvoiceDetails = function(){
       $scope.proposal.tentative_start_date = $scope.campaign_start_date;
       $scope.proposal.tentative_end_date = $scope.campaign_end_date;
      currentProposalService.saveInvoiceDetails($stateParams.proposal_id,$scope.proposal)
        .success(function(response, status){
                console.log("success");
        })
        .error(function(response, status){
          console.log("Error Occured");
        })
     }

    });//Controller ends here
