angular.module('machadaloPages')
.controller('SocietyListCtrl',
    ['$scope', '$rootScope', '$window', '$location',
    function ($scope, $rootScope, $window, $location, $http, societyListService) {
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
       "societyname":"23C_Tower1_1401",
       "location":"next to baskin"
   },
   {
       "societyname":"23C_Tower1_1402",
       "location":"next to theo"
   }
  ];
  $scope.model = dummyData;

    }]);
