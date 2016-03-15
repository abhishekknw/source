angular.module('machadaloPages')
.controller('SocietyListCtrl',
    ['$scope', '$rootScope', '$window', '$location', '$http','societyListService', 'pagesService',
    function ($scope, $rootScope, $window, $location, $http, societyListService, pagesService) {
      societyListService.processParam();
      $scope.locationValueModel = [];
      /*$scope.locationValue = [
      {id: 1, label: "Powai"},
      {id: 2, label: "Andheri(East)"},
      {id: 3, label: "Andheri(West)"},
      {id: 4, label: "Bhandup(East)"},
      {id: 5, label: "Bhandup(West)"},
      {id: 6, label: "Kandivali(East)"},
      {id: 7, label: "Kandivali(West)"}
    ];*/
$scope.locationValueSettings = {
    scrollableHeight: '100px',
    scrollable: true,
    dynamicTitle: false
};
$scope.locationcustomTexts = {
  buttonDefaultText: 'Select Location',
  checkAll: 'Select All',
  uncheckAll: 'Select None'
};
//Start: For displaying filter values
$scope.locationValue = [];
societyListService.listFilterValues()
 .success(function (response){
   $scope.locationValue = response;
   console.log(response);
 })
//End: For displaying filter values

  $scope.model = {};
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
