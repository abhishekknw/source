angular.module('catalogueApp')
.controller('OpsExecutionPlanCtrl',
    ['$scope', '$rootScope', '$window', '$location','opsExecutionPlanService','$stateParams','commonDataShare','errorHandler',
    function ($scope, $rootScope, $window, $location, opsExecutionPlanService, $stateParams,commonDataShare,errorHandler) {
      $scope.campaign_id = $stateParams.proposal_id;
      $scope.headings = [
        {header : 'Supplier Id'},
        {header : 'Inventory Id'},
        {header : 'Inventory Type'},
        {header : 'Image'},
         {header : 'Activity Name'},
        {header : 'Activity Date'},
        {header : 'ReAssign'},
        {header : 'ReAssigned User'},
        {header : 'ReAssigned Date'},
      ];
      $scope.supplier_headings = [
        {header : 'Supplier Id'},
        {header : 'Supplier Name'},
        {header : 'Area'},
        {header : 'SubArea'},
        {header : 'City'},
        {header : 'State'},
         {header : 'PinCode'},
      ];
      $scope.dates = [
        {header:''},
        {header:'Total'},
        {header:'Actual'},
        {header:'Percentage'},
      ];
      $scope.summaryHeaders = [
        {header:'Release', key:'RELEASE'},
        {header:'Audit',   key:'AUDIT'},
        {header:'Closure', key:'CLOSURE'},
      ];

      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      // $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.formats = ['yyyy-MM-dd'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];
      var getOpsExecutionImageDetails = function(){
        opsExecutionPlanService.getOpsExecutionImageDetails($scope.campaign_id)
        	.success(function(response, status){
        		$scope.campaignData = response.data;
            createList();
            console.log('vidhi', $scope.campaignData);
            if($scope.campaignData.length == 0)
              $scope.hideData = false;//change to true doing for testing
                $scope.loading = response;
        	})
        	.error(function(response, status){
            $scope.hideData = true;
        		console.log("error occured", status);
        	});
        }
        var getUsersList = function(){
          commonDataShare.getUsersList()
            .success(function(response, status){
              console.log(response);
              $scope.userList = response.data;
            })
            .error(function(response, status){
              console.log("error occured", status);
            });
        }
        var init = function(){
          getOpsExecutionImageDetails();
          getUsersList();
        }
      init();
      var campaignDataStruct = {
        id : '',
        supplier_id : '',
        inv_id : '',
        inv_type : '',
        images : [],
        act_name : '',
        act_date : '',
        reAssign_date : '',
      };
      $scope.campaignDataList = [];
      function createList(){
        angular.forEach($scope.campaignData.shortlisted_suppliers,function(suppliers,spaceId){
          angular.forEach($scope.campaignData.shortlisted_inventories,function(inventories,invId){
            if($scope.campaignData.shortlisted_inventories[invId].shortlisted_spaces_id == spaceId){
              angular.forEach($scope.campaignData.inventory_activities,function(activities,actId){
                if($scope.campaignData.inventory_activities[actId].shortlisted_inventory_id == invId){
                  angular.forEach($scope.campaignData.inventory_activity_assignment,function(invAssignments,assignId){
                    if($scope.campaignData.inventory_activity_assignment[assignId].inventory_activity_id == actId){
                      var data = angular.copy(campaignDataStruct);
                      data.id = assignId;
                      data.supplier_id = $scope.campaignData.shortlisted_suppliers[spaceId].supplier_id;
                      data.inv_id = $scope.campaignData.shortlisted_inventories[invId].inventory_id;
                      data.inv_type = $scope.campaignData.shortlisted_inventories[invId].inventory_name;
                      data.act_name = $scope.campaignData.inventory_activities[actId].activity_type;
                      data.act_date = $scope.campaignData.inventory_activity_assignment[assignId].activity_date;
                      data.reAssign_date = $scope.campaignData.inventory_activity_assignment[assignId].reassigned_activity_date;
                      angular.forEach($scope.campaignData.images, function(images,imgKey){
                        if($scope.campaignData.images[imgKey].inventory_activity_assignment_id == assignId){
                          data.images.push($scope.campaignData.images[imgKey]);
                        }
                      });
                      // data.reAssigner_user = $scope.campaignData.inventory_activity_assignment[assignId].assigned_to;
                      $scope.campaignDataList.push(data);
                    }
                  });
                }
              });
            }
          });
        });
      }
      $scope.setImageUrl = function(images){
        $scope.imageUrlList = [];
        for(var i=0; i<images.length; i++){
          var imageData = {
            image_url : 'http://androidtokyo.s3.amazonaws.com/' + images[i].image_path,
            comment : images[i].comment,
          };
          $scope.imageUrlList.push(imageData);
        }
      }
      $scope.getSupplierDetails = function(supplier){
        $scope.supplierData = [];
        var supplierId = supplier.shortlisted_inventory_details.shortlisted_supplier.object_id;
        var supplier_type_code = 'RS';
        opsExecutionPlanService.getSuppierDetails(supplierId,supplier_type_code)
        	.success(function(response, status){
            $scope.supplierData = response.data;
      	   })
        	.error(function(response, status){
        		console.log("error occured", status);
        	});
      }
      $scope.getSummary = function(){
        opsExecutionPlanService.getSummaryDetails($scope.campaign_id)
        .success(function(response, status){
          $("#summaryModal").modal('show');
          $scope.summaryData = response.data;
        })
        .error(function(response, status){
          console.log(response);
        });
      }
      $scope.reAssignActivityList = {};
      $scope.activity_date;
      $scope.userCode;
      $scope.addActivity = function(index,inventory){
        if(inventory.status == true){
          $scope.reAssignActivityList[inventory.id] = {};
        }else {
          delete $scope.reAssignActivityList[inventory.id];
        }
      }
      var reAssignActivityData = function(){
        console.log($scope.reAssignActivityList);
        angular.forEach($scope.reAssignActivityList, function(activity, assignId){
          $scope.reAssignActivityList[assignId]['reassigned_activity_date'] = commonDataShare.formatDate($scope.activity_date);
          $scope.reAssignActivityList[assignId]['assigned_to'] = $scope.userCode;
          //use above after getting userList
          // $scope.reAssignActivityList[assignId]['assigned_to'] = 6;
        });
      }
      $scope.saveReAssignedActivities = function(){
        reAssignActivityData();
        opsExecutionPlanService.saveReAssignedActivities($scope.reAssignActivityList)
        .success(function(response, status){
          $scope.campaignDataList = [];
          getOpsExecutionImageDetails();
          $('#reAssignModal').modal('hide');
          swal(errorHandler.name,errorHandler.reAssign_success,errorHandler.success);

        })
        .error(function(response, status){
          $('#reAssignModal').modal('hide');
          swal(errorHandler.name,errorHandler.reAssign_error,errorHandler.error);
          console.log(response);
        });
      }
}]);
