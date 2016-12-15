angular.module('catalogueApp')
.controller('OpsDashCtrl',
    ['$scope', '$rootScope', '$window', '$location','opsDashBoardService',
    function ($scope, $rootScope, $window, $location, opsDashBoardService) {
    	$scope.proposals = [];
      $scope.reason;
    	$scope.headings = [
        {header : 'Proposal Id'},
        {header : 'Proposal Name'},
        {header : 'Created By'},
        {header : 'Invoice Number'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Campaign'},
        {header : 'Download Proposal'}
      ];

    opsDashBoardService.getProposalDetails()
    	.success(function(response, status){
        console.log(response);
    		$scope.proposals = response.data;
    		console.log("$scope.proposals : ", response.data);
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});

    $scope.downloadProposal = function(proposal_id){
        alert('vidhi');
      }

    $scope.sendNotification = function(){
      console.log($scope.currentProposal);
      var email_Data = {
        subject:'Machadalo Mail',
        body:$scope.reason,
        to:$scope.currentProposal.user.email,
      };
      opsDashBoardService.sendMail(email_Data)
      .success(function(response, status){
        alert('hello BD team has been notified');
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});

      $scope.reason = "";
   }

    $scope.updateCampaign = function(proposal){
      if(proposal.proposal.is_campaign == false){
        $scope.currentProposal = proposal;
      }
      opsDashBoardService.updateProposalDetails(proposal.proposal.proposal_id,proposal.proposal)
      .success(function(response, status){
        console.log("Successful",response);
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
    }

    //code added when the user clicks on proposal id the proposal details page will open
    $scope.showProposalDetails = function(proposal_id){
      $location.path('/' + proposal_id + '/showcurrentproposal');
    }
}]);//Controller function ends here
