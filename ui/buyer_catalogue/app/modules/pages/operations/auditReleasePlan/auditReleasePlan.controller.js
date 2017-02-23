angular.module('catalogueApp')
.controller('AuditReleasePlanCtrl',
    ['$scope', '$rootScope', '$window', '$location','auditReleasePlanService','$stateParams', 'commonDataShare',
    function ($scope, $rootScope, $window, $location, auditReleasePlanService, $stateParams, commonDataShare) {
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
      function getCampaignReleaseDetails(){
      auditReleasePlanService.getCampaignReleaseDetails($scope.campaign_id)
      	.success(function(response, status){
          console.log(response);
      		$scope.releaseDetails = response.data;
          setDataToModel($scope.releaseDetails.shortlisted_suppliers);
              $scope.loading = response;
      	})
      	.error(function(response, status){
      		console.log("error occured", status);
      	});
      }
      getCampaignReleaseDetails();
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
        .success(function(response, status){
      	})
      	.error(function(response, status){
      		console.log("error occured", status);
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
    $scope.userList = [
      {name : 'Ankit'},
      {name : 'Komal'},
    ];
    $scope.saveUserForActivity = function(){
      console.log($scope.inventoryList);
      auditReleasePlanService.saveUser($scope.inventoryList)
      .success(function(response, status){
        getCampaignReleaseDetails();
      })
      .error(function(response, status){
        console.log("error occured", status);
      });
    }

    $scope.invActivityData = [
        {activity_type : "RELEASE", act_date:{date:'',userCode:''}},
        {activity_type : "CLOSURE", act_date:{date:'',userCode:''}},
      ];
    $scope.invActivityAuditData = {
      activity_type : 'AUDIT', audit_dates:[{date:'',userCode:''}],
    };
    $scope.key;
    $scope.invIdList = [];
    $scope.addInventory = function(inventory,index){

      if(inventory.status == true)
        $scope.invIdList.push(inventory.id);
      else
        $scope.invIdList.splice(index,1);
    }
    $scope.setDate = function(date){
      date = formatDate(date);
      console.log(date);
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
      editActivityDates();
      console.log($scope.requestaActivityData);
      auditReleasePlanService.saveActivityDetails($scope.requestaActivityData)
      .success(function(response, status){
      })
      .error(function(response, status){
        console.log("error occured", status);
      });
    }
     $scope.getActivityDates = function(inventoryList){
       for(var i=0;i<inventoryList.length; i++){
         inventoryList[i].status = false;
       }
       console.log(inventoryList);
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
          var date = formatDate($scope.invActivityData[i].act_date.date);
          // var userCode = $scope.invActivityData[i].act_date.userCode;
          var userCode = 6;
          releaseClosureData.date_user_assignments[date] = userCode;
          data.push(releaseClosureData);
        }
      }

      auditData.activity_type = $scope.invActivityAuditData.activity_type;
      console.log($scope.invActivityAuditData.audit_dates[0].date);
      for(var i=0; i<$scope.invActivityAuditData.audit_dates.length; i++){
        if($scope.invActivityAuditData.audit_dates[i].date){
          // auditData.date_user_assignments[i] = {};
          var date = formatDate($scope.invActivityAuditData.audit_dates[i].date);
          // var userCode = $scope.invActivityAuditData.audit_dates[i].userCode;
          var userCode = 6;
          auditData.date_user_assignments[date] = userCode;
        }
      }
      console.log(auditData);
      data.push(auditData);
      $scope.requestaActivityData = {
        shortlisted_inventory_id_detail : $scope.invIdList,
        assignment_detail : data,
      };
      console.log(data);
      // console.log($scope.invActivityData);
    }
    function makeAssignActivityData(inventory, inventoryData){
      data.assignment_detail.push()
    }
    function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();
    console.log(month,day,year);
    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
  }
  $scope.showActivityDates = function(inventory){
    console.log(inventory);
    $scope.ActivityDatesData = inventory;
  }

  }]);
