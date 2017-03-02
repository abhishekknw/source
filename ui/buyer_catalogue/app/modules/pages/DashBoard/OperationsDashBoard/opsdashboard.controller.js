angular.module('catalogueApp')

.controller('OpsDashCtrl', ['$scope', '$rootScope', '$window', '$location','opsDashBoardService','commonDataShare',

    function ($scope, $rootScope, $window, $location, opsDashBoardService, commonDataShare) {
    	$scope.proposals = [];
      $scope.reason;

      //Start: code added to show or hide details based on user permissions
      $scope.user_code = $window.localStorage.user_code;
      if($scope.user_code == 'agency')
        $scope.hideData = true;
      //End: code added to show or hide details based on user permissions
    	$scope.headings = [
        {header : 'Proposal Id'},
        {header : 'Proposal Name'},
        {header : 'Proposal For'},
        {header : 'Proposal Created By'},
        {header : 'Invoice Number'},
        {header : 'Start Date'},
        {header : 'End Date'},
        {header : 'Create Campaign'},
        {header : 'Download Proposal'}
      ];

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

  var getProposalDetails = function(){
    opsDashBoardService.getProposalDetails()
    	.success(function(response, status){
    		$scope.proposals = response.data;
        $scope.loading = response;
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
    }

  var getCampaignDetails = function(){
    opsDashBoardService.getCampaignDetails($rootScope.globals.currentUser.user_id)
    	.success(function(response, status){
        console.log(response);
    		$scope.campaignData = response.data;
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
    }

    var getUsersList = function(){
      commonDataShare.getUsersList()
        .success(function(response, status){
          console.log(response);
      		$scope.userList = response.data;
      	})
      	.error(function(response, status){
      		console.log("error occured", status);
      	});
    }
    var init = function(){
      getProposalDetails();
      getCampaignDetails();
      getUsersList();
    }
    //Call init function TO Load reuired data initially..
    init();

    $scope.sendNotification = function(){
      var email_Data = {
        subject:'Machadalo Mail',
        body:$scope.reason,
        to:$scope.currentProposal.user.email,
      };
      opsDashBoardService.sendMail(email_Data)
      .success(function(response, status){
        // alert('BD team has been notified');
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
      $scope.reason = "";
   }

    $scope.updateCampaign = function(proposal){
        $scope.currentProposal = proposal;
      opsDashBoardService.updateProposalDetails(proposal.proposal.proposal_id,proposal.proposal)
      .success(function(response, status){
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});
    }

    $scope.convertProposalToCampaign = function(proposal){
      $scope.currentProposal = proposal;
      opsDashBoardService.convertProposalToCampaign(proposal.proposal.proposal_id, proposal.proposal)
          .success(function(response, status){
            console.log(response);
              if(status == 200){
                // $scope.showAssignModal = true;
                $("#assignModal").modal('show');
              }
    	})
          .error(function(response, status){
    	  	    console.log("error occured", status);
    	});
    }

    $scope.convertCampaignToProposal = function(proposal){
      $scope.currentProposal = proposal;
      opsDashBoardService.convertCampaignToProposal(proposal.proposal.proposal_id, proposal.proposal)
          .success(function(response, status){
              console.table(response);
    	})
          .error(function(response, status){
    	  	    console.log("error occured", status);
    	});
    }
    //code added when the user clicks on proposal id the proposal details page will open
    $scope.showProposalDetails = function(proposal_id){
      $location.path('/' + proposal_id + '/showcurrentproposal');
    }

    $scope.saveAssignment = function(){
console.log($scope.userId);
      var userId = $scope.userId;
      var data = {
        to:userId,
        campaign_id:$scope.currentProposal.proposal.proposal_id
      };
      opsDashBoardService.saveAssignment(data)
          .success(function(response, status){
              console.table(response);
              getCampaignDetails();
    	})
          .error(function(response, status){
    	  	    console.log("error occured", status);
    	});
    }
    $scope.getDetails = function(proposal_id){
      $location.path('/' + proposal_id + '/releasePlan');
    }
    $scope.getExecutionDetails = function(proposal_id){
      $location.path('/' + proposal_id + '/opsExecutionPlan');
    }
}]);//Controller function ends here
