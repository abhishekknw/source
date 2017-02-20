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
          if($scope.campaignData.length == 0)
            $scope.hideData = false;//change to true doing for testing
              $scope.loading = response;
      	})
      	.error(function(response, status){
          $scope.hideData = true;
      		console.log("error occured", status);
      	});
      $scope.setImageUrl = function(supplier){
        $scope.imageUrlList = [];
        for(var i=0; i<supplier.images.length; i++){
          var imageData = {
            image_url : 'http://androidtokyo.s3.amazonaws.com/' + supplier.images[i].image_path,
            comment : supplier.images[i].comment,
          };
          $scope.imageUrlList.push(imageData);
        }
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
      $scope.getSummary = function(){
        opsExecutionPlanService.getSummaryDetails($scope.campaign_id)
        .success(function(response, status){
          console.log(response);
          $scope.summaryData = response.data;
        })
        .error(function(response, status){
          console.log(response);
        });
      }
}]);
