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
        {header : 'Release Date'},
        {header : 'Audit Date'},
        {header : 'Closure Date'},
        {header : 'Assign'},
        {header : 'Comments'},
      ];
      $scope.audit_dates = [
        {header : 'Audit Date'},
      ];
      $scope.assignModal_headers = [
        {header : 'AdInventory Id'},
        {header : 'Activity'},
        {header : 'Activity Date'},
        {header : 'Action'},
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

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];


      $scope.auditDates = [];
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
      auditReleasePlanService.saveUser($scope.inventoryList)
      .success(function(response, status){
      })
      .error(function(response, status){
        console.log("error occured", status);
      });
    }
  }]);
