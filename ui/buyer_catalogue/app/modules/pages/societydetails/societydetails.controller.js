angular.module('machadaloPages')
.controller('SocietyCtrl',
    ['$scope', '$rootScope', '$window', '$location','societyDetailsService',
    function ($scope, $rootScope, $window, $location, societyDetailsService) {
     societyDetailsService.processParam();
     $scope.society = {};
     societyDetailsService.getSociety('MUMPOHNRSOC2')
      .success(function (response) {
        $scope.society = response;
       console.log(response);
     });

     //Start:For adding shortlisted society
     //if($rootScope.campaignId){
       $scope.shortlistThis = function() {
         alert('bhvidhi');
       societyListService.addShortlistedSociety($rootScope.campaignId, 'MUMPOHNRSOC2')
        .success(function (response){
            $scope.model = response;
              console.log(response);
       });
     }//}//End: For adding shortlisted society

   }]);//Controller function ends here
