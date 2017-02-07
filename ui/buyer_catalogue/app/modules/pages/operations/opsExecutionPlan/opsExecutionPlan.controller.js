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
        {header : 'Comments'},
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

      opsExecutionPlanService.getOpsExecutionImageDetails($scope.campaign_id)
      	.success(function(response, status){
          console.log(response);
      		$scope.campaignData = response.data;
              $scope.loading = response;
      	})
      	.error(function(response, status){
      		console.log("error occured", status);
      	});
      $scope.setImageUrl = function(image_path){
        console.log(image_path);
        $scope.image_url = "http://androidtokyo.s3.amazonaws.com/" + image_path;
      }
      $scope.getSupplierDetails = function(supplier){
        $scope.supplierData = [];
        var supplierId = supplier.inventory_details.shortlisted_supplier.object_id;
        var contentType = supplier.inventory_details.shortlisted_supplier.content_type;
        opsExecutionPlanService.getSuppierDetails(supplierId,contentType)
        	.success(function(response, status){
            $scope.supplierData = response.data;
      	   })
        	.error(function(response, status){
        		console.log("error occured", status);
        	});

      }


}]);
