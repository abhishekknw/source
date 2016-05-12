angular.module('machadaloPages')
.controller('SocietyCtrl',
    ['$scope', '$rootScope', '$window', '$location','societyDetailsService',
    function ($scope, $rootScope, $window, $location, societyDetailsService) {
     societyDetailsService.processParam();
     $scope.society = {};
     societyDetailsService.getSociety($rootScope.societyId)
      .success(function (response) {
        $scope.society = response;
        $rootScope.societyname = response.society_name;
        console.log(response);
     });

     $scope.societyList = function() {
       $location.path("manageCampaign/shortlisted/" + $rootScope.campaignId + "/societies");
     };

     //Start:For adding shortlisted society
     if($rootScope.campaignId){
       $scope.shortlistThis = function(id) {
       societyDetailsService.addShortlistedSociety($rootScope.campaignId, id)
        .success(function (response){
            $scope.model = response;
              console.log(response);
              $location.path("manageCampaign/shortlisted/" + $rootScope.campaignId + "/societies");
       });
     }}//End: For adding shortlisted society
   }]);//Controller function ends here
