angular.module('catalogueApp')
.controller('AuditReleasePlanCtrl',
    ['$scope', '$rootScope', '$window', '$location','auditReleasePlanService','$stateParams',
    function ($scope, $rootScope, $window, $location, auditReleasePlanService, $stateParams) {
      $scope.campaign_id = $stateParams.proposal_id;
      $scope.headings = [
        {header : 'Phase'},
        {header : 'Inventory Type'},
        {header : 'Supplier Id'},
        {header : 'Supplier Type'},
        {header : 'Release Date'},
        {header : 'Audit Date'},
        {header : 'Closure Date'},
        {header : 'Comments'},
      ];
      $scope.audit_dates = [
        {header : 'Audit Date'},
      ];
      $scope.auditDates = [];
      auditReleasePlanService.getCampaignReleaseDetails($scope.campaign_id)
      	.success(function(response, status){
          console.log(response);
      		$scope.releaseDetails = response.data;
              $scope.loading = response;
      	})
      	.error(function(response, status){
      		console.log("error occured", status);
      	});
      $scope.emptyList = ['empty'];
      $scope.getFilters = function(supplier){
        // console.log(supplier);
        if(supplier.shortlisted_inventories.length > 0){
          return supplier.shortlisted_inventories;
        }
        else
          return $scope.emptyList;
      }
      //For audit dates modal
      $scope.addDate = function(date){
        var auditDate = {
          // audit_date = ''
        };
        $scope.auditDates.push({
          auditDate:date,
        });
      }
      $scope.auditDate = []
      $scope.setAuditDate = function(filter){
        $scope.auditDates = [];
        if(filter.audit_dates.length > 0){
          for(var i=0;i<filter.audit_dates.length; i++)
              $scope.addDate(filter.audit_dates[i]);
        }else{
          $scope.addDate();
        }
      }
      $scope.deleteDate = function(index){
    		$scope.auditDates.splice(index,1);
    	}
  }]);
