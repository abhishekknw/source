angular.module('catalogueApp')
.controller('OpsDashCtrl',
    ['$scope', '$rootScope', '$window', '$location','opsDashBoardService',
    function ($scope, $rootScope, $window, $location, opsDashBoardService) {
    	$scope.proposals = [];
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

$scope.proposals = [
{
	 "proposal_id": "YPrVkSqG",
     "name": "vidhi2",
     "payment_status": false,
     "updated_on": "2016-12-13T07:47:25.164747Z",
     "updated_by": "Admin",
     "created_on": "2016-07-29T12:09:09.064000Z",
     "created_by": "Admin",
     "tentative_cost": 85858,
     "tentative_start_date": null,
     "tentative_end_date": null,
     "is_campaign": false,
     "invoice_number": "456INVOICE",
     "user": 1,
     "account": "VIDHJHBH",
     "parent": null
    }
];
    opsDashBoardService.getProposalDetails()
    	.success(function(response, status){
    		// $scope.proposals = response.data;
    		// console.log("$scope.proposals : ", response.data);
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});

    $scope.downloadProposal = function(proposal_id){
        alert('vidhi');
      }

    $scope.sendNotification = function(){
      alert('hello BD team has been notified');
   }
}]);//Controller function ends here
    
