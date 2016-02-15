angular.module('machadaloPages')
.controller('FinalizeInventoryCtrl',
    ['$scope', '$rootScope', '$window', '$location', 'pagesService',
    function ($scope, $rootScope, $window, $location, pagesService) {
      pagesService.processParam();

      $scope.model = {};

      if($rootScope.campaignId){
         pagesService.getRequestedInventory($rootScope.campaignId)
          .success(function (response, status) {
              console.log(response);
              $scope.model = response;

          });
      }
          
     
    	$scope.save = function(type) {
          alert(type);
        $scope.data = $scope.model;
        console.log("data");
        for(var i=0; i<$scope.data.length; i++){
          $scope.data[i].campaign = undefined;
          $scope.data[i].society = undefined;
          /*for(var j=0; j<$scope.data[i].inventories.length; j++){
            if ($scope.data[i].inventories[j].start_date && $scope.data[i].inventories[j].end_date){
              $scope.data[i].inventories[j].start_date = $scope.data[i].inventories[j].start_date.toString().substring(0, 10);  
              $scope.data[i].inventories[j].end_date = $scope.data[i].inventories[j].end_date.toString().substring(0, 10); 
            } 
          }*/
        }
        $scope.post_data = {"inventory":$scope.data, "type":type}
        console.log($scope.post_data);
        pagesService.saveFinalizedInventory($scope.post_data)
            .success(function (response, status) {
            if (status == '200') {
              $location.path("/manageCampaign/finalize");  
            }
        }).error(function(response, status){
           if(status<'200'){
                $rootScope.errorMsg = "Connection error, please try again later.";
                return;
        }
        });
      };

      $scope.removeSociety = function(id) {
        var result = confirm("Want to delete?");
        if (result){
        
          pagesService.removeFinalizedInventory(id)
              .success(function (response, status) {
              if (status == '200') {
                $window.location.reload(); 
              }
          }).error(function(response, status){
             if(status<'200'){
                  $rootScope.errorMsg = "Connection error, please try again later.";
                  return;
          }
          });
        }
      };





  $scope.statuses = ['Requested', 'Finalized'];

  $scope.clear = function() {
    $scope.dt = null;
  };

  $scope.maxDate = new Date(2020, 5, 22);
  $scope.today = new Date();

 
  $scope.setDate = function(year, month, day) {
    $scope.dt = new Date(year, month, day);
  };

  $scope.dateOptions = {
    formatYear: 'yy',
    startingDay: 1
  };

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy-MM-dd', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[1];
  $scope.altInputFormats = ['M!/d!/yyyy'];

      //[TODO] implement this
    }]);
