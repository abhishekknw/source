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

    $scope.saveDetails = function(){
      alert("vidhi");
    };

    releaseCampaignService.getReleaseDetails()
    	.success(function(response, status){
    		$scope.releases = response.data;
        $scope.loading = response;
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
 
}]);//Controller function ends here
