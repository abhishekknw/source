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
          
     
    	$scope.save = function() {
    		console.log($scope.model);
          $location.path("/manageCampaign/create");  
        }

  $scope.statuses = ['Shortlisted', 'Requested', 'Finalized'];

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

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[0];
  $scope.altInputFormats = ['M!/d!/yyyy'];

      //[TODO] implement this
    }]);
