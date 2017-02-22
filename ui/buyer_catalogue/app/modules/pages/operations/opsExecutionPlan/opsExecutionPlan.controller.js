angular.module('catalogueApp')
.controller('OpsExecutionPlanCtrl',
    ['$scope', '$rootScope', '$window', '$location','opsExecutionPlanService','$stateParams',
    function ($scope, $rootScope, $window, $location, opsExecutionPlanService, $stateParams) {
      $scope.campaign_id = $stateParams.proposal_id;
      $scope.headings = [
        {header : 'Supplier Id'},
        {header : 'Inventory Id'},
        {header : 'Inventory Type'},
        {header : 'Image'},
         {header : 'Activity Name'},
        {header : 'Activity Date'},
        {header : 'ReAssign'},
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

      opsExecutionPlanService.getOpsExecutionImageDetails($scope.campaign_id)
      	.success(function(response, status){
      		$scope.campaignData = response.data;
          console.log('vidhi', $scope.campaignData);
          if($scope.campaignData.length == 0)
            $scope.hideData = false;//change to true doing for testing
              $scope.loading = response;
      	})
      	.error(function(response, status){
          $scope.hideData = true;
      		console.log("error occured", status);
      	});
      $scope.setImageUrl = function(c1){
        $scope.imageUrlList = [];
        for(var i=0; i<c1.length; i++){
          var imageData = {
            image_url : 'http://androidtokyo.s3.amazonaws.com/' + c1[i].inventory_activity_assignment[i].images[i].image_path,
            comment : c1[i].inventory_activity_assignment[i].images[i].comment,
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
          console.log(response);
          $("#summaryModal").modal('show');
          $scope.summaryData = response.data;
        })
        .error(function(response, status){
          console.log(response);
        });
      }
}]);
