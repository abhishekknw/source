angular.module('machadaloPages')
.controller('ShortlistedCampaignCtrl',
  ['$scope', '$rootScope', '$window', '$location', 'pagesService',
  function ($scope, $rootScope, $window, $location, pagesService) {

    $scope.businesses = [];

	pagesService.getCampaigns('Shortlisted')
	.success(function (response, status) {
	  console.log(response);
      $scope.model = response;
        
     });

	$scope.societyList = function(campaign_id) {
	  $location.path("manageCampaign/shortlisted/" + campaign_id + "/societies");  
	};

}])

.controller('ShortlistedSocietiesCtrl',
['$scope', '$rootScope', '$window', '$location', 'pagesService',
function ($scope, $rootScope, $window, $location, pagesService) {

  pagesService.processParam();
  $scope.model = {};

  pagesService.getSocietyInventory($rootScope.campaignId)
  .success(function (response, status) {
    console.log(response);
    $scope.model = response;
    
  })

   $scope.catalogue = function(society_id){
     $location.path('/society/details');
   }//End: To navigate to catalogue page

   $scope.removeThis = function(society_id){
     pagesService.removeThisSociety(society_id, 'Permanent')
     .success(function (response, status) {
        if (status == '200') {
          $window.location.reload(); 
        }
     })
   }


}]);
