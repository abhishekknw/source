angular.module('catalogueApp')

.controller('CampaignListCtrl', ['$scope', '$rootScope', '$window', '$location','commonDataShare','constants','campaignListService',
    function ($scope, $rootScope, $window, $location , commonDataShare,constants,campaignListService) {

      $scope.campaignHeadings = [
        {header : 'Campaign Id'},
        {header : 'Campaign Name'},
        {header : 'Assgined To '},
        {header : 'Assigned Date'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'View Release Details'},
        {header : 'View Execution Details'}
      ];

      var getCampaignDetails = function(){
        campaignListService.getCampaignDetails($rootScope.globals.currentUser.user_id)
        	.then(function onSuccess(response){
            console.log(response);
        		$scope.campaignData = response.data.data;
            if($scope.campaignData.length == 0){
              $scope.isEmpty = true;
              $scope.msg = constants.emptyCampaignList;
            }
            $scope.loading = response.data;
        	})
        	.catch(function onError(response){
            $scope.isEmpty = true;
            $scope.loading = response;
        		console.log("error occured", response);
            swal(constants.name,constants.errorMsg,constants.error);
        	});
        }

        var getUsersList = function(){
          commonDataShare.getUsersList()
            .then(function onSuccess(response){
              console.log(response);
          		$scope.userList = response.data.data;
          	})
          	.catch(function onError(response){
          		console.log("error occured", response);
              swal(constants.name,constants.errorMsg,constants.error);
          	});
        }

        var init = function(){
          getCampaignDetails();
          getUsersList();
        }
        //Call init function TO Load reuired data initially..
        init();

        $scope.getDetails = function(proposal_id){
          $location.path('/' + proposal_id + '/releasePlan');
        }
        $scope.getExecutionDetails = function(proposal_id){
          $location.path('/' + proposal_id + '/opsExecutionPlan');
        }

    }]);