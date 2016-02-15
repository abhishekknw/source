angular.module('machadaloPages')
.controller('SocietyListCtrl',
    ['$scope', '$rootScope', '$window', '$location', '$http','societyListService',
    function ($scope, $rootScope, $window, $location, $http, societyListService) {
      societyListService.processParam();
      //Start: for filter functionality
      $scope.getLocation = function(val) {
         return $http.get('https://maps.googleapis.com/maps/api/geocode/json', {
           params: {
             address: val,
             key: 'AIzaSyDCTq6FNBxVrhd2te_GIrCa8TI8CYwobYg',
             sensor: true
           }
         }).then(function(response){
           return response.data.results.map(function(item){
             return item.formatted_address;
           });
         });
       };// End: filter functionality
  $scope.model = {};
  var dummyData = [
   {
       "society_name":"abc",
       "society_address1":"next to baskin"
   },
   {
       "society_name":"bcd",
       "society_address1":"next to theo"
   }
  ];
   $scope.model = dummyData;
  //  societyListService.getSocietyInfo('10')
  //   .success(function (response){
  //     $scope.model = [response];
  //       console.log(response);
  //    });

   //var sObj = '';
   //societyListService.listSocieties(sObj)
    //.success(function (response) {
    // $scope.model = response.results;
    // console.log(response);
 //})

   //Start:For adding shortlisted society
   if($rootScope.campaignId){
     $scope.shortlistThis = function() {
     societyListService.addShortlistedSociety($rootScope.campaignId, '10')
      .success(function (response){
          $scope.model = response;
            console.log(response);
     });
   }}//End: For adding shortlisted society

   //Start: To navigate to catalogue page
   $scope.catalogue = function(){
     $location.path('/society/details');
   }//End: To navigate to catalogue page

   $scope.filter = function() {
     alert('njnjnj');
  }
  //Start: Sort Functionality
  $scope.predicate = 'society_name';
  $scope.reverse = true;
  $scope.order = function(predicate) {
    $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
    $scope.predicate = predicate;
  }
  //End: Sort Functionality


}])// SocietyListCtrl Controller Functions end
 .controller('SocietyFilterCtrl',
     ['$scope', '$rootScope', '$window', '$location', '$http','societyListService',
     function ($scope, $rootScope, $window, $location, $http, societyListService) {
 // $scope.filter = function() {
 //   alert('bhbh');
 // }
 }]);
