angular.module('catalogueApp')

.controller('OpsDashCtrl', ['$scope', '$rootScope', '$window', '$location','opsDashBoardService','commonDataShare','constants',

    function ($scope, $rootScope, $window, $location, opsDashBoardService, commonDataShare,constants) {
    	$scope.proposals = [];
      $scope.reason = null;
      $scope.bucket_url = constants.aws_bucket_url;
      //for loading spinner
      $scope.loadSpinner = true;

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

  var getProposalDetails = function(){
    opsDashBoardService.getProposalDetails()
    	.then(function onSuccess(response){
        console.log(response);
    		$scope.proposals = response.data.data;
        if(response.data.data == null){
          $scope.isEmpty = true;
          $scope.msg = constants.emptyProposalMsg;
        }else {
          $scope.isEmpty = false;
        }
        $scope.loading = response.data;
    	})
    	.catch(function onError(response){
        $scope.isEmpty = true;
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
      getProposalDetails();
      getUsersList();
    }
    //Call init function TO Load reuired data initially..
    init();

    $scope.sendNotification = function(){
      $scope.loadSpinner = false;
      var email_Data = {
        subject:'Machadalo Mail',
        body:$scope.reason,
        to:$scope.currentProposal.user.email,
      };
      opsDashBoardService.sendMail(email_Data)
      .then(function onSuccess(response){
        // alert('BD team has been notified');
        $scope.loadSpinner = true;
        $('#onHoldModal').modal('hide');
        $('#declineModal').modal('hide');

        swal(constants.name,constants.onhold_success,constants.success);
    	})
    	.catch(function onError(response){
        $scope.loadSpinner = true;
        $('#onHoldModal').modal('hide');
        $('#declineModal').modal('hide');
        swal(constants.name,constants.onhold_error,constants.error);
    		console.log("error occured", response);
    	});
      $scope.reason = "";
   }

    $scope.updateCampaign = function(proposal){
        $scope.currentProposal = proposal;
      opsDashBoardService.updateProposalDetails(proposal.proposal.proposal_id,proposal.proposal)
      .then(function onSuccess(response){
    	})
    	.catch(function onError(response){
    		console.log("error occured", response);
    	});
    }

    $scope.convertProposalToCampaign = function(proposal){
      $scope.loadSpinner = false;
      $scope.currentProposal = proposal;
      opsDashBoardService.convertProposalToCampaign(proposal.proposal.proposal_id, proposal.proposal)
          .then(function onSuccess(response){
            console.log(response);
            $scope.loadSpinner = true;
              if(response.status == 200){
                $("#assignModal").modal('show');
              }
    	      })
          .catch(function(response){
            getProposalDetails();
            $scope.loadSpinner = true;
            swal(constants.name,constants.accept_proposal_error,constants.error);
    	  	    console.log("error occured", status);
              console.log(response);
    	});
    }

    $scope.convertCampaignToProposal = function(proposal){
      console.log(proposal);
      $scope.currentProposal = proposal;
      opsDashBoardService.convertCampaignToProposal(proposal.proposal.proposal_id, proposal.proposal)
          .then(function onSuccess(response){
            $("#declineModal").modal('show');
              console.table(response);
    	})
          .catch(function onError(response){
            getProposalDetails();
            swal(constants.name,constants.decline_proposal_error,constants.error);
    	  	    console.log("error occured", status);
    	});
    }
    //code added when the user clicks on proposal id the proposal details page will open
    $scope.showProposalDetails = function(proposal_id){
      $location.path('/' + proposal_id + '/showcurrentproposal');
    }

    $scope.saveAssignment = function(){
      var userId = $scope.userId;
      var data = {
        to:userId,
        campaign_id:$scope.currentProposal.proposal.proposal_id
      };
      opsDashBoardService.saveAssignment(data)
          .then(function onSuccess(response){
              console.table(response);
              $('#assignModal').modal('hide');
              swal(constants.name,constants.assign_user_success,constants.success);
    	})
          .catch(function onError(response){
            $('#assignModal').modal('hide');
            swal(constants.name,constants.assign_user_error,constants.error);
    	  	    console.log("error occured", status);
    	});
    }
    $scope.goToCampaignList = function(){
     $location.path("/CampaignList");
    }
}]);//Controller function ends here
