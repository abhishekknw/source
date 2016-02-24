angular.module('machadaloPages')
.controller('RequestedCampaignCtrl',
  ['$scope', '$rootScope', '$window', '$location', 'pagesService',
  function ($scope, $rootScope, $window, $location, pagesService) {

	pagesService.getCampaigns('Requested')
	.success(function (response, status) {
	  console.log(response);
      $scope.model = response;
        
     });

	$scope.societyList = function(campaign_id) {
	  $location.path("manageCampaign/requested/" + campaign_id + "/societies");  
	};

}])
.controller('RequestedSocietiesCtrl',
['$scope', '$rootScope', '$window', '$location', 'pagesService',
function ($scope, $rootScope, $window, $location, pagesService) {

  pagesService.processParam();
  $scope.model = {};

  pagesService.getSocietyInventory($rootScope.campaignId)
  .success(function (response, status) {
    console.log(response);
    $scope.model = response.inventories;
    $scope.campaign = response.campaign;

    
  })

   $scope.catalogue = function(campaign_id, society_id){
     $location.path('campaign/' + campaign_id + '/societyDetails/' + society_id);
   }//End: To navigate to catalogue page

   $scope.removeThis = function(society_id){
     pagesService.removeThisSociety(society_id, 'Permanent')
     .success(function (response, status) {
        if (status == '200') {
          $window.location.reload(); 
        }
     })
   }

   $scope.addSocieties = function(campaign_id){
     $location.path("/campaign/" + campaign_id + "/societyList");
   }

   $scope.book = function(campaign_id){
     pagesService.book(campaign_id, 'Finalized')
     .success(function (response, status) {
        if (status == '200') {
          $location.path("/manageCampaign/finalized/" + campaign_id + "/societies");
        }
     })
     
   }//

  }])




