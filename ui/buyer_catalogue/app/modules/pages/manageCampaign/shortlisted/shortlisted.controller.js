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

}]);
