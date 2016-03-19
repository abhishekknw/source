angular.module('machadaloPages')
.controller('FinalBookingCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location',
    function ($scope, $rootScope, $window, $location) {
    //Start: for document type in modal window
      $scope.documenttypes = [];
         var doctype = [
         {"name":"Invoice"},
         {"name":"Cost Sheet"},
         {"name":"Proposal"}
        ];
        $scope.documenttypes = doctype;
      //End: for document type in modal window

      $scope.companies = [
                    { 'name':'Infosys Technologies',
                    	'employees': 125000,
                    	'headoffice': 'Bangalore'},
                    	{ 'name':'Cognizant Technologies',
	                    	'employees': 100000,
	                    	'headoffice': 'Bangalore'},
	                    	{ 'name':'Wipro',
		                    	'employees': 115000,
		                    	'headoffice': 'Bangalore'},
		                    	{ 'name':'Tata Consultancy Services (TCS)',
			                    	'employees': 150000,
			                    	'headoffice': 'Bangalore'},
			                    	{ 'name':'HCL Technologies',
				                    	'employees': 90000,
				                    	'headoffice': 'Noida'},
      ];
      $scope.addRow = function(){
  	$scope.companies.push({ 'name':$scope.name, 'employees': $scope.employees, 'headoffice':$scope.headoffice });
  	$scope.name='';
  	$scope.employees='';
  	$scope.headoffice='';
  };





}]);//Controller ends here
