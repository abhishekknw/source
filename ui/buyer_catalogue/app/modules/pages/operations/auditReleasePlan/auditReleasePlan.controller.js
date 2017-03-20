angular.module('catalogueApp')
.controller('AuditReleasePlanCtrl',
    ['$scope', '$rootScope', '$window', '$location','auditReleasePlanService','$stateParams', 'commonDataShare','constants',
    function ($scope, $rootScope, $window, $location, auditReleasePlanService, $stateParams, commonDataShare, constants) {
      $scope.campaign_id = $stateParams.proposal_id;
      $scope.headings = [
        {header : 'Phase'},
        {header : 'Inventory Type'},
        {header : 'Supplier Id'},
        {header : 'Supplier Type'},
        {header : 'AdInventory Id'},
        {header : 'Activity Date'},
        // {header : 'Release Date'},
        // {header : 'Audit Date'},
        // {header : 'Closure Date'},
        // {header : 'Assign'},
        {header : 'Comments'},
      ];
      $scope.audit_dates = [
        {header : 'Audit Date'},
      ];
      $scope.assignModal_headers = [
        {header : 'AdInventory Id'},
        {header : 'Activity Name'},
        {header : 'Activity Date'},
        {header : 'Assigned User'},
      ];
      $scope.activity_names = [
        {header : 'Release' , code : 'RE'},
        {header : 'Closure',   code : 'CL'},
        {header : 'Audit',     code : 'AU'},
      ];
      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;
      $scope.popup3 = false;
      $scope.error = false;

      $scope.setDate = function(year, month, day) {
        $scope.dt = new Date(year, month, day);
      };
      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      // $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.formats = ['yyyy-MM-dd'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];


      $scope.auditDates = [];
      function init(){
        getCampaignReleaseDetails();
        getUsersList();
      }
      //get user list
      var getUsersList = function(){
        commonDataShare.getUsersList()
          .then(function onSuccess(response){
            console.log(response);
            $scope.userList = response.data.data;
          })
          .catch(function onError(response){
            console.log("error occured", response.status);
          });
      }
      init();

      //initial call to get release Data
      function getCampaignReleaseDetails(){
      auditReleasePlanService.getCampaignReleaseDetails($scope.campaign_id)
      	.then(function onSuccess(response){
          console.log(response);
      		$scope.releaseDetails = response.data.data;
          setDataToModel($scope.releaseDetails.shortlisted_suppliers);
              $scope.loading = response.data;
      	})
      	.then(function onError(response){
      		console.log("error occured", response.status);
      	});
      }
      // getCampaignReleaseDetails();
        var setDataToModel = function(suppliers){
          for(var i=0;i<suppliers.length;i++){
            angular.forEach(suppliers[i].shortlisted_inventories, function(filter){
              filter.detail.closure_date = new Date(filter.detail[0].closure_date);
              filter.detail.release_date = new Date(filter.detail[0].release_date);
              filter.detail.comments = filter.detail[0].comment;
            });
          }
        }
      $scope.emptyList = {NA:'NA'};
      $scope.getFilters = function(supplier){
        var keys = Object.keys(supplier.shortlisted_inventories);
        if(keys.length > 0){
          $scope.inventory_type = supplier.shortlisted_inventories
          return supplier.shortlisted_inventories;
        }
        else{
          return $scope.emptyList;
        }
      }
      //For audit dates modal
      $scope.addDate = function(date){
        $scope.auditDates.push({
          audit_date:'',
        });
      }
      $scope.auditDate = []
      $scope.setAuditDate = function(filter,index,key){
        $scope.inventory_key = key;
        $scope.supplier_index = index;
        $scope.auditDates = [];
        $scope.auditDates = filter.detail[0].audit_dates;
        if($scope.auditDates.length == 0){
          $scope.addDate();
        }else{
          for(var i=0;i<$scope.auditDates.length;i++){
            $scope.auditDates[i]['audit_date'] = new Date($scope.auditDates[i]['audit_date']);
          }
        }
      }
      $scope.deleteDate = function(index){
    		$scope.auditDates.splice(index,1);
    	}
      $scope.saveAuditDates = function(){
        for(var i=0;i<$scope.auditDates.length;i++){
            $scope.releaseDetails.shortlisted_suppliers[$scope.supplier_index].shortlisted_inventories[$scope.inventory_key].detail[0].audit_dates[i]['audit_date'] = $scope.auditDates[i].audit_date;
        }
      }
      $scope.addClosureDate = function(date_array,date){
        for(var i=0;i<date_array.length;i++){
          date_array[i].closure_date = date;
        }
      }
      $scope.addReleaseDate = function(date_array,date){
        for(var i=0;i<date_array.length;i++){
          date_array[i].release_date = date;
        }
      }
      $scope.addComments = function(comments_array,comment){
        for(var i=0;i<comments_array.length;i++){
          comments_array[i].comment = comment;
        }
      }

      $scope.updateData = function(){
        auditReleasePlanService.updateAuditReleasePlanDetails($scope.campaign_id,$scope.releaseDetails.shortlisted_suppliers)
        .then(function onSuccess(response){
          getCampaignReleaseDetails();
          $scope.resetData();
          swal(constants.name,constants.updateData_success,constants.success);
      	})
      	.catch(function onError(response){
          swal(constants.name,constants.updateData_error,constants.error);
      		console.log("error occured", response.status);
      	});
      }

      $scope.assignUserToActivity = function(inv){
        try{
          console.log(inv);
          $scope.inventoryList = [];
          for(var i=0; i<inv.length; i++){
            createInventoryList(inv[i].inventory_id,'RELEASE',inv[i].release_date,inv[i].id);
            createInventoryList(inv[i].inventory_id,'CLOSURE',inv[i].closure_date,inv[i].id);
            for(var j=0; j<inv[i].audit_dates.length; j++){
              createInventoryList(inv[i].inventory_id,'AUDIT',inv[i].audit_dates[j].audit_date,inv[i].id);
            }
          }
        }catch(error){
          commonDataShare.showMessage(error.message);
        }
      }
      var createInventoryList = function(id,name,date,invId){
        try{
          var data = {
            id : id,
            activity_type : name,
            activity_date : date,
            shortlisted_inventory_id : invId,
            assigned_to : 6,
          };
          $scope.inventoryList.push(data);
      }catch(error){
        commonDataShare.showMessage(error.message);
      }
    }
    $scope.saveUserForActivity = function(){
      console.log($scope.inventoryList);
      auditReleasePlanService.saveUser($scope.inventoryList)
      .then(function onSuccess(response){
        getCampaignReleaseDetails();
      })
      .catch(function onError(response){
        console.log("error occured", response.status);
      });
    }

    $scope.invActivityData_struct = [
        {activity_type : "RELEASE", act_date:{date:'',userCode:''}},
        {activity_type : "CLOSURE", act_date:{date:'',userCode:''}},
      ];
    $scope.invActivityAuditData = {
      activity_type : 'AUDIT', audit_dates:[{date:'',userCode:''}],
    };
    $scope.key;
    $scope.invIdList = [];
    //adding adIds to list to send in request
    $scope.addInventory = function(inventory,rowIndex,index){
      if(inventory.status == true){
        $scope.invIdList.push(inventory.id);
        $scope.selectedRow = rowIndex;
      }
      else
        $scope.invIdList.splice(index,1);
    }
    //To disable other checkboxes of other rows of adInventory Id
    $scope.isDisable = function(index){
      if($scope.invIdList.length == 0)
        $scope.selectedRow = undefined;
      if($scope.selectedRow == undefined || $scope.selectedRow == index)
        return false;
      else
        return true;
    }
    $scope.setDate = function(date){
      date = commonDataShare.formatDate(date);
    }
    $scope.addAuditDate = function(inventory){
      console.log(inventory);
      inventory.push({
        date : '',
        userCode : '',
      });
      console.log(inventory);
    }
    $scope.removeAuditDate = function(inventory,index){
      inventory.splice(index,1);
    }
    $scope.saveActivityDates = function(){
      //below function creates complex request structure for data
      editActivityDates();
      auditReleasePlanService.saveActivityDetails($scope.requestaActivityData)
      .then(function onSuccess(response){
        getCampaignReleaseDetails();
        $scope.resetData();
        $('#manageDatesModal').modal('hide');
        swal(constants.name,constants.inventory_date_success,constants.success);
      })
      .catch(function onError(response){
        $('#manageDatesModal').modal('hide');
        swal(constants.name,constants.inventory_date_error,constants.error);
        console.log("error occured", response.status);
      });
    }
     $scope.getActivityDates = function(supplier){
       $scope.invActivityData = angular.copy($scope.invActivityData_struct);
       angular.forEach(supplier.shortlisted_inventories, function(inventoryList,inventory){
          for(var i=0; i<inventoryList.detail.length; i++){
            inventoryList.detail[i].status = false;
          }
       });
      //  console.log(inventoryList);
     }
    var editActivityDates = function(){
      // console.log($scope.invActivityData);
      var data = [];
      var auditData = {
        activity_type : '',
        date_user_assignments : {},
      };
      var releaseClosureDataStruct = {
        activity_type : '',
        date_user_assignments : {},
      };

      for(var i=0; i<$scope.invActivityData.length; i++){
        if($scope.invActivityData[i].act_date.date){
          var releaseClosureData = angular.copy(releaseClosureDataStruct);
          releaseClosureData.activity_type = $scope.invActivityData[i].activity_type;
          var date = commonDataShare.formatDate($scope.invActivityData[i].act_date.date);
          var userCode = $scope.invActivityData[i].act_date.userCode;
          // var userCode = 6;
          releaseClosureData.date_user_assignments[date] = userCode;
          data.push(releaseClosureData);
        }
      }

      auditData.activity_type = $scope.invActivityAuditData.activity_type;
      for(var i=0; i<$scope.invActivityAuditData.audit_dates.length; i++){
        if($scope.invActivityAuditData.audit_dates[i].date){
          // auditData.date_user_assignments[i] = {};
          var date = commonDataShare.formatDate($scope.invActivityAuditData.audit_dates[i].date);
          var userCode = $scope.invActivityAuditData.audit_dates[i].userCode;
          // var userCode = 6;
          auditData.date_user_assignments[date] = userCode;
        }
      }
      data.push(auditData);
      $scope.requestaActivityData = {
        shortlisted_inventory_id_detail : $scope.invIdList,
        assignment_detail : data,
      };
    }

    $scope.showActivityDates = function(inventory){
      $scope.ActivityDatesData = inventory;
    }
    //event on modal close i.e - clear invIdList
    $scope.resetData = function(){
      $scope.invIdList = [];
      $scope.selectedRow = undefined;
      $scope.invActivityData = [];
      $('#manageDatesModal').on('hide.bs.modal', function () {
      })
    }
}]);
