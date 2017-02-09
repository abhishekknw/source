angular.module('catalogueApp')
.controller('ReleaseCampaignCtrl',
    ['$scope', '$rootScope', '$window', '$location','releaseCampaignService','$stateParams',
    function ($scope, $rootScope, $window, $location, releaseCampaignService, $stateParams) {
  $scope.campaign_id = $stateParams.proposal_id;
 	$scope.headings = [
        {header : 'Supplier Name'},
        {header : 'Area'},
        {header : 'Sub Area'},
        {header : 'Supplier ID'},
        {header : 'Inventory Type'},
        {header : 'Inventory Count'},
        {header : 'Inventory Price'},
        {header : 'Total Price'},
        {header : 'Negotiated Price'},
        {header : 'Booking Status'},
        {header : 'Phase'},
        {header : 'Mode Of Payment'},
        {header : 'Contacts'},
        {header : 'Payment Status'},
      ];
  $scope.booking_status = [
    {name:'Booked', code : 'BK'},
    {name:'Not Booked', code : 'NB'},
  ];
  $scope.contact_headings = [
    {header : 'Salutation'},
    {header : 'Name'},
    {header : 'Contact_type'},
    {header : 'Email'},
    {header : 'STD Code'},
    {header : 'Landline No'},
    {header : 'Mobile No'},

  ];
  $scope.payment_headings = [
    {header : 'Name On Cheque'},
    {header : 'Bank Name'},
    {header : 'IFSC Code'},
    {header : 'Account Number'},
  ];
    $scope.clear = function() {
        $scope.dt = null;
      };

      $scope.maxDate = new Date(2020, 5, 22);
      $scope.today = new Date();
      $scope.popup1 = false;
      $scope.popup2 = false;
      $scope.popup3 = false;
      $scope.error = false;

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

    $scope.saveDetails = function(){
      // alert("vidhi");
    };

    releaseCampaignService.getCampaignReleaseDetails($scope.campaign_id)
    	.success(function(response, status){
    		$scope.releaseDetails = response.data;
        setDataToModel($scope.releaseDetails.shortlisted_suppliers);
            $scope.loading = response;
    	})
    	.error(function(response, status){
    		console.log("error occured", status);
    	});

      var setDataToModel = function(suppliers){
        for(var i=0;i<suppliers.length;i++){
          suppliers[i].total_negotiated_price = parseInt(suppliers[i].total_negotiated_price);
          suppliers[i].phase = parseInt(suppliers[i].phase);
        }
      }
    $scope.emptyList = {NA:'NA'};
    $scope.getFilters = function(supplier){
      var keys = Object.keys(supplier.shortlisted_inventories);
      if(keys.length > 0){
        $scope.inventory_type = supplier.shortlisted_inventories
        return supplier.shortlisted_inventories;
      }
      else{
        return $scope.emptyList;
      }
    }
    //Start:To set contacts to show in contactModal
    $scope.setContact = function(supplier){
      if(supplier.contacts.length > 0)
        $scope.contacts = supplier.contacts;
      else
        $scope.contacts = null;
    }
    //End:To set contacts to show in contactModal
    //Start:To set payment details to show in paymentModal
    $scope.setPayment = function(supplier){
        $scope.payment = supplier;
    }
    //End:To set payment details to show in paymentModal
    //Start: TO go to audit release plan pages
    $scope.changeLocation = function(){
      $location.path('/' + $scope.campaign_id + '/auditReleasePlan');
    }
    //To show inventory ids in modal after clicking on inventory type
    $scope.setInventoryIds = function(filter){
      $scope.inventoryIds = [];
      $scope.inventoryIds = filter.detail;
    }
    $scope.updateData = function(){
      releaseCampaignService.updateAuditReleasePlanDetails($scope.campaign_id,$scope.releaseDetails.shortlisted_suppliers)
      .success(function(response, status){
      })
      .error(function(response, status){
        console.log("error occured", status);
      });
    }
}]);//Controller function ends here
