angular.module('machadaloPages')
.controller('SocietyListCtrl',
    ['$scope', '$rootScope', '$window', '$location', '$http','societyListService', 'pagesService',
    function ($scope, $rootScope, $window, $location, $http, societyListService, pagesService) {
      societyListService.processParam();
      $scope.example14model = [];
$scope.example14data = [
    {id: 1, label: "Powai"},
    {id: 2, label: "Andheri(East)"},
    {id: 3, label: "Andheri(West)"},
    {id: 4, label: "Bhandup(East)"},
    {id: 5, label: "Bhandup(West)"},
    {id: 6, label: "Kandivali(East)"},
    {id: 7, label: "Kandivali(West)"}
];

$scope.example14settings = {
    scrollableHeight: '100px',
    scrollable: true,
    dynamicTitle: false
};
$scope.example5customTexts = {
  buttonDefaultText: 'Select Location',
  checkAll: 'Select All',
  uncheckAll: 'Select None'
};
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
   //$scope.model = dummyData;

    var sObj = '';
      societyListService.listSocieties(sObj)
        .success(function (response) {
           $scope.model = response.results;
           console.log(response);
    })

   //Start:For adding shortlisted society
   if($rootScope.campaignId){
     $scope.shortlistThis = function(id) {
       alert(id);
     societyListService.addShortlistedSociety($rootScope.campaignId, id)
      .success(function (response){
          console.log(response);
     });
   }}//End: For adding shortlisted society

   //Start: To navigate to catalogue page
   if($rootScope.campaignId){
   $scope.catalogue = function(id){
     alert(id);
     $location.path('campaign/' + $rootScope.campaignId +'/societyDetails/' + id);
   }}//End: To navigate to catalogue page

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

  /*//pagination starts here
  $scope.totalItems = 64;
  $scope.currentPage = 4;

  $scope.setPage = function (pageNo) {
    $scope.currentPage = pageNo;
  };

  $scope.pageChanged = function() {
   alert('gvg');
  };
  $scope.maxSize = 5;
  $scope.bigTotalItems = 175;
  $scope.bigCurrentPage = 1;
    //pagination ends here
*/
}]);// SocietyListCtrl Controller Functions end
// .controller('SocietyFilterCtrl',
//     ['$scope', '$rootScope', '$window', '$location', '$http','societyListService',
//     function ($scope, $rootScope, $window, $location, $http, societyListService) {
      //$scope.filter = function() {
 //   alert('bhbh');
 // }
 //}]);
