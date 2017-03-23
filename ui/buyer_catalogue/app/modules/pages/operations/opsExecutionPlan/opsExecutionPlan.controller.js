angular.module('catalogueApp')
.controller('OpsExecutionPlanCtrl',
    ['$scope', '$rootScope', '$window', '$location','opsExecutionPlanService','$stateParams','commonDataShare','constants','$timeout',
    function ($scope, $rootScope, $window, $location, opsExecutionPlanService, $stateParams,commonDataShare,constants,$timeout) {
      $scope.campaign_id = $stateParams.proposal_id;
      var sleepTime = 0;
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
        	.then(function onSuccess(response){
        		$scope.campaignData = response.data.data;
            createList();
            console.log('vidhi', $scope.campaignData);
            if($scope.campaignData.length == 0)
              $scope.hideData = false;//change to true doing for testing
                $scope.loading = response.data;
        	})
        	.catch(function onError(response){
            $scope.hideData = true;
        		console.log("error occured", response);
        	});
        }
        var getUsersList = function(){
          commonDataShare.getUsersList()
            .then(function onSuccess(response){
              console.log(response);
              $scope.userList = response.data.data;
            })
            .catch(function onError(response){
              console.log("error occured", response);
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
        .then(function onSuccess(response){
          $("#summaryModal").modal('show');
          $scope.summaryData = response.data.data;
        })
        .catch(function onError(response){
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
        .then(function onSuccess(response){
          $scope.campaignDataList = [];
          getOpsExecutionImageDetails();
          $('#reAssignModal').modal('hide');
          swal(constants.name,constants.reAssign_success,constants.success);

        })
        .catch(function onError(response){
          $('#reAssignModal').modal('hide');
          swal(constants.name,constants.reAssign_error,constants.error);
          console.log(response);
        });
      }
    $scope.downloadImages = function(){
      $scope.buttonDisable = true;
      opsExecutionPlanService.downloadImages($stateParams.proposal_id)
      .then(function onSuccess(response){
        console.log(response);
        $scope.taskId = response.data.data;
        downloadInProgress();
      }).catch(function onError(response){
        console.log("Error occured", response.status);
      })
    }
    function downloadInProgress(){
      opsExecutionPlanService.downloadInProgress($scope.taskId)
      .then(function onSuccess(response){
        console.log(response);
        // $scope.progress = response.progress+"%";
        sleepTime = 2 * sleepTime + 5000;
        if(response.data.data.ready != true){
           $timeout(downloadInProgress,10000); // This will perform async
        }
        else if(response.data.data.status == true){
          opsExecutionPlanService.finishDownload($scope.taskId,$stateParams.proposal_id)
          .then(function onSuccess(response){
            console.log(response);
             $window.open(response.data.data, '_blank');
             $scope.buttonDisable = false;
          }).catch(function onError(response){
            console.log(response);
          });
        }
        else {
          swal(constants.name,constants.images_download_error,constants.error);
        }
      }).catch(function onError(response){
        console.log(response);
      });
    }
}]);
