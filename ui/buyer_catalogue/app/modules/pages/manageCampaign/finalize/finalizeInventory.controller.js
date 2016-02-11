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
            
       
    	$scope.create = function() {
    		console.log($scope.campaign_type);
            $location.path("/manageCampaign/create");  
        }

  $scope.statuses = ['Shortlisted', 'Requested', 'Finalized'];

  $scope.clear = function() {
    $scope.dt = null;
  };

  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
  };

  $scope.toggleMin = function() {
    $scope.minDate = $scope.minDate ? null : new Date();
  };

  $scope.toggleMin();
  $scope.maxDate = new Date(2020, 5, 22);

  $scope.open1 = function() {
    $scope.popup1.opened = true;
  };

  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };

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

  $scope.popup1 = {
    opened: false
  };

  $scope.popup2 = {
    opened: false
  };

      //[TODO] implement this
    }]);
