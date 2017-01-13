angular.module('catalogueApp')
.controller('ReleaseCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location','releaseCampaignService',
    function ($scope, $rootScope, $window, $location, releaseCampaignService) {
 	
 	$scope.headings = [
        {header : 'Supplier Name'},
        {header : 'Area'},
        {header : 'Sub Area'},
        {header : 'Inventory Type'},
        {header : 'Release Date'},
        {header : 'Audit Date'},
        {header : 'Closure Date'},
        {header : 'Comments'},
        {header : 'Phase'}
      ]; 

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
      $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
      };

      $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
      $scope.format = $scope.formats[1];
      $scope.altInputFormats = ['M!/d!/yyyy'];

    $scope.saveDetails = function(){
      alert("vidhi");
    };

    releaseCampaignService.getCampaignReleaseDetails()
    	.success(function(response, status){
    		$scope.releaseDetails = response.data;
            $scope.loading = response;
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
 
}]);//Controller function ends here
